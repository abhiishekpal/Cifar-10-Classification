import tensorflow as tf
import numpy as np
import pickle
import os
import cv2

path = '/home/knot/Documents/Semester6/Dl/Assignment1/cifar-10-python/cifar-10-batches-py/train_data/data_batch_1'
batch_size = 8
epochs = 3
learning_rate = 0.01
X = tf.placeholder(tf.float32, [None, 32, 32, 3])
Y_ = tf.placeholder(tf.float32, [None, 10])
lr = tf.Variable(0.01)

def convolution_neural_network():

    conv1 = tf.layers.conv2d(inputs = X, filters = 32, kernel_size = 7, padding = "same", activation = tf.nn.relu)
    b_norm1 = tf.layers.batch_normalization(inputs = conv1, axis = -1, momentum = 0.99, epsilon = 0.001, center = True, scale = True)
    pool1 = tf.layers.max_pooling2d(inputs = b_norm1, pool_size = 2, strides=2)

    pool1_flat = tf.reshape(pool1, [-1, 16 * 16 * 32])
    dense = tf.layers.dense(inputs = pool1_flat, units = 1024, activation = tf.nn.relu)
    # dropout = tf.layers.dropout(inputs = dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)
    logits = tf.layers.dense(inputs = dense, units = 10)
    out = tf.nn.softmax(logits, name="softmax_output")

    return out

def nn():
    prediction = convolution_neural_network()
    cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(logits = prediction,labels = Y_))
    optimizer = tf.train.AdamOptimizer(lr).minimize(cost)
    init = tf.global_variables_initializer()
    fo = open(path, 'rb')
    dict_ = pickle.load(fo, encoding='latin1')
    label = dict_['labels']
    data = dict_['data']

    train_y = []
    for i in range(len(label)):
        temp = np.zeros(10)
        temp[label[i]] = 1
        train_y.append(temp)

    train_x = []
    for i in range(len(data)):
        img  = data[i].reshape((32,32,3))
        train_x.append(img)
    epoch = 0
    epoch_loss = 0
    with tf.Session() as sess:
        sess.run(init)
        for epoch in range(epochs):
            epoch_loss = 0
            i = 0
            while i < (2):
                start = i
                end = i+batch_size
                batch_x = np.array(train_x[start:end])
                batch_y = np.array(train_y[start:end])
                _, c, pred = sess.run([optimizer, cost, prediction], feed_dict={X: batch_x, Y_: batch_y, lr: learning_rate})
                print(pred.shape)
                epoch_loss += c
                i+=batch_size
            print('Epoch', epoch+1, 'completed out of',epochs,'loss:',epoch_loss)

        # correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
        # accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        # print('Accuracy:',accuracy.eval({x: batch_x, y:mnist.test.labels}))

def main():
    nn()



if __name__ == "__main__":
    main()
