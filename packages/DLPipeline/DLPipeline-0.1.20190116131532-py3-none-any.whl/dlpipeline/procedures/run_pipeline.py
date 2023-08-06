# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

import tensorflow as tf
from warg import NOD

from dlpipeline import AlbumentationsAugmentor, TFDataLoader
from dlpipeline.classifier.tf_classifier import TFClassifier
from dlpipeline.demo.web_app_demo.app.app import create_app
from dlpipeline.embedder.tf_hub_embedder import TFHubEmbedder
from dlpipeline.utilities.hub_size import get_hub_sizes
from dlpipeline.visualiser.visualisation.confusion_matrix import plot_confusion_matrix


def run_pipeline(C, data_loader_type=TFDataLoader,
                 augmentor_type=AlbumentationsAugmentor,
                 embedder_type=TFHubEmbedder,
                 model_type=TFClassifier,
                 **kwargs):
  tf.reset_default_graph()
  graph = tf.get_default_graph()
  with graph.as_default() as graph:
    with tf.Session(config=C.tf_config, graph=graph) as sess:

      # region Pipeline Setup

      data_loader = data_loader_type(C=C)

      augmentor = augmentor_type(C=C, do_augment=C.default_do_augmentation)

      embedder = embedder_type(C=C, cache_embeddings=not augmentor.do_augment, trainable=C.fine_tune_embedder)

      model = model_type(C=C,
                         input_size=embedder.embedding_size,
                         output_size=data_loader.class_count,
                         additional_evaluation_terms=(embedder.embedder_loss,))

      # endregion

      # region Building

      sizes = get_hub_sizes(C)

      pipeline = (data_loader,
                  augmentor,
                  embedder,
                  model)
      for module in pipeline:
        module.build(**sizes, sess=sess)

      init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
      sess.run(init_op)

      train_saver = tf.train.Saver()

      tf.logging.set_verbosity(tf.logging.INFO)

      train_writer = tf.summary.FileWriter(C.summaries_directory + '/training_set', sess.graph)
      validation_writer = tf.summary.FileWriter(C.summaries_directory + '/validation_set')

      # endregion

      val_gen = data_loader.sampler(set_name='validation', sess=sess)

      step_i = 0
      for batch in data_loader.sampler(set_name='training', batch_size=C.train_batch_size, sess=sess):
        x = augmentor.apply(batch.data, sess=sess)
        x = embedder.apply(x,
                           label_index=batch.label_index,
                           label_name=batch.label_name,
                           data_path=batch.data_path,
                           sess=sess)
        train_summary, _ = model.apply(x,
                                       label_index=batch.label_index,
                                       sess=sess)

        step_i += 1
        train_writer.add_summary(train_summary, step_i)

        # region Switches

        if step_i == C.begin_augmenting_at_step:
          augmentor.do_augment = True
          embedder.do_cache_embeddings = not augmentor.do_augment
          print('Started data augmention')

        # endregion

        # region Validation

        if (step_i % C.eval_step_interval) == 0 or step_i + 1 == C.steps:
          train_accuracy, cross_entropy_value, cf_mat_value = sess.run([model._evaluation.accuracy,
                                                                        model._classifier.cross_entropy_node,
                                                                        model._evaluation.cf_mat],
                                                                       feed_dict={
                                                                         model._classifier.input_node:x,
                                                                         model._classifier.label_node:batch.label_index
                                                                         }
                                                                       )

          conf_mat = plot_confusion_matrix(labels=data_loader.keys(),
                                           tensor_name='training/confusion_matrix',
                                           conf_mat=cf_mat_value)
          train_writer.add_summary(conf_mat, step_i)

          v = val_gen.__next__()
          vx = embedder.apply(v.data,
                              label_index=v.label_index,
                              label_name=batch.label_name,
                              data_path=batch.data_path,
                              sess=sess)

          (validation_summary,
           validation_accuracy,
           validation_cf_mat_value) = sess.run([model._summary,
                                                model._evaluation.accuracy,
                                                model._evaluation.cf_mat],
                                               feed_dict={
                                                 model._classifier.input_node:vx,
                                                 model._classifier.label_node:v.label_index
                                                 }
                                               )

          validation_writer.add_summary(validation_summary, step_i)

          val_conf_mat = plot_confusion_matrix(
              labels=data_loader.keys(),
              tensor_name='validation/confusion_matrix',
              conf_mat=validation_cf_mat_value)
          validation_writer.add_summary(val_conf_mat, step_i)

          if step_i % C.logging_interval == 0:
            tf.logging.info(f'{datetime.now()}: '
                            f'Step {step_i:d}: '
                            f'Train accuracy = {train_accuracy * 100:.1f}%%')
            tf.logging.info(f'{datetime.now()}: '
                            f'Step {step_i:d}: '
                            f'Cross entropy = {cross_entropy_value:f}')
            tf.logging.info(f'{datetime.now()}: '
                            f'Step {step_i:d}: '
                            f'Validation accuracy = {validation_accuracy * 100:.1f}%% '
                            f'(N={len(v.label_index):d})')

        # endregion

        # region Checkpointing

        if (C.intermediate_store_frequency > 0 and
            (step_i % C.intermediate_store_frequency == 0) and
            step_i > 0):
          model.intermediate_save(step_i,
                                  data_loader.class_count,
                                  train_saver,
                                  checkpoint_name=C.checkpoint_name + str(step_i),
                                  intermediate_output_graphs_directory=C.intermediate_output_graphs_directory,
                                  module_specification=embedder.module_specification)

        # endregion

        # region Stopping

        if step_i > C.steps:
          break

        # endregion

      # region Saving

      train_saver.save(sess, C.checkpoint_name + str(step_i))

      saved_model_path = model.save(data_loader,
                                    C.checkpoint_name + str(step_i),
                                    C,
                                    embedder.module_specification)

      model.test(sess,
                 data_loader,
                 C,
                 embedder=embedder,
                 graph_handles=NOD(resized_image_node=data_loader._handles.resized_image_node,
                                   jpeg_str_placeholder=data_loader._handles.jpeg_str_placeholder))

      # endregion

      # region Webapp

      print('Finished')
      print('Launching web app')

      app = create_app(base_path=saved_model_path, labels_path=C.output_labels_file_name)
      app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

      # endregion
