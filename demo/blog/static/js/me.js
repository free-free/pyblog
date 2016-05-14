$(function(){

	function load_server_data(url,callback_func,type,data)
	{
		data=data||{};
		type=type||'get';
		$.ajax({
			'url':url,
			'contentType':'application/x-www-form-urlencoded',
			'dataType':'json',
			'data':data,
			'type':type,
			 success:function(data){
			 	if(data.code!=200)
			 	{
			 		alert('server internal error');
			 	}
			 	else
			 	{
			 		callback_func(data.data);
			 	}
			 }
		})
	}
	function create_music_player(data)
	{
		/*var data=[
			{'music_name':'hello','music_url':'http://localhost/json.php'},
			{'music_name':'hello','music_url':'http://localhost/json.php'},
			{'music_name':'hello','music_url':'http://localhost/json.php'},
			{'music_name':'hello','music_url':'http://localhost/json.php'},
			{'music_name':'hello','music_url':'http://localhost/json.php'},
			{'music_name':'hello','music_url':'http://localhost/json.php'},
			{'music_name':'hello','music_url':'http://localhost/json.php'},
		];*/
		var pHeight=parseInt($(window).innerHeight());
		var audioContent=document.createElement('audio');
		$(audioContent).attr('preload','auto');
		for(var i=0;i<data.length;i++)
		{
			var source=document.createElement('source');
			$(source).attr('title',data[i].music_name);
			$(source).attr('src',data[i].music_url);
			$(source).attr('type','audio/mpeg');
			$(audioContent).append(source);
		}
		var timer;
		$('.music-player-container').css({
			'top':pHeight-300+'px',
			'width':'320px',
			'background':'#333',
		}).on({
			mouseenter:function(){
					clearTimeout(timer)
					timer=setTimeout(function(){
						$('.music-player-container').animate({
						'top':pHeight-300+'px',
						'width':'320px',
						'background':'#333',
						'left':'0px',
						},500)	;
					},500);
				},
			mouseleave:function(){
					clearTimeout(timer);
					timer=setTimeout(function(){
						$('.music-player-container').animate({
						'top':pHeight-300+'px',
						'left':'-310px',
						'background':'#333',
						},500);	
					},1500);
			}
		});
		//$('.music-player-container').append(audioContent);
		$('#myAudio').append(audioContent);
		$('#myAudio').initAudio();
	}
	load_server_data('/music',create_music_player)
})
