"""TensorFlow DS-CNN-small definition for the 124x10 MFCC input."""
from __future__ import annotations


def build_model(num_classes: int = 14):
    """Build the unquantised training model; TensorFlow is imported lazily."""
    import tensorflow as tf

    inputs = tf.keras.Input(shape=(124, 10, 1), name="mfcc")
    x = tf.keras.layers.Conv2D(24, (5, 5), strides=(2, 2), padding="same", use_bias=False)(inputs)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)
    for filters in (24, 32, 48):
        x = tf.keras.layers.DepthwiseConv2D((3, 3), padding="same", use_bias=False)(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.ReLU()(x)
        x = tf.keras.layers.Conv2D(filters, (1, 1), padding="same", use_bias=False)(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.ReLU()(x)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax", name="class_probabilities")(x)
    return tf.keras.Model(inputs, outputs, name="vaanicore_ds_cnn_small")
