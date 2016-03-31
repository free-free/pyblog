$(function(){
		$(window).resize(function(){
			var top=parseInt($(document).height())/2-parseInt($('.login-panel').height())/2;
			var left=parseInt($(document).width())/2-parseInt($('.login-panel').width())/2;
			if(parseInt(top)<60)
			{
				top=60;
			}
			$('.login-main-container').css({
					'position':'absolute',
					'top':top+'px',
					'left':left+'px'
					});	
			$('.login-main-container').fadeIn(1200);
		});
		$(window).resize();
		$('.all-input').focus(function(){
				$(this).css({
					'boxShadow':'0 0 5px #1bbcf2'
				});
				if($(this).prop('name')=='password')
				{
					$('.pwd-error-note').hide();
				}
				if($(this).prop('name')=='email'){
					$('.email-error-note').hide();	
				}
		})
		$('.all-input').blur(function(){
				$(this).css({
					'boxShadow':''
				})
				
		});
		function create_error_note(parentname,childname,top,left,msg)
		{
				var note=document.createElement('div');
						var span=document.createElement('span');
						$(span).css({
							'width':'0px',
							'height':'0px',
							'position':'absolute',
							'left':'10px',
							'top':'-10px',
							'border':'5px solid transparent',
							'border-bottom':'5px solid #ff9900',
						});
						$(note).css({
							'height':'35px',
							'lineHeight':'35px',
							'position':'absolute',
							'width':'200px',
							'top':top+'px',
							'left':left+'px',
							'paddingLeft':'10px',
							'background':'#ff9900',
							'zIndex':99999999,
							'color':'#fff',
							'letterSpacing':'0px',
							'boxShadow':'0 0 5px #ff9900'
						}).text(msg);
						$(note).addClass(childname);
						$(note).append(span);
						$(parentname).append(note);			
		}
		$('.email-input').blur(function(){
			reg=/^[\w][\w\.]+@[\w]+(\.[\w]+)+/
			if(!reg.test($(this).val()))
			{
				if($('.email-error-note').length==0)
				{
					create_error_note('.email-box','email-error-note',45,300,'邮箱格式不正确');
				}else{
					$('.email-error-note').show();
				}
				$(this).attr('id',0);
				return ;
			}
			$(this).attr('id',1);
		});
		$('.pwd-input').blur(function(){
			var pwd=$(this).val();
			if(pwd.length<6){
				if($('.pwd-error-note').length==0)
				{
					create_error_note('.pwd-box','pwd-error-note',45,300,'密码少于六位数');
				}
				else
				{
					$('.pwd-error-note').show();
				}
				$(this).attr('id',0);
				return ;
			}
			$(this).attr('id',1);
		});
		$('.login-form').submit(function(){
			$('.pwd-input').blur();
			$('.email-input').blur();
			if(parseInt($('.pwd-input').attr('id'))==0||parseInt($('.email-input').attr('id'))==0)
			{
				console.log('false');
				return false;
			}
			else
			{
				return true;	
			}
			
		});
		$('.login-btn').click(function(){
			$('.login-form').submit();
		})
		

})
