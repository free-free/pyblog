$(function(){
	function create_arrow(parent){
		var uparrow=document.createElement('div');
		var downarrow=document.createElement('div');
		$(uparrow).addClass('uparrow').addClass('arrow').attr('id',1)
		.append('<i class="icon-caret-up "><i>');
		$(downarrow).addClass('downarrow').addClass('arrow')
		.append('<i class="icon-caret-down"><i>').attr('id',-1);
		$(parent).append(uparrow).append(downarrow).css('color','#555');
	}
	function create_post_artilce_view(data)
	{
		for(var i=0;i<data.length;i++)
		{
				var postArticleContainer=document.createElement('div');
				$(postArticleContainer).addClass('post-article').attr('id',i+1).addClass('post-article'+(i+1));
				var postArticleHeder=document.createElement("div");
				$(postArticleHeder).addClass('post-article-header-line');
				var postArticleDesc=document.createElement("div");
				$(postArticleDesc).addClass('post-article-desc');
				var postArticleInfo=document.createElement("div");
				$(postArticleInfo).addClass('post-article-info');

				//post article header operation
				var iconFileSpan=document.createElement("span")
				$(iconFileSpan).addClass('icon-file-span').append("<i class='icon-file-alt icon-large'></i>");
				var postArticleNameSpan=document.createElement("a");
				$(postArticleNameSpan).addClass("post-article-name-span").text(data[i].article_title).attr('href',data[i].article_url);

				$(postArticleHeder).append(iconFileSpan).append(postArticleNameSpan);

				//post article description operation
				$(postArticleDesc).text(data[i].article_desc);

				//post article information operation
				var postDate=document.createElement('span');
				var postCategory=document.createElement("span");
				var checkNum=document.createElement('span');
				$(postDate).addClass('info-item').addClass('post-date');
				$(postDate).text('发表日期:'+data[i].post_at);
				$(postCategory).addClass('info-item').addClass('post-category');
				$(postCategory).text('分类:'+data[i].article_category);
				$(checkNum).addClass('info-item').addClass('check-num');
				$(checkNum).text('阅读('+data[i].scan_num+')');
				$(postArticleInfo).append(postDate).append(postCategory).append(checkNum);


				// add all to post article container
				$(postArticleContainer).append(postArticleHeder)
				.append(postArticleDesc).append(postArticleInfo);
				$('.new-post-container').append(postArticleContainer);
		}
	}
	function post_article_init(){
		$('.new-post').css({
		'position':'absolute',
		'width':'800px',
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
			$(this).css('boxShadow', '0 0 5px #408dd1');
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
	function create_share_view(data)
	{
		var itemH=parseInt($('.share-content').height())/6;
		var itemW=parseInt($('.share-content').width());
		var icon_arr=['icon-music','icon-film','icon-picture','icon-file-alt'];
		for(var i=0;i<data.length;i++)
		{
			var viewItem=document.createElement('div');
			var icon=document.createElement("span");
			var name=document.createElement("a");
			var desc=document.createElement("span");
			$(icon).css({
				'display':'inlineBlock',
				'height':itemH*0.5+'px',
				'width':'30px',
				'lineHeight':itemH*0.5+'px',
				'paddingLeft':'30px',
				'color':'#828282'
			}).append('<i class="'+icon_arr[data[i].type]+'"></i>');
			$(name).css({
				'display':'inlineBlock',
				'height':itemH*0.5+'px',
				'width':'30px',
				'letterSpacing':'0px',
				'lineHeight':itemH*0.5+'px',
				'paddingLeft':'5px',
				'paddingRight':'10px',
				'fontSize':'16px',
				'color':'#4078c0',
			}).text(data[i].name).attr('href',data[i].url).addClass('name-link');
			$(desc).css({
				'display':'block',
				'height':itemH*0.5+'px',
				'paddingLeft':'80px',
				'lineHeight':itemH*0.4+'px',
				'fontSize':'14px',
				'letterSpacing':'0px',
				'color':'#9f9f9f'
			}).text(data[i].desc)
			$(viewItem).css({
				'boxSizing':'borderBox',
				'width':itemW+'px',
				'height':itemH+'px',
				'borderBottom':'1px solid #ccc',
				'cursor':'pointer'
			}).append(icon).append(name).append(desc).click(function(){
					$(this).find('.name-link').get(0).click();
			}).hover(function(){
				$(this).find('.name-link').css('textDecoration','underline');
			}).mouseleave(function(){
				$(this).find('.name-link').css("textDecoration",'none');
			});
			$('.share-content').append(viewItem);
		}
	}
	function create_reading_view(data)
	{
		var itemH=parseInt($('.reading-content').height())*0.75;
		var itemW=parseInt($('.reading-content').width())/3;
		var timer;
		for(var i=0;i<data.length;i++)
		{	
			viewItemContainer=document.createElement('div');
			viewItem=document.createElement('div');
			bookCommentLink=document.createElement('a');
			bookImage=document.createElement('img');
			bookInfo=document.createElement('div');
			bookName=document.createElement('div');
			bookAuthor=document.createElement('div');
			bookDesc=document.createElement('div');
			angle=document.createElement('div');
			$(bookName).addClass('book-name').text(data[i].book_name);
			$(bookAuthor).addClass('book-author').text(data[i].book_author);
			$(bookDesc).addClass('book-desc').text(data[i].book_desc);
			$(bookInfo).css({
				'width':itemW*1.25+'px',
				'height':itemH*0.9+'px',
				'background':'#dedede',
				'borderRadius':'6px',
				'position':'absolute',
				'padding':'10px 10px',
				'zIndex':99999999999,
				'border':'1px solid #bebebe',
				'top':-1*itemH/6+'px',
				'display':'none',
				'left':itemW*0.88+'px',
			}).addClass("book-info").append(bookName).append(bookAuthor).append(bookDesc);
			$(angle).css({
				'width':'0px',
				'height':'0px',
				'border':'15px solid transparent',
				'borderRight':'15px solid #dedede',
				'position':'absolute',
				'zIndex':9999999999999,
				'display':'none',
				'top':itemH*0.3+'px',
				'left':itemW*0.88-30+'px',
			}).addClass("angle");
			$(bookImage).attr('src',data[i].book_image)
			.css({
				'width':itemW*0.8+'px',
				'height':itemH*0.75+'px',
				'display':'block',
			});
			$(bookName).css({})
			$(bookCommentLink).attr('href',data[i].url)
			.attr('id',i)
			.addClass('book-comment-link'+i)
			.css({
				'width':itemW*0.8+'px',
				'height':itemH*0.75+'px',
				'display':'block',
				'position':'relative',
			}).on({
				mouseenter:function(){
						var that=$(this);
						$(this).parent().css({
						'boxShadow':'0px 0px 20px #ccc',
						});
						$(this).find('.angle').hide();
						$(this).find('.book-info').hide();

						clearTimeout(timer);
						timer=setTimeout(function(){
							$(that).find('.angle').fadeIn(1000);
							$(that).find('.book-info').fadeIn(1000);	
							},500);
						},
				mouseleave:function(){
						var that=$(this);
						$(this).parent().css({
							'boxShadow':'0px 0px 5px #ccc',
						});
						clearTimeout(timer);
						$(that).find('.angle').hide();
						$(that).find('.book-info').hide();		
				}
			}).append(bookImage).append(bookInfo).append(angle);
			$(viewItem).css({
				'width':itemW*0.8+'px',
				'height':itemH*0.75+'px',
				'position':'absolute',
				'top':itemH*0.1+'px',
				'left':itemW*0.1+'px',
				'borderRadius':'5px',
				'border':'1px solid #eee',
				'boxShadow':'0px 0px 5px #ccc',
			}).addClass('reading-content-item').append(bookCommentLink);
			$(viewItemContainer).css({
				'width':itemW+'px',
				'height':itemH+'px',
				'marginTop':itemH/6+'px',
				'boxSizing':'borderBox',
				'position':'relative',
				'float':'left'
			}).append(viewItem);
			$('.reading-content').append(viewItemContainer);
		}
	}
	function user_activity_init(upelement){
		$('.user-activity').css({
			'position':'absolute',
			'top':parseInt($(upelement).height())+180+'px',
			'left':parseInt($('.main-container').width())*0.2+'px',
			'height':'400px',
			'width':'800px',
		}).delay(500).slideDown(1000);	
		/* category for user activity*/
		$('.u-a-span').click(function(){
			$('.hand-right-current-span').get(0).removeChild($('.icon-hand-right-span').get(0));
			$('.u-a-span').removeClass("hand-right-current-span");
			$(this).append('<span class="icon-hand-right-span"><i class="icon-hand-right"></i></span>')
			.addClass('hand-right-current-span');
			$('.current-content').hide().removeClass('current-content');
			switch (parseInt($(this).attr('id')))
			{
				case 1:
					var d=[
						{'type':1,'name':"linux",'desc':'linux is free and great operating system','url':'http://localhost/json.php'},
						{'type':2,'name':"freeBSD",'desc':'linux is free and great operating system','url':'http://localhost/json.php'},
						{'type':3,'name':'jack son','desc':'linux is free and great operating system','url':'http://localhost/json.php'},
						{'type':1,'name':"linux",'desc':'linux is free and great operating system','url':'http://localhost/json.php'},
						{'type':2,'name':"freeBSD",'desc':'linux is free and great operating system','url':'http://localhost/json.php'},
						{'type':3,'name':'jack son','desc':'linux is free and great operating system','url':'http://localhost/json.php'},
					];
					create_share_view(d);
					$('.share-content').fadeIn(1000).addClass("current-content");
					break;
				case 2:
					var d=[
						{'url':'http://localhost/json.php',
						'book_image':'http://localhost/zerotoone.jpg',
						'book_name':"从0到1",
						"book_desc":"Paypal创始人、Facebook第一位外部投资者彼得·蒂尔在本书中详细阐述了自己的创业历程与心得，包括如何避免竞争、如何进行垄断、如何发现新的市场。《从0到1》还将带你穿越哲学、历史、经济等多元领域，解读世界运行的脉络，分享商业与未来发展的逻辑，帮助你思考从0到1的秘密，在意想不到之处发现价值与机会。",
						"book_author":'彼得·蒂尔、布莱克·马斯特斯 '},
						{'url':'http://localhost/json.php','book_image':'http://localhost/mongodb.jpg',
						'book_name':"MongoDB管理与开发实战详解-深入云计算",
						'book_desc':"作为基于分布式文件存储的数据库，在目前的云计算实践中，MongoDB炙手可热。《深入云计算(MongoDB管理与开发实战详解)》系统全面的介绍了MongoDB开发、管理、维护和性能优化等方方面面。详细而深入，对MongoDB的开发和管理方法进行了详细的讲解，也对MongoDB的工作机制进行了深入的探讨。注重实战，通过实际中的案例为读者讲解使用MongoDB时遇到的各种问题，并给出了解决方案。本书旨在帮助云计算初学者迅速掌握MongoDB数据库，提升读者在云计算实践中的应用和开发能力。同时本书极强的系统性和大量翔实的案例对于有一定基础的中高级用户有非常好的参考价值。",
						'book_author':'邹贵金 '},
						{'url':'http://localhost/json.php','book_image':'http://localhost/computersystem.jpg',
						'book_name':'深入理解计算机系统',
						"book_desc":"本书主要介绍了计算机系统的基本概念，包括最深入理解计算机系统各个版本深入理解计算机系统各个版本 (1张)底层的内存中的数据表示、流水线指令的构成、虚拟存储器、编译系统、动态加载库，以及用户应用等。书中提供了大量实际操作，可以帮助读者更好地理解程序执行的方式，改进程序的执行效率。此书以程序员的视角全面讲解了计算机系统，深入浅出地介绍了处理器、编译器、操作系统和网络环境，是这一领域的权威之作",
						'book_author':'（美）布赖恩特'},
					];
					create_reading_view(d);
					$('.reading-content').fadeIn(1000).addClass('current-content');
					break;
			}
		});
		$('.share').click();
	}
	function create_music_player()
	{
		var data=[
			{'music_name':'hello','music_url':'http://localhost/json.php'},
			{'music_name':'hello','music_url':'http://localhost/json.php'},
			{'music_name':'hello','music_url':'http://localhost/json.php'},
			{'music_name':'hello','music_url':'http://localhost/json.php'},
			{'music_name':'hello','music_url':'http://localhost/json.php'},
			{'music_name':'hello','music_url':'http://localhost/json.php'},
			{'music_name':'hello','music_url':'http://localhost/json.php'},
		];
		var pHeight=parseInt($(window).innerHeight());
		var audioContent=document.createElement('audio');
		for(var i=0;i<data.length;i++)
		{
			var source=document.createElement('source');
			$(source).attr('title',data[i].music_name);
			$(source).attr('src',data[i].music_url);
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
		$('#myAudio').append(audioContent)
		$('#myAudio').initAudio();
	}
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
	
	data=[
		{
			'article_title':'linux container',
			'article_url':'http://localhost/json.php',
			'article_desc':'MSIE 正好相反，它使用 event.clientX 和 event.clientY 表示鼠标相当于窗口的位置，而不是文档。在同样的例子中，如果你向下滚动500，clientY 依然是 250，因此，我们需要添加 scrollLeft 和 scrollTop 这两个相对于文档的属性。最后，MSIE 中文档并不是从 0，0 开始，而是通常有一个小的边框（通常是 2 象素），边框的大小定义在 document.body.clientLeft 和 clientTop 中，我们也把这些加进去MSIE 正好相反，它使用 event.clientX 和 event.clientY 表示鼠标相当于窗口的位置，而不是文档。在同样的例子中，如果你向下滚动500，clientY 依然是 250，因此，我们需要添加 scrollLeft 和 scrollTop 这两个相对于文档的属性。最后，MSIE 中文档并不是从 0，0 开始，而是通常有一个小的边框（通常是 2 象素），边框的大小定义在 document.body.clientLeft 和 clientTop 中，我们也把这些加进去',
			'article_category':'linux',
			'post_at':'2016/02/13',
			'scan_num':'40',
		},
		{
			'article_title':'git',
			'article_url':'http://localhost/json.php',
			'article_desc':'MSIE 正好相反，它使用 event.clientX 和 event.clientY 表示鼠标相当于窗口的位置，而不是文档。在同样的例子中，如果你向下滚动500，clientY 依然是 250，因此，我们需要添加 scrollLeft 和 scrollTop 这两个相对于文档的属性。最后，MSIE 中文档并不是从 0，0 开始，而是通常有一个小的边框（通常是 2 象素），边框的大小定义在 document.body.clientLeft 和 clientTop 中，我们也把这些加进去MSIE 正好相反，它使用 event.clientX 和 event.clientY 表示鼠标相当于窗口的位置，而不是文档。在同样的例子中，如果你向下滚动500，clientY 依然是 250，因此，我们需要添加 scrollLeft 和 scrollTop 这两个相对于文档的属性。最后，MSIE 中文档并不是从 0，0 开始，而是通常有一个小的边框（通常是 2 象素），边框的大小定义在 document.body.clientLeft 和 clientTop 中，我们也把这些加进去',
			'article_category':'git',
			'post_at':'2016/02/14',
			'scan_num':'100',
		},
		{
			'article_title':'iptables config',
			'article_url':'http://localhost/json.php',
			'article_desc':'MSIE 正好相反，它使用 event.clientX 和 event.clientY 表示鼠标相当于窗口的位置，而不是文档。在同样的例子中，如果你向下滚动500，clientY 依然是 250，因此，我们需要添加 scrollLeft 和 scrollTop 这两个相对于文档的属性。最后，MSIE 中文档并不是从 0，0 开始，而是通常有一个小的边框（通常是 2 象素），边框的大小定义在 document.body.clientLeft 和 clientTop 中，我们也把这些加进去MSIE 正好相反，它使用 event.clientX 和 event.clientY 表示鼠标相当于窗口的位置，而不是文档。在同样的例子中，如果你向下滚动500，clientY 依然是 250，因此，我们需要添加 scrollLeft 和 scrollTop 这两个相对于文档的属性。最后，MSIE 中文档并不是从 0，0 开始，而是通常有一个小的边框（通常是 2 象素），边框的大小定义在 document.body.clientLeft 和 clientTop 中，我们也把这些加进去',
			'article_category':'linux',
			'post_at':'2016/02/15',
			'scan_num':'4',
		},
		{
			'article_title':'docker',
			'article_url':'http://localhost/json.php',
			'article_desc':'MSIE 正好相反，它使用 event.clientX 和 event.clientY 表示鼠标相当于窗口的位置，而不是文档。在同样的例子中，如果你向下滚动500，clientY 依然是 250，因此，我们需要添加 scrollLeft 和 scrollTop 这两个相对于文档的属性。最后，MSIE 中文档并不是从 0，0 开始，而是通常有一个小的边框（通常是 2 象素），边框的大小定义在 document.body.clientLeft 和 clientTop 中，我们也把这些加进去MSIE 正好相反，它使用 event.clientX 和 event.clientY 表示鼠标相当于窗口的位置，而不是文档。在同样的例子中，如果你向下滚动500，clientY 依然是 250，因此，我们需要添加 scrollLeft 和 scrollTop 这两个相对于文档的属性。最后，MSIE 中文档并不是从 0，0 开始，而是通常有一个小的边框（通常是 2 象素），边框的大小定义在 document.body.clientLeft 和 clientTop 中，我们也把这些加进去',
			'article_category':'linux',
			'post_at':'2016/02/17',
			'scan_num':'30',
		},

	];
	create_post_artilce_view(data);
	post_article_init();
	user_activity_init($('.new-post'));
	create_music_player();
	$(window).resize();
	
})


