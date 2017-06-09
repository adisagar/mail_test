import tensorflow as tf
import numpy as np
import pandas as pd
import pickle

# from sentiment import create_featureset_and_labels
from deepnueral import neural_network_model
from sentiment import featureset_from_lexicon

train_x, train_y , test_x, test_y = pd.read_pickle('Models/sentiment_set.pickle')

#10 class output -

# n_nodes_hl1 = 500
# n_nodes_hl2 = 500
# n_nodes_hl3 = 500

# n_classes = 2
# batch_size = 100

x = tf.placeholder('float', [None,1583])
y = tf.placeholder('float')


# def neural_network_model_delete(data):
#     hidden_1_layer = {'weights' : tf.Variable(tf.random_normal([len(train_x[0]),n_nodes_hl1])), 'biases' : tf.Variable(tf.random_normal([n_nodes_hl1]))}
#     hidden_2_layer = {'weights' : tf.Variable(tf.random_normal([n_nodes_hl1,n_nodes_hl2])), 'biases' : tf.Variable(tf.random_normal([n_nodes_hl2]))}
#     hidden_3_layer = {'weights' : tf.Variable(tf.random_normal([n_nodes_hl2,n_nodes_hl3])), 'biases' : tf.Variable(tf.random_normal([n_nodes_hl3]))}
#     output_layer   = {'weights' : tf.Variable(tf.random_normal([n_nodes_hl3,n_classes])), 'biases' : tf.Variable(tf.random_normal([n_classes]))}

#     l1 = tf.add(tf.matmul(data,hidden_1_layer['weights']), hidden_1_layer['biases'])
#     l1 = tf.nn.relu(l1)

#     l2 = tf.add(tf.matmul(l1,hidden_2_layer['weights']), hidden_2_layer['biases'])
#     l2 = tf.nn.relu(l2)

#     l3 = tf.add(tf.matmul(l2,hidden_3_layer['weights']), hidden_3_layer['biases'])
#     l3 = tf.nn.relu(l3)

#     output = tf.matmul(l3,output_layer['weights']) + output_layer['biases']

    # return output

def predict_mail(x):
    prediction = neural_network_model(x)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess, "model.ckpt")
        correct = tf.equal(tf.argmax(prediction,1), tf.argmax(y,1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print(test_x)
        print('Accuracy:', accuracy.eval({x:test_x, y:test_y}))


def predict_sample(x):
    prediction = neural_network_model(x)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess, "Models/model.ckpt")
        correct = tf.equal(tf.argmax(prediction,1), tf.argmax(y,1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        test_x = featureset_from_lexicon("toMarkThwaites ccMaheshaHolla ccManjunathBhat")
        # print("test_x" ,test_x)
        result = accuracy.eval({x:[test_x], y:[[1,0]]})
        if result == 1:
            print("Replied")
        else:
            print("Not Replied")

predict_sample(x)









