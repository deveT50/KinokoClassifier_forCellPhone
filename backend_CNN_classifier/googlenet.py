#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chainer
import chainer.functions as F
import chainer.links as L
import math
import chainer.initializers
import chainer.cuda

#http://qiita.com/icoxfog417/items/5fd55fad152231d706c2
#Convolutional Layer: 特徴量の畳み込みを行う層
#Pooling Layer: レイヤの縮小を行い、扱いやすくするための層
#まずPooling Layerですが、これは画像の圧縮を行う層になります。画像サイズを圧縮して、後の層で扱いやすくできるメリットがあります。このPoolingを行う手段として、Max Poolingがあります。これは、各領域内の最大値をとって圧縮を行う方法です。

#scikit-learnのpreprocessing.scaleが便利です。

#Fully Connected Layer: 特徴量から、最終的な判定を行う層
#DCGAN
#http://qiita.com/rezoolab/items/5cc96b6d31153e0c86bc
#batchNormalization
#http://hirotaka-hachiya.hatenablog.com/entry/2016/08/06/175824
#http://www.iandprogram.net/entry/2016/02/11/181322
#http://qiita.com/bohemian916/items/9630661cd5292240f8c7

#modelzoo
#modelはライセンス保護されているが、手法は大丈夫だと思う
#https://github.com/BVLC/caffe/wiki/Model-Zoo

#prelu
#http://qiita.com/shima_x/items/8a2f001621dfcbdac028

