$(function(){
	$(document).scrollTop(0);
	$('.main-container').css({
		'width':parseInt($(document).width())+'px',
		'margin':'0px auto',
		'position':'relative'
	});
	function create_box(id,parent,name){
				var box=document.createElement('div');
				var item=document.createElement('div');
				var parentWidth=$(parent).width();
				$(box).attr('id',id).addClass('box'+id).addClass('box');
				$(item).attr('id',id).addClass('item'+id).addClass('item');
				$(box).css({
					'width':parseInt(parentWidth/3)+'px',
					'boxSizing':'border-box',
					'padding':'40px',
					'paddingBottom':'0px',
					'position':'absolute',
					'top':parseInt($(window).innerHeight())+parseInt($(document).scrollTop())+10+'px',
					'opacity':'0',
					//'top':parseInt(id/3)*300+'px',
					'left':(id%3)*parseInt(parentWidth/3)+'px'
				})
				if(id==0)
				{
					$(box).addClass('header-box');
				}
				$(item).css({
					'position':'relative',
					'width':parseInt($(box).width())+'px',
					'height':'250px',
					'overFlow':'hidden',
					'borderRadius':'10px',
					'boxShadow':'0 0 5px #ccc',
					'cursor':'pointer',
					'textAlign':'center'
				}).text(name);
				var tangle=document.createElement('div')
				var tangelWidth=parseInt($(item).width())/8;
				$(tangle).css({
					'position':'absolute',
					'width':'0px',
					'height':'0px',
					'border':tangelWidth+'px solid transparent',
					'borderLeft':tangelWidth+'px'+' solid #1bbcf2',
					'borderTop':tangelWidth+'px'+' solid #1bbcf2',
					'top':'0px',
					'left':'0px',
					'borderRadius':'10px'
				});
				var pin=document.createElement('span')
				$(pin).addClass('pin');
				$(pin).addClass('pin'+id);
				$(pin).css({
					'display':'block',
					'height':tangelWidth/2+'px',
					'lineHeight':tangelWidth/2+'px',
					'width':tangelWidth+'px',
					'textAlign':'center',
					'position':'absolute',
					'top':'-10px',
					'left':'5px',
					'color':'#555'
				}).append('<i class="icon-pushpin icon-2x"></i>');
				$(item).append(tangle).append(pin);
				$(box).append(item);
				$(parent).append(box);
	}
	function create_left_track_bar(id,parent,text)
	{
			var track_bar=document.createElement('div');
			var icon_span=document.createElement('span');
			var cate_span=document.createElement('span');
			$(cate_span).css({
					'fontSize':'18px',
					'lineHeight':'30px',
					'display':'inlineBlock',
					'height':'30px',
					'textAlign':'center',
					'color':'#55aaff',
					'letterSpacing':'0px'
			}).addClass('cate_span').text(text);
			$(icon_span).css({
						'display':'inlineBlock',
						'lineHeight':'30px',
						'height':'30px',
						'width':'50px',
						'color':'#818181',
						'fontSize':'14px',
						'textAlign':'center',
						'paddingLeft':'30px',
						'paddingRight':'10px',
						'letterSpacing':'0px',
			}).addClass('icon_span').append('<i class="icon-tag icon-large"></i>');
			$(track_bar).css({
				'boxSizing':'borderBox',
				'height':'30px',
				'lineHeight':'30px',
				'position':'absolute',
				'width':parseInt($(parent).width())+'px',
				'top':parseInt($(window).innerHeight())+parseInt($(document).scrollTop())+10+'px',
				'opacity':0,
				'cursor':'pointer'
			}).addClass('track_bar'+id).attr('id',id);
			$(track_bar).append(icon_span).append(cate_span);
			$(parent).append(track_bar);
	}
	function create_view()
	{
		var leftParentBox=document.createElement('div');
		var rightParentBox =document.createElement('div');
		var tags=document.createElement('div');
		var tagsIcon=document.createElement('span');
		var tagsTitle=document.createElement('span');
		var mainContainer=$('.main-container');
		$(tagsIcon).css({
			'display':'inlineBlock',
			'height':'40px',
			'lineHeight':'40px',
			'width':'40px',
			'paddingLeft':'10px',
			'color':'#333',
			'textAlign':'center',
		}).append('<i class="icon-tags"></i>');
		$(tagsTitle).css({
			'display':'inlineBlock',
			'height':'40px',
			'lineHeight':'40px',
			'paddingLeft':'10px',
			'color':'#333',
			'fontSize':'18px',
			'textAlign':'left'
		}).text('标签');
		$(tags).css({
			'boxSizing':'borderBox',
			'width':'100%',
			'background':'#efefef',
			'position':'absolute',
		}).addClass('tags').append(tagsIcon).append(tagsTitle);
		$(leftParentBox).css({
					'boxSizing':'borderBox',
					'width':parseInt(parseInt($(document).width())*0.2)+'px',
					'background':'#f5f5f5',
					'position':'absolute',
					'height':parseInt($(window).innerHeight())+'px',
					'left':'0px',
					'top':'0px',
					'borderRight':'1px solid #ccc'
		}).addClass('lparent');
		$(leftParentBox).append(tags);

		$(rightParentBox).css({
					'width':parseInt(parseInt($(document).width())*0.8)+'px',
					'float':'right',
					'position':'relative',
					'overFlow':'hidden',
		}).addClass('rparent');
		$(mainContainer).append(leftParentBox).append(rightParentBox).append('<div class="clear-fix></div>"');
		

		$(document).scroll(function(){
			var scrollTop=parseInt($(this).scrollTop());
			var leftParent=$('.lparent');
			var leftParentOff=parseInt($('.main-container').offset().top);
			if(scrollTop>leftParentOff)
			{
				leftParent.css({
					'top':scrollTop-leftParentOff+'px'
				});
			}else{
				leftParent.css({
					'top':'0px'
				});
			}		
		});
		rightParent=$('.rparent');
		leftParent=$('.lparent');
		var list=['linux','git','python','php','javascript','java','css/html','c','c++'];
		for (var i=0;i<10;i++)
				{
					create_box(i,rightParent,list[i]);	
					$('.box'+i).animate({
						'top':parseInt(i/3)*300+'px',
						'opacity':1
					},2000);
					$('.item'+i).hover(function(){
						$(this).css({
							'boxShadow':'0 0 10px #444',
						});
					})
					$('.item'+i).click(function(){
						$(this).find('.pin').animate({
							//'top':-1*(parseInt($(window).innerHeight())+parseInt($(document).scrollTop()))+20+'px',
							'top':'-40px',
							'left':'40px',
							//'left':parseInt($(window).innerWidth())+20+'px',
							'opacity':0,
						},1000)	
					})
					$('.item'+i).mouseleave(function(){
						$(this).css('boxShadow','0 0 5px #ccc');
						$(this).find('.pin').animate({
							'top':'-10px',
							'left':'5px',
							'opacity':1
						},1000);
					});

					create_left_track_bar(i,leftParent,list[i]);
					$('.track_bar'+i).animate({
						'opacity':1,
						'top':i*30+40+'px'
					},2000);
					var timer;
					$('.track_bar'+i).on({
						'mouseenter':function(){
							clearTimeout(timer);
							$(this).css({
							'textDecoration':'underline',
							'color':'#55aaff'
							});
							var item=$('.item'+$(this).attr('id'));
							item.css('boxShadow','0 0 10px #444');	
							that=this
							timer=window.setTimeout(function(){
									var thisId=$(that).attr('id');
									var box=$('.box'+thisId);
									if((parseInt(box.offset().top)+50)>(parseInt($(window).innerHeight())+parseInt($(document).scrollTop())))
									{
										$('.header-box').animate({
											'top':parseInt(box.position().top)+'px',
											'left':parseInt(box.position().left)+'px'
										},400).removeClass('header-box');
										$('.box'+thisId).animate({
											'top':'0px',
											'left':'0px',
										},400).addClass('header-box').find('.item').css({
										'boxShadow':'0 0 10px #444'	
										});
									}else
									{
										
									}
							},900);
						},
						'mouseleave':function(){
							clearTimeout(timer);
							$(this).css({
								'textDecoration':'none'
							});
							$('.item'+$(this).attr('id')).css('boxShadow','0 0 5px #ccc');
						}
					});
				}	
	}
	
	create_view()
});