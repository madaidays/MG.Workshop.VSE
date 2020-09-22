import tensorflow as tf
import numpy as np

from models.inception import VectorGenerator


def evaluate(vse, image_path, vectors_path):
    hidden = vse.decoder.reset_state(batch_size=1)
    tokenizer = vse.tokenizer
    features = vse.encoder(get_image_tensor(image_path, vectors_path))
    dec_input = tf.expand_dims([tokenizer.word_index['<start>']], 0)
    result = []
    for _ in range(200):
        predictions, hidden, _ = vse.decoder(
            dec_input, features, hidden)
        predicted_id = tf.random.categorical(predictions, 1)[0][0].numpy()
        result.append(tokenizer.index_word[predicted_id])

        if tokenizer.index_word[predicted_id] == '<end>':
            break
        dec_input = tf.expand_dims([predicted_id], 0)
    return result


def get_image_tensor(trx_image_path, vectors_path):
    inception = VectorGenerator(vectors_path)
    temp_input = tf.expand_dims(inception.load_image(trx_image_path)[0], 0)
    img_tensor_val = inception.model(temp_input)
    img_tensor_val = tf.reshape(
        img_tensor_val, (img_tensor_val.shape[0], -1, img_tensor_val.shape[3]))
    return np.array(img_tensor_val)
