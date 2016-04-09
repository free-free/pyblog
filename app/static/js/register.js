$(function(){
	function dropdown_btn_click_handler()
	{
		if($(this).hasClass('active'))
		{
			$(this).css('color','#ababab').removeClass('active');
			$('.nb-user-dropdown-menu').hide();
			$('.nb-user-dropdown-menu-tangle').hide();
		}
		else
		{
			$(this).css('color','#fff').addClass('active');
			$('.nb-user-dropdown-menu').show();
			$('.nb-user-dropdown-menu-tangle').show();	
		}
	}
	function check_email(checkTarget,noteEle,noteInfo)
	{
		reg=/^[\w][\w\.]+@[\w]+(\.[\w]+)+/
		if(!reg.test($(checkTarget).val()))
		{
				$(noteEle).text(noteInfo);
				return -1
		}
		else
		{
				$(noteEle).text('');
				return 1;
		}
	}
	function check_password(checkTarget,noteEle,noteInfo,minLength)
	{
		minLength=minLength||6;
		if($(checkTarget).val().length<minLength)
		{
			$(noteEle).text(noteInfo);
			return -1;
		}
		else
		{
			$(noteEle).text('');
			return 1;	
		}
	}
	function check_null(checkTarget,noteEle,noteInfo)
	{
		if($(checkTarget).val().length<1)
		{
			$(noteEle).text(noteInfo);
			return -1;
		}
		else
		{
			$(noteEle).text('');
			return 1;
		}
	}
	function navagitar_bar_init(){
		$('.nb-user-dropdown-tangle-btn').click(dropdown_btn_click_handler);
		$(document).dblclick(function(){
			$('.nb-user-dropdown-tangle-btn').css('color','#ababab').removeClass('active');
			$('.nb-user-dropdown-menu').hide();
			$('.nb-user-dropdown-menu-tangle').hide();
		});	
	}
	function register_form_init(){
		$('#email').blur(function(){
			check_email("#email",'.email-error-note','邮箱格式不正确');
		});
		$('#password').blur(function(){
			check_password("#password",'.password-error-note','密码少于六位');
		});
		$("#user-name").blur(function(){
			check_null("#user-name",'.user-name-error-note','用户名不能为空');
		})
		$('.register-form').submit(function(){
			var emailValidate=check_email("#email",'.email-error-note','邮箱格式不正确');
			var pwdValidate=check_password("#password",'.password-error-note','密码少于六位');
			var nameValidate=check_null("#user-name",'.user-name-error-note','用户名不能为空');
			if(emailValidate==1&&pwdValidate==1&&nameValidate==1)
			{
				return true;
			}
			else
			{
				return false;
			}
		});
		$('.submit-btn').click(function(){
			$('.register-form').submit();
		});
	}
	navagitar_bar_init();
	register_form_init();

	
})	