$(function(){
	$(document).dblclick(function(){
		$('.dropdown-menu').removeClass('active').hide();
	});
	$('.nb-user-dropdown').click(function(){
		if($('.dropdown-menu').length==0)
		{
		    var dropMenu=document.createElement('ul')
		    $(dropMenu).addClass("dropdown-menu")
		    /*.click(function(e){
		    	$('.dropdown-menu').removeClass('active').hide();
		    	var loginPanel=$('.login-panel');
		    	var backmuck=document.createElement('div')
		    	$(backmuck).css({
		    		'background':'#000',
		    		'opacity':0.5,
		    		'position':'fixed',
		    		'top':'0px',
		    		'left':'0px',
		    		'height':'100%',
		    		'width':'100%',
		    		'zIndex':999999
		    	}).addClass('backmuck');
		    	$(loginPanel).css({
		    			'position':'fixed',
		    			'top':parseInt($(document).scrollTop())+document.documentElement.clientHeight/2-125+'px',
		    			'left':parseInt($(document).width())/2-200+'px',
		    			'background':'#f5f5f5',
		    			'opacity':1,
		    			'zIndex':99999999
		    	}).addClass('loginPanel');
		    	$('body').append(backmuck).append(loginPanel);
		    })
			*/	
			$(dropMenu).append('<li><a href="#" class="avatar"><img class="avatar-img" src="avatar.jpeg"/></a></li>');
			$(dropMenu).append('<li><a href="#" class="avatar">Whoami\'s Blog</a></li>');
		    $(dropMenu).append('<li><a  href="signin.html"><span class="addon"><i class="icon-signin"></i></span>登录</a></li>');
		    $(dropMenu).append('<li><a class="item-link" href="https://github.com/free-free/" target="_blank"><span class="addon"><i class="icon-github-alt"></i></span>Github</a><a class="item-link" href="https://twitter.com" target="_blank"><span class="addon"><i class="icon-twitter-sign"></i></span>Twitter</a></li>');
		    $(dropMenu).append('<li><a class="item-link" href="https://www.facebook.com" target="_blank" t><span class="addon"><i class="icon-facebook-sign"></i></span>facebook</a><a class="item-link" href="#" target="_blank" t><span class="addon"><i class="icon-google-plus-sign"></i></span>Google+</a></li>');
		    $(dropMenu).append('<li><a class="item-link" href="http://weibo.com/5577495302/profile?topnav=1&wvr=6" target="_blank" t><span class="addon"><i class="icon-spinner"></i></span>weibo</a></li>');
			var span=document.createElement("span");
			$(span).css({
				'display':'inlineBlock',
				'width':'0px',
				'height':'0px',
				'position':'absolute',
				'border':'7px solid transparent',
				'borderBottom':'7px solid #fff',
				'top':'-14px',
				'left':'30px'
			})
			$(dropMenu).append(span);
			$(dropMenu).find('a').css('color','#333');
			$(dropMenu).css({
				'zIndex':99999,
				'position':'absolute',
				'top':'35px',
				'background':'#f5f5f5',
				'fontSize':'14px',
				'boxShadow':'0 0 5px #333',
			});
			$(dropMenu).find('li').css({
				'width':'200px',
				'margin':'0px',
				'padding':'0px',
			});
			$(dropMenu).find('.item-link').css({
				'display':'block',
				'textAlign':'left',
				'float':'left',
				'color':'#999',
				'width':'85px',
				'marginLeft':'10px',
				'height':'30px',
				'lineHeight':'30px',
				'letterSpacing':'0px',
				'overflow':'hidden'
			}).hover(function(){
				$(dropMenu).find('.item-link').css({'color':'#999','background':'#f5f5f5'});
				$(this).css({
					'color':'#333'
				});
			}).mouseleave(function(){
				$(this).css('color','#999');
			}).find('.addon').css({
				'lineHeight':'30px',
				'height':'30px',
				'paddingLeft':'5px',
				'textAlign':'center',
				'display':'inlineBlock',
			})
			$(dropMenu).find('.avatar-img').css({
				'width':'200px',
				'margin':'0px',
				'padding':'0px',
				'height':'150px',
				'display':'block'
			});
			$('.nb-user-center').append(dropMenu)
		}
		/* if dropdown-menu exists,just hide it and show it*/
		if($('.dropdown-menu').hasClass('active'))
		{
			$('.dropdown-menu').removeClass('active').hide();
		}else
		{
			$('.dropdown-menu').find('.item-link').css({'color':'#999','background':'#f5f5f5'});
			$('.dropdown-menu').addClass('active').show();
		}
	});
})
