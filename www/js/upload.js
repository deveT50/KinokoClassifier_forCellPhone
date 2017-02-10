// This is a JavaScript file

//元ネタ
//http://stockcode.info/%E3%82%A2%E3%83%97%E3%83%AA/monaca%E3%81%A7%E5%86%99%E7%9C%9F%E3%82%92%E6%92%AE%E5%BD%B1%E3%81%97%E3%81%A6%E3%82%B5%E3%83%BC%E3%83%90%E3%83%BC%E3%81%AB%E3%82%A2%E3%83%83%E3%83%97%E3%83%AD%E3%83%BC%E3%83%89%E3%81%99%E3%82%8B/    
// 撮影した画像データを入れる変数
var g_image = '';
var g_version=0.0;

document.addEventListener ("deviceready", onDeviceReady, false);

//This function is executed when Cordova loading completed.
function onDeviceReady () {
    //window.alert ('Loading Cordova is completed、Camera is now ready to be used.');
    knockHeroku(g_version);
    loadParam(g_version);
}

// 撮影
function camera(isCamera){
    //写真供給元を指定
    var photoMode;
    var wantPreserve;
    if(isCamera==1){
        photoMode=Camera.PictureSourceType.CAMERA;
        wantPreserve=true;
    }else{
        photoMode=navigator.camera.PictureSourceType.PHOTOLIBRARY;
        wantPreserve=false;
    }
    
	navigator.camera.getPicture (onSuccess, onFail, {
		quality: 90, // 画質
		destinationType: Camera.DestinationType.DATA_URL, // base64encodeされた値で取得
		sourceType : photoMode,
		targetWidth:256, // 取得する画像の横幅
		targetHeight:256, // 取得する画像の高さ
		allowEdit: false, // 正方形にトリミングするかどうか
		encodingType: Camera.EncodingType.JPEG,
        correctOrientation: true, // 撮影時と同じ向きに写真を回転
		saveToPhotoAlbum: wantPreserve, // 撮影後、端末のアルバムに画像を保存
	});


	// 成功した際に呼ばれるコールバック関数
	function onSuccess (imageData) {
		// 写真データがあれば挿入
		if(typeof(imageData) != 'undefined' && imageData != '') {	
			// データ保持
			g_image = imageData;
			//画面に挿入
			$('.image').html('<img src="data:image/jpeg;base64,' + imageData + '" width="200">');
            var para0=$('#loading')[0];
            var para1=$('#caption')[0];
            var para2=$('#description')[0];
            para0.innerHTML="classifing...";
            
            //そのままアップロードして、分類結果を受け取る
            upload(para0,para1,para2);
            
		}
	}

	// 失敗した場合に呼ばれるコールバック関数
	function onFail (message) {
		alert(message);
	}
}

/*
//init function
function loadParam(ver){
        var data={'version':ver};
        data=JSON.stringify(data);
		$.ajax({
			type: 'post',
            url:'your/post/url',
            data:JSON.stringify(data),
			dataType:'json',
            contentType:'application/json',
			cache: false,
			async: true,
			success: function(result){
                var res=JSON.stringify(result);
    		    res=JSON.parse(res);
                //alert(res[0]);
                $('#camera')[0].innerHTML=res[1];
                $('#album')[0].innerHTML=res[2];
                
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				alert(errorThrown);
                //description.innerHTML="申し訳ありません。分類できませんでした。";
			},
		});
		
	
}

*/

//init(MySQL)
function loadParam(ver){
        
        var data={'version':ver};
        data=JSON.stringify(data);
    	$.ajax({
			type: 'post',
            url:'your/post/url',
            data:JSON.stringify(data),
			dataType:'json',
            contentType:'application/json',
			cache: false,
			async: true,
			success: function(result){
                var res=JSON.stringify(result);
    		    res=JSON.parse(res);
                //alert(res[0]);
                $('#camera')[0].innerHTML="Camera";//res[1];
                $('#album')[0].innerHTML="Album";//res[2];

			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				alert(errorThrown);
			},
		});
		
	
}


//herokuを起こす
function knockHeroku(query){
        var data={'query':query};
        data=JSON.stringify(data);
        $.ajax({
    		type: 'post',
            url:'your/heroku/url',
            data:JSON.stringify(data),
			dataType:'json',
            contentType:'application/json',
			cache: false,
			async: true,
			success: function(result){
                //alert(result);
                var res=JSON.stringify(result);
    		    res=JSON.parse(res);
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				alert(errorThrown);
			},
		});
		
	
}


// アップロード*分類(herokuPostgres)
function upload(loading,caption,description){
	if(g_image != '') {
        var data={'img':g_image};
        data=JSON.stringify(data);
		$.ajax({
			type: 'post',
            url:'your/post/url',
            data:JSON.stringify(data),
			dataType:'json',
            contentType:'application/json',
			cache: false,
			async: true,
			success: function(result){
                var res=JSON.stringify(result);
    		    res=JSON.parse(res);
			    
                /*
                var parent=$("#resTable")[0];
			    for(var i=0;i<Object.keys(res).length-2;i++){
    				//alert(res[i]['class']);
                    parent.rows[i].cells[0].innerHTML=(String)(i+1)+"位";
    				parent.rows[i].cells[1].innerHTML=res[i]['class'];
    				parent.rows[i].cells[2].innerHTML=(res[i]['p']*100).toFixed(1)+"%";				
			    }
                */
                loading.innerHTML="";
                caption.innerHTML=res[3][0];
                description.innerHTML=res[3][1];
                
                //g_res=res[0]['class'];
                //g_prob=res[0]['p'];
                //mySQLに保存
                storeImage(g_image, res[0]['class'], res[0]['p'], g_version);
                $('.image').html('<img src="data:image/jpeg;base64,' + res[4] + '"width="200">');
                
                
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				alert(errorThrown);
                description.innerHTML="申し訳ありません。分類できませんでした。";
			},
		});
		
	} else {
		description.innerHTML="写真が選択されていません。";
	}

}


//画像保存(MySQL)
function storeImage(image, classid, probability, version){
    if(image != ''){     
        var data={'img':image,
                'clad':classid,
                'prob':probability,
                'ver':version,};
        $.ajax({
			type: 'post',
            url:'your/strage/url',
            data:JSON.stringify(data),
			dataType:'json',
            contentType:'application/json',
			cache: false,
			async: true,
			success: function(result){
                
                var res=JSON.stringify(result);
    		    res=JSON.parse(res);
                //alert(result["image"]);
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				alert(errorThrown);
			},
		});
    }
	
}



