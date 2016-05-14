<?php

$d=[];
if(!empty($_POST))
{
	if($_POST['rtype']==1)
	{
		$d=[
			'code'=>200,
			'msg'=>'ok',
			'type'=>1,
			'data'=>[
				['cate_name'=>'Linux','cate_image'=>'http://localhost/linux.jpg'],
				['cate_name'=>'Git','cate_image'=>'http://localhost/git.png'],
				['cate_name'=>'PHP','cate_image'=>'http://localhost/php.jpg'],
				['cate_name'=>'Java','cate_image'=>'http://localhost/java.jpg'],
				['cate_name'=>'C/C++','cate_image'=>'http://localhost/c-cplusplus.jpg'],
				['cate_name'=>'Life','cate_image'=>'http://localhost/life.jpg'],
				['cate_name'=>'Python','cate_image'=>'http://localhost/python.jpg'],
			]
		];		
	}
	else if ($_POST['rtype']==2)
	{
			$d=[
				'code'=>200,
				'msg'=>'ok',
				'type'=>2,
				'data'=>[
				['article_title'=>'Linux contaier','article_desc'=>'最佳答案: Sublime Text3使用技巧教程 1 Sublime用的比较多的版本是Text2和Text3,这些网上都可以下载,汉化的也是有的,小编使用的是Text3中文版,安装好后,右击...zhidao.baidu.com/linSublime Text 有哪些使用技巧? - Sublime Text - 知乎','article_category'=>'linux','article_post_date'=>'2016/02/12','article_read_num'=>21,'article_url'=>'http://localhost/article-show.html'],
				['article_title'=>'Linux contaier','article_desc'=>'最佳答案: Sublime Text3使用技巧教程 1 Sublime用的比较多的版本是Text2和Text3,这些网上都可以下载,汉化的也是有的,小编使用的是Text3中文版,安装好后,右击...zhidao.baidu.com/linSublime Text 有哪些使用技巧? - Sublime Text - 知乎','article_category'=>'linux','article_post_date'=>'2016/02/12','article_read_num'=>21,'article_url'=>'http://localhost/article-show.html'],
				['article_title'=>'Linux contaier','article_desc'=>'最佳答案: Sublime Text3使用技巧教程 1 Sublime用的比较多的版本是Text2和Text3,这些网上都可以下载,汉化的也是有的,小编使用的是Text3中文版,安装好后,右击...zhidao.baidu.com/linSublime Text 有哪些使用技巧? - Sublime Text - 知乎','article_category'=>'linux','article_post_date'=>'2016/02/12','article_read_num'=>21,'article_url'=>'http://localhost/article-show.html'],
				['article_title'=>'Linux contaier','article_desc'=>'最佳答案: Sublime Text3使用技巧教程 1 Sublime用的比较多的版本是Text2和Text3,这些网上都可以下载,汉化的也是有的,小编使用的是Text3中文版,安装好后,右击...zhidao.baidu.com/linSublime Text 有哪些使用技巧? - Sublime Text - 知乎','article_category'=>'linux','article_post_date'=>'2016/02/12','article_read_num'=>21,'article_url'=>'http://localhost/article-show.html'],
				['article_title'=>'Linux contaier','article_desc'=>'最佳答案: Sublime Text3使用技巧教程 1 Sublime用的比较多的版本是Text2和Text3,这些网上都可以下载,汉化的也是有的,小编使用的是Text3中文版,安装好后,右击...zhidao.baidu.com/linSublime Text 有哪些使用技巧? - Sublime Text - 知乎','article_category'=>'linux','article_post_date'=>'2016/02/12','article_read_num'=>21,'article_url'=>'http://localhost/article-show.html'],
				['article_title'=>'Linux contaier','article_desc'=>'最佳答案: Sublime Text3使用技巧教程 1 Sublime用的比较多的版本是Text2和Text3,这些网上都可以下载,汉化的也是有的,小编使用的是Text3中文版,安装好后,右击...zhidao.baidu.com/linSublime Text 有哪些使用技巧? - Sublime Text - 知乎','article_category'=>'linux','article_post_date'=>'2016/02/12','article_read_num'=>21,'article_url'=>'http://localhost/article-show.html'],
				]
			];

	}
	else if($_POST['rtype']==3)
	{
			$d=[
				'code'=>200,
				'msg'=>'ok',
				'type'=>3,
				'data'=>[
					'date'=>['2016/03/12','2016/03/13','2016/03/14','2016/03/15','2016/03/16','2016/03/17'],
					'post_data'=>[
						[['is_post'=>false],['is_post'=>true,'article_title'=>'Linux container'],['is_post'=>false],['is_post'=>false],['is_post'=>false],['is_post'=>false]],
						[['is_post'=>true,'article_title'=>'Github and Git'],['is_post'=>false],['is_post'=>false],['is_post'=>false],['is_post'=>false],['is_post'=>false]],
						[['is_post'=>false],['is_post'=>false],['is_post'=>false],['is_post'=>false],['is_post'=>false],['is_post'=>false]],
						[['is_post'=>false],['is_post'=>false],['is_post'=>false],['is_post'=>false],['is_post'=>false],['is_post'=>false]],
						[['is_post'=>false],['is_post'=>false],['is_post'=>false],['is_post'=>false],['is_post'=>false],['is_post'=>false]],
						[['is_post'=>false],['is_post'=>false],['is_post'=>false],['is_post'=>true,'article_title'=>'the value of my life'],['is_post'=>false],['is_post'=>false]],
						[['is_post'=>false],['is_post'=>false],['is_post'=>false],['is_post'=>true,'article_title'=>'python io模型'],['is_post'=>false],['is_post'=>false]],
					]
				]
			];
	}
	else
	{
			$d=[
			  'code'=>300,
			  [[],[],[],[],[],[]],
			  [[],[],[],[],[],[]],
			  'msg'=>'bad request',
			  'type'=>'',
			  'data'=>'',
			];
	}
}
else
{
	$d=[
	'code'=>300,
	'msg'=>'not allowed request method',
	'type'=>'',
	'data'=>'',
	];
}
echo json_encode($d);
/* article category list*/
/*	$d=[
	'code'=>200,
	'msg'=>'ok',
	'type'=>1,
	'data'=>[
		['cate_name'=>'Linux','cate_image'=>'http://localhost/linux.jpg'],
		['cate_name'=>'Git','cate_image'=>'http://localhost/git.png'],
		['cate_name'=>'PHP','cate_image'=>'http://localhost/php.jpg'],
		['cate_name'=>'Java','cate_image'=>'http://localhost/java.jpg'],
		['cate_name'=>'C/C++','cate_image'=>'http://localhost/c-cplusplus.jpg'],
		['cate_name'=>'Life','cate_image'=>'http://localhost/life.jpg'],
		['cate_name'=>'Python','cate_image'=>'http://localhost/python.jpg'],
	]
	];		*/

