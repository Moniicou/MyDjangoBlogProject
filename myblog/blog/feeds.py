from django.contrib.syndication.views import Feed

from .models import Post


# 定义rss订阅的feed
class ALLPostFeed(Feed):
    # title表示我们的feed在聚合阅读器上显示的标题
    title = '千峰博客'

    # link表示要跳转的连接
    link = '/blog/index/'

    # 描述信息
    description = '千峰博客rss订阅'

    # 需要显示的条目
    def items(self):
        return Post.objects.all()

    # 显示的条目的标题
    def item_title(self, item):
        return '[%s]%s' % (item.category, item.title)

    # 条目的内容描述
    def item_description(self, item):
        return item.content

