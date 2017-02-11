#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
import sys
import time
import numpy as np
from PIL import Image


import six
import cPickle as pickle
import chainer
import math
import random
import chainer.functions as F
import chainer.links as L
from chainer import serializers

import network
from network import imageModel

mean_image = pickle.load(open("mean.npy", 'rb'))
sigma_image = pickle.load(open("sigma.npy",'rb'))

model = network.imageModel()
serializers.load_hdf5("modelhdf5", model)
cropwidth = 256 - model.insize
model.to_cpu()



def read_image(path, center=False, flip=False):

	image = np.asarray(path).transpose(2, 0, 1)

	top = random.randint(0, cropwidth - 1)
	left = random.randint(0, cropwidth - 1)
	bottom = model.insize + top
	right = model.insize + left
	image = image[:, top:bottom, left:right].astype(np.float32)
	#正規化
	image -= mean_image[:, top:bottom, left:right]
	image/=sigma_image

	return image



def inspect(path):
	
	img = read_image(path)
	x = np.ndarray(
			(1, 3, model.insize, model.insize), dtype=np.float32)
	x[0]=img
	x = chainer.Variable(np.asarray(x), volatile='on')
	score = imageModel.predict(model,x)

	categories = np.loadtxt("labels.txt", str, delimiter="\t")

	#for i in range(len(categories)):
	cat2num={
		categories[0]:0,
		categories[1]:1,
		categories[2]:2,
		categories[3]:3,
		categories[4]:4,
		categories[5]:5,
		categories[6]:6,
	}

	top_k = 3
	prediction = zip(score.data[0].tolist(), categories)
	prediction.sort(cmp=lambda x, y: cmp(x[0], y[0]), reverse=True)
	resList=[]
	for rank, (score, name) in enumerate(prediction[:top_k], start=0):
		pair=(name,score,cat2num[name])
		resList.append(pair)
	return resList




