#!/app/.heroku/python/include/python2.7
import math

import chainer
import chainer.functions as F
import numpy as np
import chainer.links as L
import chainer.initializers

class imageModel(chainer.Chain):


	insize = 227
	global w
	w = math.sqrt(2)  # MSRA scaling

	def __init__(self):
		w = math.sqrt(2)  # MSRA scaling
		super(imageModel, self).__init__(
			conv1=L.Convolution2D(3, 8, 7,wscale=w),
			conv2=L.Convolution2D(8, 16, 5,wscale=w),
			conv3=L.Convolution2D(16, 32, 3,wscale=w),
			conv4=L.Convolution2D(32, 48, 3,wscale=w),
		)
		self.train = True


	def predict(self, x_data):
		#x = chainer.Variable(x_data, volatile=True)
		x=x_data
		h = self.conv1(x)
		h = F.relu(h)
		h = F.max_pooling_2d(h, 3, stride=2)

		h = self.conv2(h)
		h = F.relu(h)
		h = F.average_pooling_2d(h, 3, stride=2)

		h = self.conv3(h)
		h = F.relu(h)
		h = F.average_pooling_2d(h, 3, stride=2)
		
		h = self.conv4(h)
		h = F.relu(F.dropout(h, ratio=0.5,train=False))
		h = F.average_pooling_2d(h, 3, stride=2)
		

		y = F.reshape(F.average_pooling_2d(h, 6), (x.data.shape[0],48))

		return F.softmax(y)



