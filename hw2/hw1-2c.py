import tensorflow as tf
import numpy as np
from keras.datasets import mnist
from keras.utils import np_utils
import time
def generate_data():
	(x_train, y_train), (x_test, y_test) = mnist.load_data()
	print('reshape')
	x_train = np.reshape(x_train, (60000, 28, 28, 1))
	x_test = np.reshape(x_test, (10000, 28, 28, 1))
	y_train = np_utils.to_categorical(y_train)
	y_test = np_utils.to_categorical(y_test)
	return (x_train, y_train, x_test, y_test)

class CNN(object):
	def __init__(self, sess):

		# session
		self.sess = sess

		# input and labels
		self.X = tf.placeholder(tf.float32, shape = (None, 28, 28, 1))
		self.y = tf.placeholder(tf.int32, shape = (None, 10))

		# convulution layer
		with tf.variable_scope("parms"):
			# conv1
			conv1 = tf.layers.conv2d(inputs = self.X,
			 filters = 32, kernel_size = [5, 5],
			 padding = "same", activation = tf.nn.relu)

			# pool1
			pool1 = tf.layers.max_pooling2d(inputs = conv1, pool_size = [2, 2], strides = 2)

			# conv2
			conv2 = tf.layers.conv2d(inputs = pool1, filters = 64, kernel_size = [5, 5], padding = "same", activation = tf.nn.relu)

			# pool2
			pool2 = tf.layers.max_pooling2d(inputs = conv2, pool_size = [2, 2], strides = 2)

			# Dense Layer
			pool2_flat = tf.reshape(pool2, shape = [-1, 7 * 7 * 64])
			dense = tf.layers.dense(inputs = pool2_flat, units = 1024,
				activation = tf.nn.relu)

			# Logits layer
			logits = tf.layers.dense(inputs = dense, units = 10)

		# Loss
		self.loss = tf.reduce_mean(tf.losses.softmax_cross_entropy(self.y, logits = logits))

		# Gradient
		self.parms = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope = "parms")
		self.parms_placeholder = [tf.placeholder(tf.float32, shape = parm.shape) for parm in self.parms]
		self.assign_op = [tf.assign(parm, parm_placeholder) for parm, parm_placeholder in zip(self.parms, self.parms_placeholder)]

		gradients = tf.gradients(ys = self.loss, xs = self.parms)
		squared_para = [tf.reduce_sum(tf.square(gradient)) for gradient in gradients]
		self.squared_gradient = tf.reduce_sum(squared_para)

		# train_op
		self.loss_optimizer = tf.train.AdamOptimizer()
		self.gradient_optimizer = tf.train.AdamOptimizer()

		self.loss_train_op = self.loss_optimizer.minimize(self.loss)
		self.gradient_train_op = self.gradient_optimizer.minimize(self.squared_gradient)

		return

	def cal_min_ratio(self, X_train, sample_epoc = 200, sample_size = 1000):
		cnt = 0
		parms_w = self.sess.run([self.parms])[0]
		loss = self.sess.run([self.loss], feed_dict = {self.X : X_train[-sample_size:], self.y : y_train[-sample_size:]})
		for i in range(sample_epoc):
			# print(i)
			shuffled_parms_w = [parm_w + np.random.standard_normal(parm_w.shape) for parm_w in parms_w]
			sess.run([self.assign_op], feed_dict = {self.parms_placeholder[i] : shuffled_parms_w[i] for i in range(len(shuffled_parms_w))})
			changed_loss = self.sess.run([self.loss], feed_dict = {self.X : X_train[-sample_size:], self.y : y_train[-sample_size:]})
			if changed_loss > loss:
				cnt += 1
		sess.run([self.assign_op], feed_dict = {self.parms_placeholder[i] : parms_w[i] for i in range(len(parms_w))})
		return (cnt / sample_epoc)

	def train(self, X_train, y_train, epoc, train_loss = True):
    	
		loss_list = []
		minimal_ratio_list = []

		if train_loss:
			self.sess.run(tf.global_variables_initializer())

		batch_sz = 128
		N = X_train.shape[0]
		batch_num = N // batch_sz
		for i in range(epoc):
			print(i)

			for j in range(batch_num):
				delta_time = time.time()
				X_batch, y_batch = X_train[j*batch_sz:(j+1)*(batch_sz)], y_train[j*batch_sz:(j+1)*(batch_sz)]
				if train_loss :
					self.sess.run([self.loss_train_op], feed_dict = {self.X : X_batch, self.y : y_batch})
				else:
					self.sess.run([self.gradient_train_op], feed_dict = {self.X : X_batch, self.y : y_batch})
				loss = self.sess.run([self.loss], feed_dict = {self.X : X_batch, self.y : y_batch})
				squared_gradient = self.sess.run([self.squared_gradient], feed_dict = {self.X : X_batch, self.y : y_batch})
				if j % 10 == 0:
					print("loss", loss, "squared_gradient", squared_gradient, "time", time.time() - delta_time)
					if train_loss == False:
						ratio = self.cal_min_ratio(X_train)
						loss_list.append(loss)
						minimal_ratio_list.append(ratio)
						print("ratio: %i"%ratio)

		return list(zip(loss, minimal_ratio_list))


if __name__ == '__main__':
	x_train, y_train, x_test, y_test = generate_data()
	sess = tf.InteractiveSession()
	model = CNN(sess)
	model.train(x_train, y_train, 1)
	print(model.train(x_train, y_train, 2,  train_loss = False))
