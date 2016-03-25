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
					window.lastMouseY=parseInt(e.offsetY);
					var thisOffsetTop=Math.abs(parseInt($('.article-content').offset().top))-45;	
					var windowH=parseInt($(window).innerHeight());
					if(window.lastMouseY>(windowH*2/3+thisOffsetTop))
					{
							clearInterval(window.upTimer);
							window.upTimer=null;
							if (window.downTimer==null)
							{
								
								window.downTimer=setInterval(function(){
											var articleHeight=parseInt($('.article-content').height());
											var articleOffsetTop=Math.abs(parseInt($('.article-content').offset().top))-45;
											var clientHeight=parseInt(window.innerHeight);
											if((articleOffsetTop+clientHeight)>articleHeight)
											{
													clearInterval(window.downTimer);
													window.downTimer=null;

											}else{
												  var thisOffsetTop=parseInt($('.article-content').offset().top)-45;	
														$('.article-content').css({
															'top':(thisOffsetTop-1)+'px',
															'position':'absolute',
														});		
											}
											
								},100);
							}
					}
					else if(window.lastMouseY<(windowH/3+thisOffsetTop))
					{
							(windowH/3+thisOffsetTop-window.lastMouseY);
							clearInterval(window.downTimer);
							window.downTimer=null;
							if(window.upTimer==null)
							{
								
								window.upTimer=setInterval(function(){
									if((parseInt($('.article-content').offset().top)-45)==0)
									{
											clearInterval(window.downTimer);
											window.downTimer=null;
									}
									else{
											var thisOffsetTop=parseInt($('.article-content').offset().top)-45;	
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
					window.lastMouseY=parseInt(e.offsetY);
					var thisOffsetTop=Math.abs(parseInt($('.article-content').offset().top))-45;	
					var windowH=parseInt($(window).innerHeight());
					if(window.lastMouseY>(windowH*2/3+thisOffsetTop))
					{
							$(this).css('cursor','pointer');
					}
					else if(window.lastMouseY<(windowH/3+thisOffsetTop))
					{
							$(this).css('cursor','pointer');	
					}
					else{
							$(this).css('cursor','default');	
					}

			});
			function scroll_mouse_move(e){
					var mouseClientTop=parseInt(e.clientY);
					var windowHeight=parseInt(window.innerHeight)-45;
					var scrollOffset=(mouseClientTop-window.yPos-45);
					
					//console.log(scrollOffset+60);
						if(scrollOffset<=0)
						{
							$(this).css('top','0px');
							$('.article-content').css('top','0px');
						}	
						else if((scrollOffset+75)>windowHeight)
						{
							$(this).css('top',windowHeight-80+'px');
							$('.article-content').css('top',-1*(windowHeight-80)*window.scrollUnit+'px');
						}else{
							$(this).css('top',scrollOffset+'px');		
							$('.article-content').css('top',-1*scrollOffset*window.scrollUnit+'px');
						}
						
			}
			function scroll_hover(e){
					var mouseDisTop=parseInt(e.clientY);
					var thisDisTop=parseInt($(this).offset().top)
					window.yPos=mouseDisTop-thisDisTop;
					var articleContentHeight=parseInt($('.article-content').height());
					var winH=parseInt(window.innerHeight)-115;
					window.scrollUnit=(articleContentHeight-winH)/winH;
					console.log(window.scrollUnit);
					if(thisDisTop>=45){
						$(this).mousemove(scroll_mouse_move);		
					}else{
						$(this).css('top','0px');
					}
				
			}
			$('.scroll-bar-container').mousedown(scroll_hover).mouseup(function(){
				   $(this).off('mousemove',scroll_mouse_move);
			})
			$(document).mouseup(function(){
				    $('.scroll-bar-container').off('mousemove',scroll_mouse_move);	
			})
	}
	article_content_init();
})