$(function(){
	$(window).resize(function(){
		var postWidth=parseInt($('.new-post').width());
		var childWidth=(parseInt($('.main-container').width())-postWidth)/2
		if(childWidth<0)
		{
			childWidth=0;
		}
		$('.new-post').css({
		'position':'absolute',
		'top':'100px',
		'left':childWidth+'px',
		});
		$('.user-activity').css({
			'position':'absolute',
			'left':childWidth+'px',
		})
	})
	function create_arrow(parent){
		var uparrow=document.createElement('div');
		var downarrow=document.createElement('div');
		$(uparrow).addClass('uparrow').addClass('arrow').attr('id',1)
		.append('<i class="icon-caret-up "><i>');
		$(downarrow).addClass('downarrow').addClass('arrow')
		.append('<i class="icon-caret-down"><i>').attr('id',-1);
		$(parent).append(uparrow).append(downarrow).css('color','#555');
	}
	function post_article_init(){
		$('.new-post').css({
		'position':'absolute',
		'width':'800px',
		//'width':parseInt($('.main-container').width())*0.6+'px',
		'top':'100px',
		'left':parseInt($('.main-container').width())*0.2+'px',
		}).fadeIn(2000);	
		$('.post-article').css({
			'top':'-25px',
			'left':parseInt($('.new-post-container').width())*0.96+'px',
			'width':'0px',
			'height':'0px',
			'display':'block',
			'opacity':1
		}).click(function(){
			$(this).find('.post-article-name-span').get(0).click();
		}).hover(function(){
			$(this).find('.post-article-name-span').css('textDecoration','underline');
			$(this).css('boxShadow', '0 0 5px #55aaff');
		}).mouseleave(function(){
			$(this).find('.post-article-name-span').css("textDecoration",'none');
			$(this).css('boxShadow', '0 0 5px #ccc');
		});
		$('.post-article1').css({
			'height':'120px',
			'width':parseInt($('.new-post-container').width())*0.9+'px',
			'top':'25px',
			'left':parseInt($('.new-post-container').width())*0.05+'px',
		}).addClass('current-view-article');

		create_arrow($('.new-post-container'));
		$('.arrow').hover(function(){
				$(this).find('i').addClass('icon-large').css('color','#555');
		}).mouseleave(function(){
				$(this).find('i').removeClass('icon-large').css('color','#ccc');
		}).click(function(){
			var currentViewArticle=$('.current-view-article');
			var cid=parseInt(currentViewArticle.attr('id'));
			if(parseInt($(this).attr('id'))==1)
			{
				if($('.post-article'+(cid-1)).length!=0)
				{		
					
					currentViewArticle.removeClass('current-view-article');
					currentViewArticle.animate({
						'width':10+'px',
						'height':10+'px',
						'top':'10px',
						'borderRadius':'0px',
						'left':parseInt($('.new-post-container').width())*0.95+'px'
					},500,function(){
							$('.np-seg-icon-folder-span').find('i').removeClass('icon-folder-close-alt').addClass('icon-folder-open-alt');	
					}).animate({
						'width':'0px',
						'height':'0px',
						'top':'-25px',
					});
					setTimeout(function(){
						$('.post-article'+(cid-1)).addClass('current-view-article').animate({
								'height':'10px',
								'top':'10px',
								'width':'10px',
								'left':parseInt($('.new-post-container').width())*0.95+'px',
								'opacity':1
						},500,function(){
							$('.np-seg-icon-folder-span').find('i').removeClass('icon-folder-open-alt').addClass('icon-folder-close-alt');	
						}).animate({
							'width':parseInt($('.new-post-container').width())*0.9+'px',
							'height':'120px',
							'top':'25px',
							'left':parseInt($('.new-post-container').width())*0.05+'px',
							'borderRadius':'5px',
						});	
					},1000);
				}
			}
			else
			{
				if($('.post-article'+(cid+1)).length!=0)
				{
					currentViewArticle.removeClass('current-view-article');
					currentViewArticle.animate({
						'width':10+'px',
						'height':10+'px',
						'top':'10px',
						'borderRadius':'0px',
						'left':parseInt($('.new-post-container').width())*0.95+'px'
					},500,function(){
							$('.np-seg-icon-folder-span').find('i').removeClass('icon-folder-close-alt').addClass('icon-folder-open-alt');	
					}).animate({
						'width':'0px',
						'height':'0px',
						'top':'-25px',
					});
					setTimeout(function(){
						$('.post-article'+(cid+1)).addClass('current-view-article').animate({
								'height':'10px',
								'top':'10px',
								'width':'10px',
								'left':parseInt($('.new-post-container').width())*0.95+'px',
								'borderRadius':'0px',
								'opacity':1
						},500,function(){
							$('.np-seg-icon-folder-span').find('i').removeClass('icon-folder-open-alt').addClass('icon-folder-close-alt');	
						}).animate({
							'width':parseInt($('.new-post-container').width())*0.9+'px',
							'height':'120px',
							'left':parseInt($('.new-post-container').width())*0.05+'px',
							'borderRadius':'5px',
							'top':'25px'
						});	
					},1000);
					
				}
			}
		});
	}
	function user_activity_init(upelement){
		$('.user-activity').css({
			'position':'absolute',
			'top':parseInt($(upelement).height())+250+'px',
			'left':parseInt($('.main-container').width())*0.2+'px',
			'height':'400px',
			'width':'800px',
		}).delay(500).slideDown(1000);	
		$('.u-a-span').click(function(){
			$('.hand-right-current-span').get(0).removeChild($('.icon-hand-right-span').get(0));
			$('.u-a-span').removeClass("hand-right-current-span");
			$(this).append('<span class="icon-hand-right-span"><i class="icon-hand-right"></i></span>')
			.addClass('hand-right-current-span');

		});

	}
	post_article_init();
	user_activity_init($('.post-article'));
	$(window).resize();
})


