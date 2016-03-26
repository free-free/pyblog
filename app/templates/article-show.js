$(function(){
	window.lastMouseY;
	window.downTimer=null;
	window.upTimer=null;
	window.lastMouseDisTop=null;
	function article_content_init(){
			var articleContentH=parseInt($('.article-content').height());
			var windowH=parseInt(window.innerHeight)
			if(articleContentH<windowH)
			{
				$('.article-content').height(windowH);
			}
			$('.article-content').css({
				'width':parseInt($('.article-content-container').width())-60+'px',
				'padding':'30px 30px',
			}).dblclick(function(e){
					window.lastMouseY=parseInt(e.clientY);
					var thisOffsetTop=Math.abs(parseInt($('.article-content').position().top));	
					var windowH=parseInt($(window).innerHeight())-75;
					//window.lastMouseY>(windowH*2/3+thisOffsetTop)
					if(window.lastMouseY>(windowH*2/3))
					{
							clearInterval(window.upTimer);
							window.upTimer=null;
							if (window.downTimer==null)
							{
								
								window.downTimer=setInterval(function(){
											var articleHeight=parseInt($('.article-content').height());
											var articleOffsetTop=Math.abs(parseInt($('.article-content').position().top));
											var clientHeight=parseInt(window.innerHeight);
											var scrollUnit=(articleHeight-clientHeight/2-150)/(clientHeight-150);
											if((articleOffsetTop+clientHeight-135)>articleHeight)
											{
													clearInterval(window.downTimer);
													window.downTimer=null;

											}else{

												  var thisOffsetTop=parseInt($('.article-content').position().top);
												  $('.scroll-bar-container').css({
												  			'top':30+Math.abs(thisOffsetTop)/scrollUnit+'px',
												  });
												  $('.article-content').css({
															'top':(thisOffsetTop-1)+'px',
															'position':'absolute',
												});		
											}
											
								},100);
							}
					}
					else if(window.lastMouseY<(windowH/3))
					{
							clearInterval(window.downTimer);
							window.downTimer=null;
							if(window.upTimer==null)
							{
								
								window.upTimer=setInterval(function(){
									var articleHeight=parseInt($('.article-content').height());
									var clientHeight=parseInt(window.innerHeight);
									var scrollUnit=(articleHeight-clientHeight/2-150)/(clientHeight-150);
									if((parseInt($('.article-content').position().top))==0)
									{
											clearInterval(window.downTimer);
											window.downTimer=null;
									}
									else{
											var thisOffsetTop=parseInt($('.article-content').position().top);	
											$('.scroll-bar-container').css({
												  			'top':30+Math.abs(thisOffsetTop)/scrollUnit+'px',
											});
											$('.article-content').css({
												'position':'absolute',
												'top':(thisOffsetTop+1)+'px',
											});	
									}
									
								},100);
							}
					}else{
						clearInterval(window.downTimer);
						clearInterval(window.upTimer);
						window.downTimer=null;
						window.upTimer=null;
					}
					
			}).mouseleave(function(){
					clearInterval(window.downTimer);
					clearInterval(window.upTimer);
					window.upTimer=null;
					window.downTimer=null;
			}).mousemove(function(e){
					window.lastMouseY=parseInt(e.clientY)-75;
					var thisOffsetTop=Math.abs(parseInt($('.article-content').position().top));	
					var windowH=parseInt($(window).innerHeight())-75;
					if(window.lastMouseY>(windowH*2/3))
					{
							$(this).css('cursor','pointer');
					}
					else if(window.lastMouseY<(windowH/3))
					{
							$(this).css('cursor','pointer');	
					}
					else{
							$(this).css('cursor','default');	
					}
			});



			function scroll_mouse_move(e){
					var mouseDisTop=parseInt(e.clientY)-75;
					var windowHeight=parseInt(window.innerHeight)-150;
					var thisDisTop=parseInt($(this).position().top)-30;
					var articleContentHeight=parseInt($('.article-content').height());

					var scrollUnit=(articleContentHeight-windowHeight)/windowHeight;
					var scrollOffset=mouseDisTop-window.yPos;
						if(scrollOffset<0)
						{
							$(this).css('top','30px');
							$('.article-content').css('top','0px');
						}	
						else if((scrollOffset)>windowHeight)
						{
							//$(this).css('top',windowHeight++'px');
							//$('.article-content').css('top',-1*((windowHeight)*scrollUnit)+'px');
						}else{
							$(this).css('top',scrollOffset+30+'px');		
							$('.article-content').css('top',-1*(scrollOffset)*scrollUnit+'px');
						}			
			}
			function scroll_hover(e){
					var thisDisTop=parseInt($(this).position().top);
					var mouseDisTop=parseInt(e.clientY)-45;
					window.yPos=mouseDisTop-thisDisTop;
					if(thisDisTop>=30){
						$(this).mousemove(scroll_mouse_move);		
					}else{
						$(this).css('top','30px');
					}
			}
			$('.scroll-bar-container').mousedown(scroll_hover).mouseup(function(){
				   $(this).off('mousemove',scroll_mouse_move);
			})
			$(document).mouseup(function(){
				    $('.scroll-bar-container').off('mousemove',scroll_mouse_move);	
			})
	}
	function create_music_player()
	{
		var data=[
			{'music_title':'hello','music_url':'http://localhost/json.php'},
			{'music_title':'hello','music_url':'http://localhost/json.php'},
			{'music_title':'hello','music_url':'http://localhost/json.php'},
			{'music_title':'hello','music_url':'http://localhost/json.php'},
			{'music_title':'hello','music_url':'http://localhost/json.php'},
			{'music_title':'hello','music_url':'http://localhost/json.php'},
			{'music_title':'hello','music_url':'http://localhost/json.php'},
		];
		var pHeight=parseInt($(window).innerHeight());
		var audioContent=document.createElement('audio');
		for(var i=0;i<data.length;i++)
		{
			var source=document.createElement('source');
			$(source).attr('title',data[i].music_title);
			$(source).attr('src',data[i].music_url);
			$(audioContent).append(source);
		}
		var timer;
		$('.music-player-container').css({
			'top':pHeight-300+'px',
			'width':'320px',
			'background':'#666',
		}).on({
			mouseenter:function(){
					clearTimeout(timer)
					timer=setTimeout(function(){
						$('.music-player-container').animate({
						'top':pHeight-300+'px',
						'width':'320px',
						'background':'#666',
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
						'background':'#666',
						},500);	
					},1500);
			}
		});
		$('#myAudio').initAudio();
		$('.music-player-container').append(audioContent);
	}
	create_music_player();
	article_content_init();
})