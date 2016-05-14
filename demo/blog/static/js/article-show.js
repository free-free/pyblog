$(function(){
	window.lastMouseY;
	window.downTimer=null;
	window.upTimer=null;
	window.lastMouseDisTop=null;
	function article_content_init()
	{
			var articleContentH=parseInt($('.article-content').height());
			var windowH=parseInt(window.innerHeight)
			if(articleContentH<windowH)
			{
				$('.article-content').height(windowH);
			}
			$('.article-content').css({
				'width':parseInt($('.article-content-container').width())-60+'px',
				'padding':'30px 30px',
			});
			/* scroll article from up to down or from down to up,when double click event
			be captured in article content specific area*/
			function article_dblclick_handler(e)
			{
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
			}
			/* clear article content scroll timer*/
			function article_mouseleave_handler(e)
			{
					clearInterval(window.downTimer);
					clearInterval(window.upTimer);
					window.upTimer=null;
					window.downTimer=null;
			}
			/* change cursor shape ,when cursor enter in article content specific area*/
			function article_mousemove_handler(e)
			{
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
			}
			/* scroll bar mouse move event handler for article content*/
			function article_scrollbar_mousemove_handler(e)
			{
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
			/* scroll bar  hover event handler and bind scroll bar mouse move event handler*/
			function article_scrollbar_hover_handler(e)
			{
					var thisDisTop=parseInt($(this).position().top);
					var mouseDisTop=parseInt(e.clientY)-45;
					window.yPos=mouseDisTop-thisDisTop;
					if(thisDisTop>=30){
						$(this).mousemove(article_scrollbar_mousemove_handler);		
					}else{
						$(this).css('top','30px');
					}
			}
			/* unbind article scroll bar mousemove event handler*/
			function unbind_article_scrollbar_mousemove()
			{
					    $('.scroll-bar-container').off('mousemove',article_scrollbar_mousemove_handler);	
			}
			/* load article content from backend server*/
			$('.article-content')
			.dblclick(article_dblclick_handler)
			.mouseleave(article_mouseleave_handler)
			.mousemove(article_mousemove_handler);
			
			$('.scroll-bar-container').mousedown(article_scrollbar_hover_handler);
			$(document).mouseup(unbind_article_scrollbar_mousemove);


			$('.article-content').fadeIn(2000);
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
	function create_writing_comment_view(e)
	{
			function write_comment_cancel_btn_click_handler(){
					$('.write-comment-screen-mask').hide();
					$('.write-comment-view-container').hide();
					$('.write-comment-input').val('');
			}	
			if($('.write-comment-screen-mask').length==0)
			{
					/*create element*/
					var writeCommentTitle=document.createElement('span');
					var writeCommentInput=document.createElement('textarea');
					var writeCommentPostBtn=document.createElement('span');
					var writeCommentPostBtnBox=document.createElement('div');
					var writeCommentCancelBtn=document.createElement('span');
					var writeCommentHeader=document.createElement('div');
					var writeCommentViewContainer=document.createElement('div');
					var screenMask=document.createElement('div');

					/* add style class and bind event handler*/
					$(writeCommentTitle).addClass('write-comment-title').text('评论');

					$(writeCommentInput).addClass('write-comment-input');

					$(writeCommentPostBtn).addClass("comment-post-btn")
					.addClass("button button-block button-rounded button-primary button-small")
					.append('<i class="icon-comment"></i>评论');

					$(writeCommentPostBtnBox).addClass('comment-post-btn-box');

					$(writeCommentCancelBtn).addClass('write-comment-cancel-btn')
					.append("<i class='icon-remove'></i>")
					.click(write_comment_cancel_btn_click_handler);

					$(writeCommentHeader).addClass('write-comment-header');

					$(writeCommentViewContainer).addClass('write-comment-view-container');

					$(screenMask).addClass('write-comment-screen-mask');
					/* append parent*/
					$(writeCommentPostBtnBox).append(writeCommentPostBtn);
					$(writeCommentHeader).append(writeCommentTitle).append(writeCommentCancelBtn);
					$(writeCommentViewContainer).append(writeCommentHeader);
					$(writeCommentViewContainer).append(writeCommentInput);
					$(writeCommentViewContainer).append(writeCommentPostBtnBox);
					$('body').append(screenMask).append(writeCommentViewContainer);	
			}
			else
			{
				$('.write-comment-screen-mask').show();
				$('.write-comment-view-container').show();
			}	
	}
	function create_old_comment_view(e)
	{
			function cancel_view_btn_handler()
			{
				$('.old-comment-screen-mask').hide();
				$('.old-comment-view-container').hide();
			}

			if($('.old-comment-screen-mask').length==0)
			{
					data=[1,2,2,3,4];
					var screenMask=document.createElement('div');
					var oldCommentViewContainer=document.createElement('div');
					var oldCommentViewHeaderBox=document.createElement('div');
					var oldCommentViewCancelBtn=document.createElement('span');
					var oldCommentItemContainer=document.createElement('div');
					var oldCommentViewTitle=document.createElement('span');
					$(screenMask).addClass('old-comment-screen-mask');
					$(oldCommentViewContainer).addClass('old-comment-view-container');
					$(oldCommentViewHeaderBox).addClass('old-commet-view-header-box');
					$(oldCommentViewCancelBtn)
					.addClass('old-comment-view-cancel-btn')
					.append('<i class="icon-remove"></i>')
					.click(cancel_view_btn_handler);
					$(oldCommentViewTitle).addClass('old-comment-view-title')
					.append('<i class="icon-comments"></i>历史评论');
					$(oldCommentItemContainer).addClass('old-comment-item-container');
					$(oldCommentItemContainer).css('height',parseInt($(window).innerHeight())-50+'px');
					$(oldCommentViewHeaderBox).append(oldCommentViewCancelBtn).append(oldCommentViewTitle);
					$(oldCommentViewContainer).append(oldCommentViewHeaderBox);
				
					for(var i=0;i<data.length;i++)
					{
							var oldCommentItem=document.createElement('div');
							$(oldCommentItem).addClass('old-comment-item');
							$(oldCommentItemContainer).append(oldCommentItem);
					}
					$(oldCommentViewContainer).append(oldCommentItemContainer);
					$('body').append(screenMask).append(oldCommentViewContainer);	
			}
			else
			{
				$('.old-comment-screen-mask').show();
				$('.old-comment-view-container').show();
			}				
	}
	function comment_init()
	{
		$('.comment-btn').click(create_writing_comment_view);
		$('.old-comment-count').click(create_old_comment_view);
	}
	create_music_player();
	article_content_init();
	comment_init();
})