#!/usr/bin/env python
# -*- coding: utf-8 -*-

# skimage can not be installed before its depending modules. be careful in deploying.
import skimage
from skimage import data, color, io, filters
from skimage.color.adapt_rgb import adapt_rgb, each_channel

#import matplotlib.pyplot as plt
#from matplotlib.colors import LinearSegmentedColormap

import numpy as np
import base64
from PIL import Image

@adapt_rgb(each_channel)
def sobel_each(image):
	return filters.sobel(image)


def sketchize(origin):
	#読み込み
	img=color.rgb2gray(data.imread(origin+".jpg"))

	
	edges = sobel_each(img) #輪郭抽出
	im=1-edges #反転
	

	# 同じサイズの画像を作成
	trans = Image.new('RGBA', (256,256), (0, 0, 0, 0))
	width = 256
	height = 256

	for x in xrange(width):
		for y in xrange(height):
			pixel = int(im[y][x]*255)
			#print pixel
			# 白なら処理しない
			#if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
			if pixel >= 250:
				continue
			#ちょっと色をこくする
			pixel=pixel*0.8
			# 白以外なら、用意した画像にピクセルを書き込み
			trans.putpixel( (x, y), (int(pixel*1.4),int(pixel*1.1),int(pixel*0.9),255) )
	# 透過画像を保存
	trans.save(origin+'_r'+'.png')



	#file読み込み
	file = open(origin+"_r"+".png", 'rt').read()
	#base64でencode
	sketchized = base64.b64encode(file)




	return sketchized

if __name__ == "__main__":
		
	print sketchize("shii")
	



