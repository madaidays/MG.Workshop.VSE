import tensorflow as tf
import numpy as np

from services.files import rebase_path, create_dir


class VectorGenerator():
    def __init__(self, vectors_path):
        self.vectors_path = vectors_path
        create_dir(self.vectors_path)
        image_model = tf.keras.applications.InceptionV3(include_top=False,
                                                        weights='imagenet')
        new_input = image_model.input
        hidden_layer = image_model.layers[-1].output
        self.model = tf.keras.Model(new_input, hidden_layer)

    def load_image(self, image_path):
        img = tf.io.read_file(image_path)
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.resize(img, (299, 299))
        img = tf.keras.applications.inception_v3.preprocess_input(img)
        return img, image_path

    def save_vectors(self, batch_features, paths, vector_root):
        vector_paths = []
        for bf, p in zip(batch_features, paths):
            path_of_feature = rebase_path(
                p.numpy().decode("utf-8"), vector_root)
            np.save(path_of_feature, bf.numpy())
            vector_paths.append(path_of_feature)
        return vector_paths

    def reshape(self, image_dataset):
        vector_paths = []
        for img, path in image_dataset:
            batch_features = self.model(img)
            batch_features = tf.reshape(batch_features,
                                        (batch_features.shape[0], -1, batch_features.shape[3]))
            batch_vector_paths = self.save_vectors(
                batch_features, path, self.vectors_path)
            vector_paths += batch_vector_paths
        return vector_paths
