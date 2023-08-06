import tensorflow as tf


def correct_rate(labels, predictions):
    labels = tf.to_int32(labels)
    predictions = tf.to_int32(predictions)

    flag = tf.math.equal(labels, predictions)
    
    correct = tf.math.reduce_all(flag, -1)
    
    fake_predictions = tf.to_int32(correct)
    
    fake_labels = tf.ones(tf.shape(fake_predictions))

    return tf.metrics.accuracy(fake_labels, fake_predictions)


if __name__ == "__main__":
    sess = tf.InteractiveSession()

    labels = [[1, 2, 3], [1, 1, 0], [1, 1, 1]]
    predictions = [[1, 2, 1], [1, 1, 0], [1, 1, 1]]
    result = correct_rate(labels, predictions)

    sess.run(tf.local_variables_initializer())

    sess.run(result[1])
    print(result[0].eval())
