---
title: 学习xpath，使用lxml+xpath提取内容。
date: 2019-03-04 18:12:41
tags: []
categories: []
copyright: true
---
什么是 XPath?  
XPath即为XML路径语言（XML Path Language），它是一种用来确定XML文档中某部分位置的语言。  
在 XPath 中，有七种类型的节点：元素、属性、文本、命名空间、处理指令、注释以及文档（根）节点。XML 文档是被作为节点树来对待的。  
下面列出了最有用的路径表达式：  
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019030417442546.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L25hb25hbzc3,size_16,color_FFFFFF,t_70)  
参考链接： [ 用lxml解析HTML
](http://www.cnblogs.com/descusr/archive/2012/06/20/2557075.html)  
使用xpath提取丁香园论坛的回复内容。丁香园直通点 [ 晕厥待查——请教各位同仁
](http://www.dxy.cn/bbs/thread/626626#626626)  
用户名称：tree.xpath(’//div[@class=“auth”]/a/text()’)  
回复内容：tree.xpath(’//td[@class=“postbody”]’) 因为回复内容中有换行等标签，所以需要用string()来获取数据。  
**Xpath中text()，string()，data()的区别如下：**  
**text()仅仅返回所指元素的文本内容。  
string()函数会得到所指元素的所有节点文本内容，这些文本讲会被拼接成一个字符串。  
data()大多数时候，data()函数和string()函数通用，而且不建议经常使用data()函数，有数据表明，该函数会影响XPath的性能。 **  
整体代码如下：  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305114028829.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L25hb25hbzc3,size_16,color_FFFFFF,t_70)  
运行结果如下：  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305114059981.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L25hb25hbzc3,size_16,color_FFFFFF,t_70)

