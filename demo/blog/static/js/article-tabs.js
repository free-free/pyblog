$(function(){
	$(document).scrollTop(0);
	$('.main-container').css({
		'width':parseInt($(window).innerWidth())-14+'px',
		'margin':'0px auto',
		'position':'relative',
		'overFlowX':'hidden'
	});
	function load_server_data(url,callback_func,type,data){
			data=data||{};
			type=type||'get';
			$.ajax({
				'url':url,
				'dataType':'json',
				'contentType':'application/x-www-form-urlencoded',
				'data':data,
				'type':type,
				'success':function(data){
					if (data.code!=200)
					{
						alert(data.msg);
					}
					else
					{
						callback_func(data.data);	
					}	
				},
			});
	}
	function create_box(id,parent,data)
	{
				/* load each category all article list */
				function category_item_click_handler(data)
				{
					var thisId=parseInt($(this).attr('id'));
					function cancel_btn_click_handler(e)
					{
						$('body').get(0).removeChild($('.article-list-container'+thisId).get(0));
						$('body').get(0).removeChild($('.article-category-screen-mask'+thisId).get(0));
						category_item_mouseleave_handler.apply($('.item'+thisId).category_item_mouseleave_handler);
					}
					if($('.article-category-screen-mask'+thisId).length==0)
					{

							var categoryScreenMask=document.createElement('div');
							var articleListContainer=document.createElement('div');
							var articleListContainerHeader=document.createElement('div');
							var articleListContainerCancelBtn=document.createElement('span');
							var articleListItemContainer=document.createElement('div');
							$(categoryScreenMask)
							.addClass('article-category-screen-mask'+thisId)
							.addClass('article-category-screen-mask');

							$(articleListContainer)
							.addClass('article-list-container')
							.addClass('article-list-container'+thisId)
							.css('height',parseInt(window.innerHeight)+'px');

							$(articleListContainerHeader).addClass('article-list-container-header');
							$(articleListItemContainer).addClass('article-list-item-container')
							.css('height',parseInt($(window).innerHeight())-60+'px');
							;
							$(articleListContainerCancelBtn)
							.addClass('article-list-container-cancel-btn')
							.append('<i class="icon-remove"></i>')
							.click(cancel_btn_click_handler);

							$(articleListContainerHeader).append(articleListContainerCancelBtn);
							$(articleListContainer).append(articleListContainerHeader).append(articleListItemContainer);
							$('body').append(categoryScreenMask).append(articleListContainer);
							$('.article-category-screen-mask').fadeIn(500);
							$('.article-list-container').fadeIn(500);
							for(var i=0;i<data.length;i++)
							{
								var  articleListItem=document.createElement('div');
								var articleTitle=document.createElement('div');
								var articleLink=document.createElement('a');
								var articleDesc=document.createElement('div');
								var articleCategory=document.createElement('span');
								var articlePostDate=document.createElement('span');
								var articleReadNum=document.createElement('span');

								$(articleListItem)
								.addClass('article-list-item')
								.mouseenter(function(){
									$(this).css('boxShadow','0 0 10px #ccc');
									$(this).find('.article-title-link').css('textDecoration','underline');
								})
								.mouseleave(function(){
									$(this).css('boxShadow','none');
									$(this).find('.article-title-link').css('textDecoration','none');
								})
								.click(function(){
									$(this).find('.article-title-link').get(0).click();
								});

								$(articleLink)
								.addClass('article-title-link')
								.text(data[i].article_title)
								.attr('href',data[i].article_url);

								$(articleTitle)
								.addClass('article-title')
								.append('<i class="icon-file-alt"></i>')
								.append(articleLink);

								$(articleDesc)
								.addClass('article-desc')
								.text(data[i].article_desc);

								$(articleCategory)
								.addClass('article-info-item')
								.addClass('article-cate')
								.text('发表于:'+data[i].article_post_date);
								$(articlePostDate)
								.addClass('article-info-item')
								.addClass('article-post-date')
								.text('分类于:'+data[i].article_category);

								$(articleReadNum)
								.addClass('article-info-item')
								.addClass('article-read-num')
								.text('阅读('+data[i].article_read_num+')');

								$(articleListItem)
								.append(articleTitle)
								.append(articleDesc)
								.append(articleCategory)
								.append(articlePostDate)
								.append(articleReadNum);
								$('.article-list-item-container').append(articleListItem);
							}
					}
					else
					{
						$('.article-category-screen-mask'+thisId).fadeIn(500);
						$('.article-list-container'+thisId).fadeIn(500);
					}	
				}
				function create_pin(parent,edgelength)
				{
					//tangelWidth/2
					var pin=document.createElement('span');
					$(pin)
					.addClass('pin')
					.addClass('pin'+id)
					.append('<i class="icon-pushpin icon-2x"></i>')
					.css({
						'display':'block',
						'height':edgelength+'px',
						'lineHeight':edgelength+'px',
						'width':edgelength*2+'px',
						'textAlign':'center',
						'position':'absolute',
						'top':'-10px',
						'left':'5px',
						'color':'#555'
					});
					$(parent).append(pin)
				}
				function create_tangle(parent,tangleW)
				{
					//tangelWidth #1bbcf2',b86424
					var tangle=document.createElement('div');
					$(tangle).css({
							'position':'absolute',
							'width':'0px',
							'height':'0px',
							'border':tangleW+'px solid transparent',
							'borderLeft':tangleW+'px'+' solid #cdb380',
							'borderTop':tangleW+'px'+' solid #cdb380',
							'top':'0px',
							'left':'0px',
							'borderRadius':'10px'
					});
					$(parent).append(tangle);
				}
				function category_item_mouseleave_handler()
				{
					var thisId=$(this).attr('id');
					$(this).css('boxShadow','0 0 5px #ccc');
					$(this).find('.pin').animate({
									'top':'-10px',
									'left':'5px',
									'opacity':1
					},1000);
					$('.track_bar'+thisId).find('.article-category-name-span').css('textDecoration','none');
				}
				function category_item_mouseenter_handler()
				{
						var thisId=$(this).attr('id');
						$(this).css('boxShadow','0 0 10px #444');
						$('.track_bar'+thisId).find(".article-category-name-span").css('textDecoration','underline');
				}
				function create_item_image(parent,imageurl)
				{
					var itemImg=document.createElement('img');
					$(itemImg).attr("src",imageurl);
					$(itemImg).css({
						'display':'block',
						'height':$(parent).height()+'px',
						'width':$(parent).width()+'px',
						'borderRadius':'10px',
					})
					$(parent).append(itemImg);
				}

				var box=document.createElement('div');
				var item=document.createElement('div');				
				var parentWidth=parseInt($(parent).width());
				$(box).attr('id',id).addClass('box'+id).addClass('box');
				$(item).attr('id',id).addClass('item'+id).addClass('item');
				$(box).css({
					'width':parseInt(parentWidth/3)-80+'px',
					'padding':'40px',
					'paddingBottom':'0px',
					'paddingRight':'40px',
					'position':'absolute',
					'top':parseInt($(window).innerHeight())+parseInt($(document).scrollTop())+10+'px',
					'opacity':'0',
					'left':(id%3)*(parentWidth/3)+'px'
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
				}).click(function(){
					$(this).find('.pin').animate({
								'top':'-40px',
								'left':'40px',
								'opacity':0,
					},1000)	;
					thisId=$(this).attr('id');
					setTimeout(function(){
						load_server_data('http://localhost/json.php',$('.item'+thisId).category_item_click_handler,'post',{'rtype':2});
					},1000);
				})
				.mouseenter(category_item_mouseenter_handler)
				.mouseleave(function(){
					var thisId =$(this).attr('id');
					$(this).css('boxShadow','0 0 5px #ccc');
					$('.track_bar'+thisId).find('.article-category-name-span').css("textDecoration",'none');
				});

				create_tangle($(item),parseInt($(item).width())/8);
				create_pin($(item),parseInt($(item).width())/16)
				create_item_image($(item),data.cate_image);
				$(box).append(item);
				$(parent).append(box);

				$.fn.category_item_mouseleave_handler=category_item_mouseleave_handler;
				$.fn.category_item_click_handler=category_item_click_handler;
	}
	function create_left_track_bar(id,parent,text)
	{
			var timer;
			function category_trackbar_mouseenter_handler()
			{
						clearTimeout(timer);
						var item=$('.item'+$(this).attr('id'));
						item.css('boxShadow','0 0 10px #444');	
						$(this).find('.article-category-name-span').css({
							'textDecoration':'underline',
							'color':'#55aaff'
						});
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
								}
								else
								{
										
								}
							},900);
			}
			function category_trackbar_mouseleave_handler()
			{
						clearTimeout(timer);
						$(this).find('.article-category-name-span').css('textDecoration','none');
						$('.item'+$(this).attr('id')).css('boxShadow','0 0 5px #ccc');
			}
			function category_trackbar_click_handler()
			{
				var thisId=$(this).attr('id');
				$('.item'+thisId).find('.pin').animate({
								'top':'-40px',
								'left':'40px',
								'opacity':0,
				},1000)	;
				setTimeout(function(){
					$('.item'+thisId).click();
				},1000);
			}

			var track_bar=document.createElement('div');
			var icon_span=document.createElement('span');
			var cate_span=document.createElement('span');
			$(cate_span).addClass('article-category-name-span').text(text);
			$(icon_span).addClass('article-category-icon-span').append('<i class="icon-tag icon-large"></i>');
			$(track_bar)
			.addClass('track_bar'+id)
			.addClass('article-category-track-bar')
			.attr('id',id)
			.css({
				'width':parseInt($(parent).width())+'px',
				'height':'30px',
			})
			.mouseenter(category_trackbar_mouseenter_handler)
			.mouseleave(category_trackbar_mouseleave_handler)
			.click(category_trackbar_click_handler);
			$(track_bar).append(icon_span).append(cate_span);
			$(parent).append(track_bar);
	}
	function create_view()
	{
		$.fn.lparentdefault_name='lparent';
		$.fn.rparentdefault_name='rparent';
		$.fn.serverdata='';
		var mainContainer=$('.main-container');
		function create_tags_header(parent)
		{
				var tags=document.createElement('div');
				var tagsIcon=document.createElement('span');
				var tagsTitle=document.createElement('span');
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
				}).addClass('tags').append(tagsIcon).append(tagsTitle);	
				$(parent).append(tags);
		}
		function create_tags_container(parent)
		{
			var tagsContainer=document.createElement('div');
			$(tagsContainer).css({
				'width':'100%',
				'background':'#f5f5f5',
				'height':parseInt($(window).innerHeight())-40+'px',
				'overflowX':'hidden'
			}).addClass('tags-container');
			$(parent).append(tagsContainer);
		}
		function create_left_right_parent_box(parent,lparentname,rparentname)
		{
			var leftParentBox=document.createElement('div');
			var rightParentBox =document.createElement('div');	
					$(leftParentBox).css({
					'boxSizing':'borderBox',
					'width':parseInt($(document).width())*0.2+'px',
					'background':'#f5f5f5',
					'position':'absolute',
					'height':parseInt($(window).innerHeight())+'px',
					'left':'0px',
					'overflow':'hidden',
					'top':'0px',
					'borderRight':'1px solid #ccc'
					}).addClass(lparentname);
					$(rightParentBox).css({
								'width':parseInt($(document).width())*0.8-14+'px',
								'float':'right',
								'position':'relative',
								'overFlow':'hidden',
					}).addClass(rparentname);
			$(parent).append(leftParentBox).append(rightParentBox).append('<div class="clear-fix"></div>');
		}
		function lparent_scroll_handler()
		{
			var scrollTop=parseInt($(this).scrollTop());
			var leftParent=$('.'+$.fn.lparentdefault_name);
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
		}
		function render_view(data)
		{
				rightParent=$('.'+$.fn.rparentdefault_name);
				leftParent=$('.'+$.fn.lparentdefault_name);	
				tagsContainer=$('.tags-container');
				for (var i=0;i<data.length;i++)
				{
					/* create category view box*/
					create_box(i,rightParent,data[i]);	
					$('.box'+i).animate({
						'top':parseInt(i/3)*300+'px',
						'opacity':1
					},2000);
					/*create category list bar */
					create_left_track_bar(i,tagsContainer,data[i].cate_name);
					$('.track_bar'+i).animate({'opacity':1,'top':i*30+40+'px'},2000);
				}
		}
		create_left_right_parent_box($('.main-container'),$.fn.lparentdefault_name,$.fn.rparentdefault_name);
		create_tags_header($('.'+$.fn.lparentdefault_name));
		create_tags_container($('.'+$.fn.lparentdefault_name));
		$(document).scroll(lparent_scroll_handler);	
		load_server_data('http://localhost/json.php',render_view,'post',{'rtype':1});
	}
	create_view()
});
