import os
from glob import glob
from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
from tensorflow.keras.models import Sequential

from core.utilities.helper import get_directories


if __name__=="__main__":
    catalog_path = Path("coin_catalog/augmented_30")

    """ Hyperparemeters """
    image_shape = (128, 128)

    testrun_name = "crops_predict_30"
    num_epochs = 20
    validation_split = 0.2
    batch_size = 32
    lr = 1e-4

    seed = 42
    np.random.seed(seed)
    tf.random.set_seed(seed)

    """ Directory for storing files """
    if not os.path.exists(output_dir := Path(os.path.dirname(__file__), "trained")):
        os.makedirs(output_dir)

    crops_path = Path(catalog_path, "predict_masks")
    model_path = Path(output_dir, f"{testrun_name}/keras_{testrun_name}.keras")
    crops_dataset_path = Path(output_dir, f"{testrun_name}/crops_dataset_{testrun_name}.tfrecord")
    enum_path = f"trained/enumerations/train_enum_{testrun_name}.json"

    enumerations = [str(coin.parts[-1]) for coin in get_directories(Path(catalog_path, "images"))]

    try:
        crop_dataset = tf.data.Dataset.load(str(crops_dataset_path))
        train_dataset, val_dataset = train_test_split(crop_dataset, test_size=validation_split, random_state=seed)
        print("=== Dataset loaded ===")

    except:
        crop_dataset = tf.keras.utils.image_dataset_from_directory(str(crops_path),
                                                               seed=42,
                                                               batch_size=batch_size,
                                                               image_size=image_shape)

        """ Split dataset into train and validation subsets """
        dataset_size = tf.data.experimental.cardinality(crop_dataset).numpy()
        val_size = int(dataset_size * validation_split)
        train_size = dataset_size - val_size
        train_dataset = crop_dataset.take(train_size)
        val_dataset = crop_dataset.skip(train_size)

        AUTOTUNE = tf.data.AUTOTUNE
        train_ds = train_dataset.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        val_dataset = val_dataset.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)

        print("=== Save datasets ===")
        crop_dataset.save(str(crops_dataset_path))

    for images, labels in train_dataset.take(1):
        print(images.shape, labels.numpy())

    """ Model """
    if not os.path.exists(model_path):
        model = Sequential([
            layers.Rescaling(1. / 255),
            Conv2D(16, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Conv2D(32, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Conv2D(64, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Dropout(0.3),
            Flatten(),
            Dense(128, activation='relu'),
            Dense(len(enumerations), activation='softmax')
        ])

    else:
        print("Model already exists. Loading the model...")
        model = tf.keras.models.load_model(model_path)

    """ Training """
    model.compile(
        optimizer=tf.keras.optimizers.Adam(lr),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=['accuracy']
    )

    callbacks = [
        ModelCheckpoint(model_path, save_best_only=True),
        ReduceLROnPlateau(factor=0.1, patience=5),
        EarlyStopping(patience=15)
    ]

    history = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=num_epochs,
        callbacks=callbacks
    )

    model.save(model_path)