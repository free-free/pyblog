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
		$('#myAudio').append(audioContent);
		$('#myAudio').initAudio();
	}
	
	function create_history_view(data)
	{
		for(var i=0;i<data.length;i++)
		{
			/* left category */
			var categoryListItem=document.createElement('div');
			var arrow=document.createElement('span');
			var connectLine=document.createElement('span');
			var imageCircle=document.createElement('span');
			$(categoryListItem).addClass('category-list-item').text(data[i].cate_name)
			.addClass('category-list-item'+i).attr('id',i);
			$(arrow).addClass('arrow');
			$(connectLine).addClass('connect-line');
			$(imageCircle).addClass('image-circle').append('<img class="cate-circle-image"src="'+data[i].cate_image+'"/>');
			$(categoryListItem).append(arrow).append(connectLine).append(imageCircle);
			$('.left-box').append(categoryListItem);
			
			/*right history line */
			var historyLine=document.createElement('div');
			$(historyLine).addClass('history-line').addClass('history-line'+i).attr('id',i);
			$('.article-history-container').append(historyLine);
		}
		$('.category-list-item').fadeIn(500);
		$('.history-line').show();
		$('.history-date').show();
		function create_history_line_dot(server_back)
		{
				var data=server_back.post_data;
				var date=server_back.date;
			    function create_article_info_note(parent,article_title)
				{
					var articleInfoNote=document.createElement('div');
					var articleInfoNoteTangle=document.createElement('div');
					$(articleInfoNote).addClass('article-info-note')
					.css({
						'position':'absolute',
						'top':'60px',
						'left':'40%',
						'zIndex':99999999999,
						'display':'none'
					}).text(article_title);
					$(articleInfoNoteTangle).css({
						'position':'absolute',
						'width':'0px',
						'height':'0px',
						'border':'8px solid transparent',
						'borderBottom':'8px solid #ff9900',
						'top':'44px',
						'left':'42%',
						'zIndex':999999999,
						'display':'none'
					}).addClass('article-info-note-tangle')
					$(parent).append(articleInfoNote).append(articleInfoNoteTangle);
				}
				for(var i=0;i<date.length;i++)
				{
					var historyDateItem=document.createElement('div');
					$(historyDateItem).addClass('history-date-item').text(date[i])
					.css('width',parseInt($('.article-history-container').width())/6+'px');
					$('.history-date').append(historyDateItem);
				}
				for(var i=0;i<data.length;i++)
				{
					for(var j=0;j<data[i].length;j++)
					{

							var historyPointBox=document.createElement('div');
							var circle=document.createElement('span');
							var straightLine=document.createElement('span');
							if(data[i][j].is_post)
							{
								create_article_info_note($(historyPointBox),data[i][j].article_title);	
								$(circle).addClass('green-history-point-circle')
								.mouseenter(function(){
									$(this).parent().find('.article-info-note-tangle').show();
									$(this).parent().find('.article-info-note').show();
								}).mouseleave(function(){
									$(this).parent().find('.article-info-note').hide();
									$(this).parent().find('.article-info-note-tangle').hide();
								}).click(function(){
									var link=document.createElement('a');
									$(link).attr('href','http://localhost/article-show.html');
									$('body').append(link)
									$(link).get(0).click();
								})
							}
							else
							{
								$(circle).addClass('gray-history-point-circle');	
							}	

							$(straightLine).addClass('history-point-straight-line');
							$(historyPointBox).addClass('history-point-box').css('width',parseInt($('.article-history-container').width())/6+'px');

							$(historyPointBox).append(circle).append(straightLine);
							$('.history-line'+i).append(historyPointBox);
					}
					
				}
		}
		load_server_data('http://localhost/json.php',create_history_line_dot,{'rtype':3});
		
	}

	$('.right-box').css('width',parseInt($('.article-history-list').width())-300+'px');
	$('.right-box').fadeIn(1000);
	$('.footer-container').fadeIn(1000);
	load_server_data('/music',create_music_player);
	load_server_data('',create_history_view,{'rtype':1});
	

	
})