class GoogLeNet(chainer.Chain):
	#MSRA scaling について	
	#http://qiita.com/dsanno/items/47f52d6f6070ad9847e1
	global xp
	xp=chainer.cuda.cupy
	#insize = 128
	insize = 227
	global w
	w = math.sqrt(2)  # MSRA scaling


	def __init__(self):
		initializer = chainer.initializers.HeNormal()
		super(GoogLeNet, self).__init__(
			#入力チャネル,出力チャネル, フィルタサイズpx
			#209*209が出力チャネル枚
			#Network in Network <http://arxiv.org/abs/1312.4400v3>
			#60.9%モデル--------------------------------------
			#conv1=L.Convolution2D(3, 8, 7),
			#conv2=L.Convolution2D(8, 16, 5),
			#conv3=L.Convolution2D(16, 32, 3),
			#conv4=L.Convolution2D(32, 48, 3),


			conv1=L.Convolution2D(3, 8, 7,wscale=w),
			conv2=L.Convolution2D(8, 16, 5,wscale=w),
			conv3=L.Convolution2D(16, 32, 3,wscale=w),
			conv4=L.Convolution2D(32, 48, 3,wscale=w),

			mo=L.Maxout(4800,32,6,wscale=w),
			
			#-----------------------------------------vasily
			#conv1 = F.Convolution2D(  3,  64, 4, stride = 2, pad = 1, initialW=initializer),
			#conv2 = F.Convolution2D( 64, 128, 4, stride = 2, pad = 1, initialW=initializer),
			#conv3 = F.Convolution2D(128, 256, 4, stride = 2, pad = 1, initialW=initializer),
			#conv4 = F.Convolution2D(256, 512, 4, stride = 2, pad = 1, initialW=initializer),
			#fl	= L.Linear(100352, 2, initialW=initializer),
			#bn1   = F.BatchNormalization(64),
			#bn2   = F.BatchNormalization(128),
			#bn3   = F.BatchNormalization(256),
			#bn4   = F.BatchNormalization(512))


	
			
			###l3=F.Linear(500,7),
			#bn5=L.BatchNormalization(500),
			#l1=L.Linear(256, 512),
			#l2=L.Linear(512, 7)
			#'''
			#conv1=L.Convolution2D(3, 16, 3),
			#bn4=L.BatchNormalization(16),
			#conv2=L.Convolution2D(16, 32, 3),
			#bn5=L.BatchNormalization(32),
			#conv3=L.Convolution2D(32, 64, 3),
			#bn6=L.BatchNormalization(64),
			#l1=L.Linear(43264, 1000),
			#l2=L.Linear(1000, 7),
			#l3=L.Linear(1000, 7)
		)
		self.train = True
	def __call__(self, x, t, train):
		
		"""
		h = F.max_pooling_2d(F.relu(self.mlpconv1(x)), 3, stride=2)
		h = F.max_pooling_2d(F.relu(self.mlpconv2(h)), 3, stride=2)
		h = F.max_pooling_2d(F.relu(self.mlpconv3(h)), 3, stride=2)
		h = self.mlpconv4(F.dropout(h, train=self.train))
		y = F.reshape(F.average_pooling_2d(h, 6), (x.data.shape[0], 1000))
		"""
		"""
		ninのまね
		h = F.max_pooling_2d(F.relu(self.conv1(x)), 3, stride=2)
		h = F.max_pooling_2d(F.relu(self.conv2(h)), 3, stride=2)
		h = F.max_pooling_2d(F.relu(self.conv3(h)), 3, stride=2)
		h = self.conv4(F.dropout(h, train=self.train))
		y = F.reshape(F.average_pooling_2d(h, 6), (x.data.shape[0], 1000))
		"""

		#---------------------------------------------60model
		#h = self.conv1(x)
		#h = F.relu(h)
		#h = F.max_pooling_2d(h, 3, stride=2)

		#h = self.conv2(h)
		#h = F.relu(h)
		#h = F.average_pooling_2d(h, 3, stride=2)

		#h = self.conv3(h)
		#h = F.relu(h)
		#h = F.average_pooling_2d(h, 3, stride=2)
		
		#h = self.conv4(h)
		#h = F.relu(h)
		#h = F.average_pooling_2d(h, 3, stride=2)
		
		#y = F.reshape(F.average_pooling_2d(h, 6), (x.data.shape[0],48))

		#----------------------------------------vasily
		#h = F.relu(self.bn1(self.conv1(x)))
		#h = F.relu(self.bn2(self.conv2(h)))
		#h = F.relu(self.bn3(self.conv3(h)))
		#h = F.relu(self.bn4(self.conv4(h)))
		#y = self.fl(h)

		h = self.conv1(x)
		#h = F.relu(h)
		h = F.prelu(h,xp.ones((8,221,221),dtype=xp.float32)*0.25)		
		h = F.max_pooling_2d(h, 3, stride=2)

		h = self.conv2(h)
		#h = F.relu(h)
		h = F.prelu(h,xp.ones((16,106,106),dtype=xp.float32)*0.15)		
		h = F.average_pooling_2d(h, 3, stride=2)

		h = self.conv3(h)
		#h = F.relu(h)
		#h = F.relu(F.dropout(h, ratio=0.3,train=train))
		h = F.prelu(h,xp.ones((32,50,50),dtype=xp.float32)*0.05)
		h = F.average_pooling_2d(h, 3, stride=2)
		
		h = self.conv4(h)
		h = F.prelu(F.dropout(h, ratio=0.4,train=train),xp.ones((48,22,22),dtype=xp.float32)*0.01)
		#h = F.prelu(h,xp.ones((48,22,22),dtype=xp.float32)*0.01)
		h = F.average_pooling_2d(h, 3, stride=2)
		
		#y=self.mo(F.dropout(h,ratio=0.5,train=train))
		y = F.reshape(F.average_pooling_2d(h, 6), (x.data.shape[0],48))


		"""
		#print x.data.ndim
		#convolution->bn->reluが安定するらしい・・・
		h = self.conv1(x)
		#h = self.bn1(h)
		h = F.relu(h)
		#h = self.bn1(h)
		#n= normarize window size
		#h = F.local_response_normalization(h,n=3)
		#wmax_pooling_2s(x,indowsize,)
		h = F.max_pooling_2d(h, 3, stride=3)

		#print h.data.shape
		h = self.conv2(h)
		#h = self.bn2(h)
		h = F.relu(h)
		#h = F.max_pooling_2d(h, 3, stride=2)
		h = F.average_pooling_2d(h, 3, stride=3)

		h = self.conv3(h)
		#h = self.bn3(h)
		h = F.relu(h)
		#h = self.bn3(h)
		#x, poolingWindowSize, stride=, pad=
		#h = F.max_pooling_2d(h, 3, stride=2)
		h = F.average_pooling_2d(h, 3, stride=3)
		
		h=self.l1(h)
		h=F.relu(h)
		h = F.dropout(h, ratio=0.5, train=train)#0.3
		y = self.l2(h)		

		#h = self.bn4(h)
		#h = F.relu(h)
		
		##h=self.l2(h)
		#h = self.bn4(h)
		##h = F.relu(h)
		#h=F.relu(self.l2(h))
		#y = F.dropout(self.l3(h),ratio=0.3,train=train)#0.2
		#h = self.bn5(h)
		#y = self.l3(h)

		#h = F.relu(self.conv1(x))
		#h = self.bn4(h)
		#h = F.average_pooling_2d(h, 2)
		#h = F.relu(self.conv2(h))
		#h = self.bn5(h)
		#h = F.average_pooling_2d(h, 2)
		#h = F.relu(self.conv3(h))
		#h = self.bn6(h)	
		#h = F.average_pooling_2d(h, 2)
		#h = F.relu(self.l1(x))
		#h = F.dropout(F.relu(self.l1(h)), train=train)
		#y = self.l2(h)
		"""
		#http://qiita.com/supersaiakujin/items/ccdb41c1f33ad5d27fdf
		#活性化関数softmax=exp(a)/sum(exp(a))は、何でもありの入力の値を確率に直す
		if train:
			#cross_entropyは誤差関数。すべてのラベルについて-sum(log(softmax(y))*Label)する。これを最小化したい。
			return F.softmax_cross_entropy(y, t), F.accuracy(y, t)
		else:
			return F.accuracy(y, t)




