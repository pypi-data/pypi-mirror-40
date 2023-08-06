#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from pathlib import Path

import tensorflow as tf

from dlpipeline import TFDataLoader, AlbumentationsAugmentor
from dlpipeline.classifier.tf_classifier import TFClassifier
from dlpipeline.embedder.tf_hub_embedder import TFHubEmbedder

__author__ = 'cnheider'
PROJECT = 'DLPipeline'
CONFIG_NAME = __name__
CONFIG_FILE = __file__
TIME = str(time.time())

# EMBEDDING https://tfhub.dev/
USE_EMBEDDING = False
# EMBEDDING_MODULE = 'https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1'
EMBEDDING_MODULE = ('https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/2')

# PATHS

HOME_DIRECTORY = Path.home()
DATA_HOME = HOME_DIRECTORY / 'Nextcloud/Visual Computing Lab/Projects/IBBD5/Data'
LOGGING_DIRECTORY = HOME_DIRECTORY / 'Models'

DATASET_NAME = 'NONE'

MODEL_DIRECTORY = LOGGING_DIRECTORY / DATASET_NAME / TIME
CHECKPOINT_PATH = MODEL_DIRECTORY / 'checkpoint'
CHECKPOINT_NAME = CHECKPOINT_PATH / 'retrain_checkpoint.ckpt'
INTERMEDIATE_OUTPUT_GRAPHS_DIRECTORY = MODEL_DIRECTORY / 'intermediate_graph'
OUTPUT_LABELS_FILE_NAME = MODEL_DIRECTORY / 'output_labels.txt'
OUTPUT_GRAPH_NAME = MODEL_DIRECTORY / 'output_graph.pbtxt'
SUMMARIES_DIRECTORY = MODEL_DIRECTORY / 'summaries'
SAVED_MODEL_DIRECTORY = MODEL_DIRECTORY / 'export'

# TRAINING

TESTING_PERCENTAGE = 0
VALIDATION_PERCENTAGE = 25
VALIDATION_BATCH_SIZE = 100
STEPS = 10000
LEARNING_RATE = 3e-5
EPOCHS = 7
TRAIN_BATCH_SIZE = 32

# EVALUATION
N_SAMPLES = 10
TOP_N_PREDICTIONS = 5

RANDOM_SCALE = .1
RANDOM_BRIGHTNESS = .1
RANDOM_CROP = .8
RANDOM_ROTATION_DEGREES = 10
FLIP_LEFT_RIGHT = False
FINAL_NODE_NAME = 'final_result'

INTERMEDIATE_STORE_FREQUENCY = 0

EVAL_STEP_INTERVAL = 10
TEST_BATCH_SIZE = -1

BEGIN_AUGMENTING_AT_STEP = 2000
CHECKPOINT_INTERVAL = 5
LOGGING_INTERVAL = 100
VERBOSITY_LEVEL = 1
PRINT_MISCLASSIFIED = False
FINE_TUNE_EMBEDDER = False
FIRST_LEVEL_CATEGORIES = True
DEFAULT_DO_AUGMENTATION = False

TF_CONFIG = tf.ConfigProto()
TF_CONFIG.gpu_options.allow_growth = True
TF_CONFIG.allow_soft_placement = True

DATA_LOADER_TYPE=TFDataLoader
AUGMENTOR_TYPE=AlbumentationsAugmentor
EMBEDDER_TYPE=TFHubEmbedder
CLASSIFIER_TYPE=TFClassifier