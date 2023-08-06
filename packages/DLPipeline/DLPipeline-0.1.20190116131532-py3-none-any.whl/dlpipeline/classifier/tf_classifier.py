#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import numpy as np

from dlpipeline.classifier.dlp_classifier import DLPClassifier
from dlpipeline.classifier.persistence.export import export_model
from dlpipeline.classifier.persistence.save import save_graph_to_file
from dlpipeline.classifier.tf_imp.classification_net import classification_net
from dlpipeline.classifier.tf_imp.evaluation import evaluation_nodes, run_final_eval
from dlpipeline.utilities.path_utilities.directory_exists import ensure_directory_exists

__author__ = 'cnheider'

import tensorflow as tf


class TFClassifier(DLPClassifier):

  def __init__(self,
               input: iter = None,
               *,
               input_size,
               output_size,
               C,
               additional_evaluation_terms=()
               ):

    self._C = C
    self._input = input
    self._classifier = classification_net(input_size=input_size,
                                          output_size=output_size,
                                          is_training=True,
                                          learning_rate=self._C.learning_rate,
                                          additional_evaluation_terms=additional_evaluation_terms)

    self._evaluation = evaluation_nodes(result_node=self._classifier.prediction_node,
                                        ground_truth_node=self._classifier.label_node
                                        )

    self._summary = tf.summary.merge_all()

    if tf.gfile.Exists(
        C.summaries_directory):  # Set up the directory we'll write summaries to for TensorBoard
      pass
      # tf.gfile.DeleteRecursively(summaries_directory)
    else:
      tf.gfile.MakeDirs(C.summaries_directory)

    if C.intermediate_store_frequency > 0:
      ensure_directory_exists(C.intermediate_output_graphs_directory)

  def pipeline_function(self,
                        data,
                        label_index,
                        sess,
                        *args,
                        **kwargs):
    return sess.run([self._summary,
                     self._classifier.train_step_node],
                    feed_dict={self._classifier.input_node:data,
                               self._classifier.label_node:label_index
                               }
                    )

  def intermediate_save(self, i, class_count, train_saver, checkpoint_name, intermediate_output_graphs_directory, *, module_specification):
    '''
    # If we want to do an intermediate save,
    # save a checkpoint of the train graph, to restore into
    # the eval graph.
    '''
    train_saver.save(checkpoint_name)

    intermediate_file_name = os.path.join(intermediate_output_graphs_directory,
                                          f'intermediate_model_{i}.pb')

    tf.logging.info(f'Save intermediate result to : {intermediate_file_name}')

    save_graph_to_file(intermediate_file_name,
                       class_count=class_count,
                       checkpoint_name=checkpoint_name,
                       module_specification=module_specification)

  def save(self, dataset, checkpoint_name, C, module_specification, quantize=False,**kwargs):
    '''
    # Write out the trained graph and labels with the weights stored as constants.
    '''

    tf.logging.info(f'Save final result to : {C.output_graph_name}')
    if quantize:
      tf.logging.info('The classifier is instrumented for quantization with TF-Lite')

    save_graph_to_file(C.output_graph_name,
                       module_specification=module_specification,
                       class_count=dataset.class_count,
                       checkpoint_name=checkpoint_name)

    with tf.gfile.GFile(C.output_labels_file_name, 'w') as f:
      f.write('\n'.join(dataset.keys()) + '\n')

    if C.saved_model_directory:
      return export_model(class_count=dataset.class_count,
                          module_specification=module_specification,
                          checkpoint_name=checkpoint_name,
                          saved_model_directory=C.saved_model_directory)

  def test(self,
           sess,
           dataset,
           C,
           *,
           embedder,
           graph_handles):
    pass
    '''run_final_eval(sess,
                   dataset=dataset,
                   jpeg_data_node=graph_handles.jpeg_str_placeholder,
                   resized_image_node=graph_handles.resized_image_node,
                   embedder=embedder,
                   **vars(C))
    '''

  @staticmethod
  def predict(sess,
              *,
              model_graph,
              input_tensor,
              **kwargs):
    input_node = model_graph.get_operation_by_name('resized_input_tensor_placeholder').outputs[0]
    output_node = model_graph.get_operation_by_name(
        'module_apply_default/hub_output/feature_vector/SpatialSqueeze').outputs[0]

    results2 = sess.run(output_node, feed_dict={input_node:input_tensor})

    input_node2 = model_graph.get_operation_by_name('classifier/placeholders/features_placeholder').outputs[0]
    output_node2 = model_graph.get_operation_by_name('softmax_output').outputs[0]

    results = sess.run(output_node2, feed_dict={input_node2:results2})
    results = np.squeeze(results)
    return results
