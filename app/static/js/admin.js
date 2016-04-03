$(function(){
	$(window).scrollTop(0);
	function user_avatar_change_note(){
		$('.user-avatar,.user-avatar-update-mask').hover(function(){
			$('.user-avatar-update-mask').show();
		}).mouseleave(function(){
			$('.user-avatar-update-mask').hide();
		});	
	}
	function load_server_data(url,callback_func,type,data)
	{
			type=type||'GET';
			data=type||{};
			$.ajax({
				'url':url,
				'dataType':'json',
				'contentType':'application/x-www-form-urlencoded',
				'type':type,
				'data':data,
				success:function(data){
					if(data.code!=200)
					{
						alert("server error!");
					}
					else
					{
						callback_func(data.data);
					}
				}
			});
	}
	function load_user_activity_item(data)
	{
		var userActivity=$('.user-activity');
		var userActivityItem=$('.user-activity-item').last();
		for(var i=0;i<data.length;i++)
		{
			var cloneActivityItem=userActivityItem.clone(true);
			cloneActivityItem.find('.user-activity-item-headerline-avatar>img').attr('src',data[i].user_avatar);
			cloneActivityItem.find('.user-activity-item-headerline-user-name').text(data[i].user_name);
			cloneActivityItem.find('.user-activity-item-headerline-post-at').text(data[i].post_at);
			cloneActivityItem.find('.user-activity-item-content-title').text(data[i].title).attr("href",data[i].url);
			cloneActivityItem.find('.user-activity-item-content-main').text(data[i].description);
			userActivity.append(cloneActivityItem);
		}
	}
	function scroll_event(){
		$(document).scroll(function(){
			var lastItem=$('.user-activity-item').last();
			var itemHeight=parseInt(lastItem.height());
			var lastItemOffTop=parseInt(lastItem.offset().top);
			var scrollTop=parseInt($(this).scrollTop());
			var winHeight=parseInt($(window).innerHeight());
			if((scrollTop+winHeight)>(lastItemOffTop+itemHeight/2))
			{
				data=[
				{'user_avatar':'./static/image/java.jpg','user_name':'helloforworld','post_at':'2016/04/02','title':'Linux Container','description':'多‘正确的废话’，那么这本书为啥能让如此多牛逼机构牛逼大神推荐，让心神创业的骚年们不断高潮呢？ 2 条评论 按投票排序 按时间排序 18 个回答 知乎用户，苦逼的产品设计和运营佬 知乎用户、南鹏、Syan 等人赞同 看不懂的是小白，觉得作用不大的还处于给别人打工的状态，感觉通透的都是对趋势有感觉的，觉得内容中讲历史金融哲学多余的都是生意人还不是企业家。 发布于 2015-05-14 2 条评论 感谢 收藏 • 没有帮助 • • 作者保留权利 徐文瑞，计蒜客 / 产品经理 / 天蝎座的 INTJ 李少鹏、西西豆豆、知乎用户 等人赞同 作者都快被捧成神了，他的书会火也是正','url':'http://localhost:8000/articles'},
				{'user_avatar':'./static/image/python.jpg','user_name':'helloforworld','post_at':'2016/04/02','title':'Linux Container','description':'多‘正确的废话’，那么这本书为啥能让如此多牛逼机构牛逼大神推荐，让心神创业的骚年们不断高潮呢？ 2 条评论 按投票排序 按时间排序 18 个回答 知乎用户，苦逼的产品设计和运营佬 知乎用户、南鹏、Syan 等人赞同 看不懂的是小白，觉得作用不大的还处于给别人打工的状态，感觉通透的都是对趋势有感觉的，觉得内容中讲历史金融哲学多余的都是生意人还不是企业家。 发布于 2015-05-14 2 条评论 感谢 收藏 • 没有帮助 • • 作者保留权利 徐文瑞，计蒜客 / 产品经理 / 天蝎座的 INTJ 李少鹏、西西豆豆、知乎用户 等人赞同 作者都快被捧成神了，他的书会火也是正','url':'http://localhost:8000/articles'},
				{'user_avatar':'./static/image/php.jpg','user_name':'helloforworld','post_at':'2016/04/02','title':'Linux Container','description':'多‘正确的废话’，那么这本书为啥能让如此多牛逼机构牛逼大神推荐，让心神创业的骚年们不断高潮呢？ 2 条评论 按投票排序 按时间排序 18 个回答 知乎用户，苦逼的产品设计和运营佬 知乎用户、南鹏、Syan 等人赞同 看不懂的是小白，觉得作用不大的还处于给别人打工的状态，感觉通透的都是对趋势有感觉的，觉得内容中讲历史金融哲学多余的都是生意人还不是企业家。 发布于 2015-05-14 2 条评论 感谢 收藏 • 没有帮助 • • 作者保留权利 徐文瑞，计蒜客 / 产品经理 / 天蝎座的 INTJ 李少鹏、西西豆豆、知乎用户 等人赞同 作者都快被捧成神了，他的书会火也是正','url':'http://localhost:8000/articles'},
				{'user_avatar':'./static/image/c-cplusplus.jpg','user_name':'helloforworld','post_at':'2016/04/02','title':'Linux Container','description':'多‘正确的废话’，那么这本书为啥能让如此多牛逼机构牛逼大神推荐，让心神创业的骚年们不断高潮呢？ 2 条评论 按投票排序 按时间排序 18 个回答 知乎用户，苦逼的产品设计和运营佬 知乎用户、南鹏、Syan 等人赞同 看不懂的是小白，觉得作用不大的还处于给别人打工的状态，感觉通透的都是对趋势有感觉的，觉得内容中讲历史金融哲学多余的都是生意人还不是企业家。 发布于 2015-05-14 2 条评论 感谢 收藏 • 没有帮助 • • 作者保留权利 徐文瑞，计蒜客 / 产品经理 / 天蝎座的 INTJ 李少鹏、西西豆豆、知乎用户 等人赞同 作者都快被捧成神了，他的书会火也是正','url':'http://localhost:8000/articles'},
				{'user_avatar':'./static/image/git.png','user_name':'helloforworld','post_at':'2016/04/02','title':'Linux Container','description':'多‘正确的废话’，那么这本书为啥能让如此多牛逼机构牛逼大神推荐，让心神创业的骚年们不断高潮呢？ 2 条评论 按投票排序 按时间排序 18 个回答 知乎用户，苦逼的产品设计和运营佬 知乎用户、南鹏、Syan 等人赞同 看不懂的是小白，觉得作用不大的还处于给别人打工的状态，感觉通透的都是对趋势有感觉的，觉得内容中讲历史金融哲学多余的都是生意人还不是企业家。 发布于 2015-05-14 2 条评论 感谢 收藏 • 没有帮助 • • 作者保留权利 徐文瑞，计蒜客 / 产品经理 / 天蝎座的 INTJ 李少鹏、西西豆豆、知乎用户 等人赞同 作者都快被捧成神了，他的书会火也是正','url':'http://localhost:8000/articles'},
				];
				load_user_activity_item(data);
			}
		});
	}
	user_avatar_change_note();
	scroll_event();
})