/* article list*/
/*$d=[
	'code'=>200,
	'msg'=>'ok',
	'type'=>2,
	'data'=>[
	['article_title'=>'Linux contaier','article_desc'=>'最佳答案: Sublime Text3使用技巧教程 1 Sublime用的比较多的版本是Text2和Text3,这些网上都可以下载,汉化的也是有的,小编使用的是Text3中文版,安装好后,右击...zhidao.baidu.com/linSublime Text 有哪些使用技巧? - Sublime Text - 知乎','article_category'=>'linux','article_post_date'=>'2016/02/12','article_read_num'=>21,'article_url'=>'http://localhost/article-show.html'],
	['article_title'=>'Linux contaier','article_desc'=>'最佳答案: Sublime Text3使用技巧教程 1 Sublime用的比较多的版本是Text2和Text3,这些网上都可以下载,汉化的也是有的,小编使用的是Text3中文版,安装好后,右击...zhidao.baidu.com/linSublime Text 有哪些使用技巧? - Sublime Text - 知乎','article_category'=>'linux','article_post_date'=>'2016/02/12','article_read_num'=>21,'article_url'=>'http://localhost/article-show.html'],
	['article_title'=>'Linux contaier','article_desc'=>'最佳答案: Sublime Text3使用技巧教程 1 Sublime用的比较多的版本是Text2和Text3,这些网上都可以下载,汉化的也是有的,小编使用的是Text3中文版,安装好后,右击...zhidao.baidu.com/linSublime Text 有哪些使用技巧? - Sublime Text - 知乎','article_category'=>'linux','article_post_date'=>'2016/02/12','article_read_num'=>21,'article_url'=>'http://localhost/article-show.html'],
	['article_title'=>'Linux contaier','article_desc'=>'最佳答案: Sublime Text3使用技巧教程 1 Sublime用的比较多的版本是Text2和Text3,这些网上都可以下载,汉化的也是有的,小编使用的是Text3中文版,安装好后,右击...zhidao.baidu.com/linSublime Text 有哪些使用技巧? - Sublime Text - 知乎','article_category'=>'linux','article_post_date'=>'2016/02/12','article_read_num'=>21,'article_url'=>'http://localhost/article-show.html'],
	['article_title'=>'Linux contaier','article_desc'=>'最佳答案: Sublime Text3使用技巧教程 1 Sublime用的比较多的版本是Text2和Text3,这些网上都可以下载,汉化的也是有的,小编使用的是Text3中文版,安装好后,右击...zhidao.baidu.com/linSublime Text 有哪些使用技巧? - Sublime Text - 知乎','article_category'=>'linux','article_post_date'=>'2016/02/12','article_read_num'=>21,'article_url'=>'http://localhost/article-show.html'],
	['article_title'=>'Linux contaier','article_desc'=>'最佳答案: Sublime Text3使用技巧教程 1 Sublime用的比较多的版本是Text2和Text3,这些网上都可以下载,汉化的也是有的,小编使用的是Text3中文版,安装好后,右击...zhidao.baidu.com/linSublime Text 有哪些使用技巧? - Sublime Text - 知乎','article_category'=>'linux','article_post_date'=>'2016/02/12','article_read_num'=>21,'article_url'=>'http://localhost/article-show.html'],
	]
];*/




?>