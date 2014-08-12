##一个图片爬虫工具：cjyfffImgGeter
   
   
####2014.08.10更新：
初始v0.1版本，实现基础功能   
   
###依赖：
python 2.7   
   
###综述：
这是一个图片爬虫工具。由于部分网站采用了异步的方式加载图片链接（例如百度贴吧的相册），导致单靠分析目标url无法解释出图片的链接。针对这种情况，本程序可以选则输入html文件。对于采用异步方式加载图片链接的网站，我们可以用fiddler或firebug之类的工具保存完整的html文件然后输入到本程序。   
本程序默认开启4个线程来下载，可以修改代码中的MAX_THREADING来制定线程数。   
   
###使用说明：
1、可以以对话框的形式输入参数，也可以通过在settings.py文件中指定输入的参数。   
2、额。。。具体输入的内容含义请看输入的提示信息和settings.py的注释吧，已经写的比较清楚，不想重复写一次了。   
   
###后续目标：
使这个程序能用在更多不同的网站上，并且更加容易使用。   
   