class GoogLeNetOrigin(chainer.Chain):

	insize = 224

	def __init__(self):
		super(GoogLeNet, self).__init__(
			conv1=L.Convolution2D(3,  64, 7, stride=2, pad=3),
			conv2_reduce=L.Convolution2D(64,  64, 1),
			conv2=L.Convolution2D(64, 192, 3, stride=1, pad=1),
			#inception consists of 1*1,3*3,5*5convolution and maxpooling(convolution)
			#http://docs.chainer.org/en/stable/_modules/chainer/links/connection/inception.html?highlight=Inception
			#inchannel, out1,proj3,out3,proj5,out5,proj_pool,conv_init=none, biase_init=none
			inc3a=L.Inception(192,  64,  96, 128, 16,  32,  32),
			inc3b=L.Inception(256, 128, 128, 192, 32,  96,  64),
			inc4a=L.Inception(480, 192,  96, 208, 16,  48,  64),
			inc4b=L.Inception(512, 160, 112, 224, 24,  64,  64),
			inc4c=L.Inception(512, 128, 128, 256, 24,  64,  64),
			inc4d=L.Inception(512, 112, 144, 288, 32,  64,  64),
			inc4e=L.Inception(528, 256, 160, 320, 32, 128, 128),
			inc5a=L.Inception(832, 256, 160, 320, 32, 128, 128),
			inc5b=L.Inception(832, 384, 192, 384, 48, 128, 128),
			loss3_fc=L.Linear(1024, 1000),

			loss1_conv=L.Convolution2D(512, 128, 1),
			loss1_fc1=L.Linear(4 * 4 * 128, 1024),
			loss1_fc2=L.Linear(1024, 1000),

			loss2_conv=L.Convolution2D(528, 128, 1),
			loss2_fc1=L.Linear(4 * 4 * 128, 1024),
			loss2_fc2=L.Linear(1024, 1000)
		)
		self.train = True

	def __call__(self, x, t, train):
		#if train:
		#	self.train=True
		#else:
		#	self.train=False
		x = chainer.Variable(x, volatile=not train)
		t = chainer.Variable(t, volatile=not train)

		h = F.relu(self.conv1(x))
		h = F.local_response_normalization(
			F.max_pooling_2d(h, 3, stride=2), n=5)
		h = F.relu(self.conv2_reduce(h))
		h = F.relu(self.conv2(h))
		h = F.max_pooling_2d(
			F.local_response_normalization(h, n=5), 3, stride=2)

		h = self.inc3a(h)
		h = self.inc3b(h)
		h = F.max_pooling_2d(h, 3, stride=2)
		h = self.inc4a(h)

		l = F.average_pooling_2d(h, 5, stride=3)
		l = F.relu(self.loss1_conv(l))
		l = F.relu(self.loss1_fc1(l))
		l = self.loss1_fc2(l)
		self.loss1 = F.softmax_cross_entropy(l, t)

		h = self.inc4b(h)
		h = self.inc4c(h)
		h = self.inc4d(h)

		l = F.average_pooling_2d(h, 5, stride=3)
		l = F.relu(self.loss2_conv(l))
		l = F.relu(self.loss2_fc1(l))
		l = self.loss2_fc2(l)
		self.loss2 = F.softmax_cross_entropy(l, t)

		h = self.inc4e(h)
		#print h.data
		h = F.max_pooling_2d(h, 3, stride=2)
		#print h.data
		h = self.inc5a(h)
		#print h.data
		h = self.inc5b(h)
		#print h.data
		h = F.average_pooling_2d(h, 7, stride=1)
		#print h.data
		#h = self.loss3_fc(F.dropout(h, 0.4, train=self.train))
		h = self.loss3_fc(F.dropout(h, 0.4, train=train))
		#print h.data
		self.loss3 = F.softmax_cross_entropy(h, t)
		print h.data
		print t.data
		self.loss = 0.3 * (self.loss1 + self.loss2) + self.loss3
		self.accuracy = F.accuracy(h, t)
		return self.loss, self.accuracy
