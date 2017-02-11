# KinokoClassifier_forCellPhone  
キノコを分類するスマホアプリ（HTML5ハイブリッドアプリ）  

環境  
フロント  :スマホ（iOS,Android）, monaca  
バック   :Heroku, Flask0.10.1  
画像分類:ubuntu14.04, python2.7, chainer1.14.0  

----------------------
<img src="https://github.com/deveT50/images/blob/master/KinokoClassifier_forCellPhone/IMG_1068.PNG" width="200px">
<img src="https://github.com/deveT50/images/blob/master/KinokoClassifier_forCellPhone/IMG_1069.PNG" width="200px">  
スクリーンショット  

##何をするのか  
キノコを分類します。  

##どのように分類するのか？  
1. monacaで作成したHTML5ハイブリッドアプリで、スマホのカメラ・アルバムの写真をHerokuに投げる  
2. Herokuに設置したCNN（コンボリューショナルニューラルネットワーク）モデルで写真に写っているキノコの種類を推定する。  
3. キノコを説明する文章をDBから取り出し、スマホ側に返す。画像もスケッチ風に変換して返す。  

##どんなキノコを分類できるのか？  
* エノキダケ  
* エリンギ  
* シイタケ  
* シメジ  
* タモギタケ  
* ナメコ  
* マイタケ  

##何がやりたかったのか？  
<img src="https://s-media-cache-ak0.pinimg.com/736x/b6/17/e6/b617e6bb090c049568e318d69c8e36c2.jpg" width="300px">  
##結果  
<img src="https://github.com/deveT50/images/blob/master/KinokoClassifier_forCellPhone/IMG_0972.PNG" width="100px"> <img src="https://github.com/deveT50/images/blob/master/KinokoClassifier_forCellPhone/IMG_1081.PNG" width="250px">
<img src="https://github.com/deveT50/images/blob/master/KinokoClassifier_forCellPhone/IMG_1078.PNG" width="150px"> <img src="https://github.com/deveT50/images/blob/master/KinokoClassifier_forCellPhone/IMG_1080.PNG" width="250px">  

読めない＾＾;  

##フォルダ構成  
* backend_CNN_classifier ・・・・・・・・・・・・・・ chainerで画像分類用CNNモデル作成  
* backend_heroku ・・・・・・・・・・・・・・・・・・・・・・・・・ システムのバックエンド。Herokuにアップロードする  
* frontend_monaca ・・・・・・・・・・・・・・・・・ フロントエンド。monaca（クラウドIDE）のプロジェクトファイル  

使い方は[画像分類](https://github.com/deveT50/MulticlassImageClassifier "")や[Herokuで画像分類](https://github.com/deveT50/imageClassifierOnWeb "")など参考にして下さい。monacaの解説はないですがあしからず・・・  







