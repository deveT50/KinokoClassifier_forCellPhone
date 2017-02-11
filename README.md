# KinokoClassifier_forCellPhone  
キノコ分類用スマホアプリ  

キノコを分類するスマホアプリ（HTML5ハイブリッドアプリ）  
フロント  :スマホ（iOS,Android）, monaca  
バック   :Heroku, Flask0.10.1  
画像分類:ubuntu14.04, python2.7, chainer1.14.0  

----------------------





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
![スケッチ](https://s-media-cache-ak0.pinimg.com/736x/b6/17/e6/b617e6bb090c049568e318d69c8e36c2.jpg "ダヴィンチのスケッチ")　　
<img src="https://s-media-cache-ak0.pinimg.com/736x/b6/17/e6/b617e6bb090c049568e318d69c8e36c2.jpg" width="400px">

##フォルダ構成  
* backend_CNN_classifier ・・・・・・・・・・・・・・ chainerで画像分類用CNNモデル作成  
* backend_heroku ・・・・・・・・・・・・・・・・・・・・・・・・・ システムのバックエンド。Herokuにアップロードする  
* frontend_monaca ・・・・・・・・・・・・・・・・・ フロントエンド。monaca（クラウドIDE）のプロジェクトファイル  

使い方は[画像分類](https://github.com/deveT50/MulticlassImageClassifier "")や[Herokuで画像分類](https://github.com/deveT50/imageClassifierOnWeb "")など参考にして下さい。monacaの解説はないですがあしからず・・・  






