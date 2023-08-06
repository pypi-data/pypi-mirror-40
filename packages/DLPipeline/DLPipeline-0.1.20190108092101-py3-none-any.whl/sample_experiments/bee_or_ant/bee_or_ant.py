#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

import tensorflow as tf
import tensorflow_hub as hub
from warg import NOD

from dlpipeline import AlbumentationsAugmentor, TFDataLoader, to_config_object
from dlpipeline.classifier.tf_classifier import TFClassifier
from dlpipeline.demo.web_app_demo.app.app import create_app
from dlpipeline.embedder.tf_hub_embedder import TFHubEmbedder
from dlpipeline.visualiser.visualisation.confusion_matrix import plot_confusion_matrix

__author__ = 'cnheider'

if __name__ == '__main__':
  import bee_or_ant_config as C

  C = to_config_object(C)

  tf.reset_default_graph()
  graph = tf.get_default_graph()
  with graph.as_default() as graph:
    with tf.Session(config=C.tf_config, graph=graph) as sess:

      # region Pipeline Setup

      data_loader = TFDataLoader(C=C, first_level_categories=True)

      # augmentor = TFAugmentor(C=C)
      # augmentor = ImgaugAugmentor(C=C)
      augmentor = AlbumentationsAugmentor(C=C, do_augment=False)

      embedder = TFHubEmbedder(C=C, cache_embeddings=not augmentor.do_augment)

      model = TFClassifier(C=C,
                           input_size=embedder.embedding_size,
                           output_size=data_loader.class_count)

      # endregion

      # region Building

      module_specification = hub.load_module_spec(C.embedding_module)
      height, width = hub.get_expected_image_size(module_specification)
      depth = hub.get_num_image_channels(module_specification)
      a = NOD.dict_of(height, width, depth)

      data_loader.build(**a, sess=sess)
      augmentor.build(**a, sess=sess)
      embedder.build(**a, sess=sess)
      model.build(**a, sess=sess)

      init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
      sess.run(init_op)

      train_saver = tf.train.Saver()

      tf.logging.set_verbosity(tf.logging.INFO)

      train_writer = tf.summary.FileWriter(C.summaries_directory + 'training_set', sess.graph)
      validation_writer = tf.summary.FileWriter(C.summaries_directory + 'validation_set')

      # endregion

      val_gen = data_loader.random_sampler(set_name='validation', sess=sess)

      step_i = 0
      for batch in data_loader.random_sampler(set_name='training', sess=sess):
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
                                  C,
                                  module_specification=module_specification)

        # endregion

      # region Saving

      train_saver.save(sess, C.checkpoint_name)

      checkpoint_name, _ = model.save(data_loader, C, embedder.module_specification)

      base_path = '/'.join(checkpoint_name.split('/')[:-2]) + '/'
      time_path = checkpoint_name.split('/')[-2]

      print(base_path, time_path)

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

      app = create_app(base_path=base_path, time_path=time_path)
      app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

      # endregion
