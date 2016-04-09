$(function(){
		
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
		$('#email').blur(function(){
			reg=/^[\w][\w\.]+@[\w]+(\.[\w]+)+/
			if(!reg.test($(this).val()))
			{
				if($('.email-error-note').length==0)
				{
					create_error_note('.email-box','email-error-note',45,280,'邮箱格式不正确');
				}else{
					$('.email-error-note').show();
				}
				$(this).removeClass("active");
				return ;
			}
			else
			{
				$('.email-error-note').hide();
				$(this).addClass("active");
			}
			
		});
		$('#password').blur(function(){
			var pwd=$(this).val();
			if(pwd.length<6){
				if($('.pwd-error-note').length==0)
				{
					create_error_note('.pwd-box','pwd-error-note',45,280,'密码少于六位数');
				}
				else
				{
					$('.pwd-error-note').show();
				}
				$(this).removeClass('active');
				return ;
			}
			else
			{
				$('.pwd-error-note').hide();
				$(this).addClass('active');
			}
			
		});
		$('.login-form').submit(function(){
			$('#password').blur();
			$('#email').blur();
			if($('#password').hasClass('active')&&$('#email').hasClass('active'))
			{
				return true;
			}
			else
			{
				return false;
			}		
		});
		$('.login-btn').click(function(){
			$('.login-form').submit();
		})
		

})
