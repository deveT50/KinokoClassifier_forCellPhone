#!/usr/bin/env python
# -*- coding: utf-8 -*-
#http://tokibito.hatenablog.com/entry/20111204/1322989305
#http://qiita.com/Nawada/items/cf6e4ee46b244fba13c6


#for flask
import os
from flask import Flask, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from flask import send_from_directory
import inspection
#for base64
from PIL import Image
from io import BytesIO
import base64
import json
import uuid
#for DB
import psycopg2
import urlparse
import os


#for sketchize
import sketchize as sket


app = Flask(__name__)

version=0.0






#http://symfoware.blog68.fc2.com/blog-entry-1255.html
#https://developer.salesforce.com/blogs/developer-relations/2016/05/heroku-connect-flask-psycopg2.html
#初期パラメータを端末に与える
def loadParams(version):
	conn = psycopg2.connect(
		host =urlparse.urlparse(os.environ.get('DATABASE_URL')).hostname, 
		port = ,#enter your port No.
		database="your_dbname",
		user="your_username",
		password="your_password")
	cur = conn.cursor()
	cur.execute("SELECT qery to get params ")
	row = cur.fetchone()

	cur.close()
	conn.close()

	return row


#分類結果の文章を取り出す
def loadDescription(result,version):
	conn = psycopg2.connect(
		host =urlparse.urlparse(os.environ.get('DATABASE_URL')).hostname, 
		port = ,#enter your port No.
		database="your_dbname",
		user="your_username",
		password="your_password")
	cur = conn.cursor()
	cur.execute("SELECT sentences for describe classified result WHERE blha blha")
	row = cur.fetchone()
	cur.close()
	conn.close()

	return row




#DBに保存
def saveImageDB(image, result, result_p, version):
	conn = psycopg2.connect(
		host =urlparse.urlparse(os.environ.get('DATABASE_URL')).hostname,
		port = ,#enter your port No.
		database="your_dbname",
		user="your_username",
		password="your_password")
	cur = conn.cursor()
	cur.execute("INSERT INTO your table some image for training the model later")

	conn.commit()
	cur.close()
	conn.close()

	return 0


#root
@app.route('/')
def main():
	return render_template("index.html")


#起こす
@app.route('your/knock/url', methods=['POST'])
def knocked():
	get_json =request.json
	trg=json.loads(get_json)
	result={0:trg['query'],}
	return jsonify(result)


#端末初期化
@app.route('your/init/url', methods=['POST'])
def init():

	get_json =request.json
	trg=json.loads(get_json)
	version=trg['version']
	res=loadParams(version)
	result={0:res[0],
			1:res[1],
			2:res[2],
			3:res[3],
			4:res[4],
			5:res[5],
			6:res[6],
			}


	return jsonify(result)



#base64で画像アップロード
@app.route('your/upload/url', methods=['POST'])
def up2():
	##data=request.form['img']
	get_json =request.json
	trg=json.loads(get_json)
	data=trg['img']
	
	#data = '''R0lGODlhDwAPAKECAAAAzMzM/////wAAACwAAAAADwAPAAACIISPeQHsrZ5ModrLlN48CXF8m2iQ3YmmKqVlRtW4MLwWACH+H09wdGltaXplZCBieSBVbGVhZCBTbWFydFNhdmVyIQAAOw==''' 

	#imgをオープンする
	im = Image.open(BytesIO(base64.b64decode(data)))
	#pngをJPGに
	if im.mode != "RGB":
		im = im.convert("RGB")

	#リサイズする
	size=(256,256)
	im = im.resize(size, Image.ANTIALIAS)


	#保存。存在すれば上書きされる
	#リネーム
	path="tmp/"+uuid.uuid4().hex
	im.save(path+".jpg")



	#分類する
	#result=inspection.inspect(path+".jpg")
	result=inspection.inspect(im)

	#DBに保存
	saveImageDB(data,result[0][2],result[0][1],version)
	#DBから文章を取り出す
	description=loadDescription(result[0][2],version)
	description={
		0:description[0],
		1:description[1],
	}

	#画像をスケッチ風にする
	sketchized=sket.sketchize(path)
	
	#結果listをjsonにして端末に返す
	result={0:{'name':result[0][0],'p':result[0][1], 'class':result[0][2]},
			1:{'name':result[1][0],'p':result[1][1]},
			2:{'name':result[2][0],'p':result[2][1]},
			3:description,
			4:sketchized,
			}

	return jsonify(result)



if __name__ == "__main__":
	app.debug = False
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

