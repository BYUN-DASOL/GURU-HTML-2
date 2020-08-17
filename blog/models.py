from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

#글의 분류
class Category(models.Model):
    name = models.CharField(max_length=25, help_text="블로그 글의 분류를 입력하세요.(ex:한식)")
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/blog/category/{}/'.format(self.slug)

class Post(models.Model):
    # 블로그에서 제목을 의미, max_length로 글자 수 제한을 둠.
    title = models.CharField(max_length=30)
    # 글에 들어갈 내용, TextField는 장문의 글을 받아올 수 있음.
    content = MarkdownxField()

    head_image = models.ImageField(upload_to='%Y/%m/%d/', blank=True)

    # 언제 작성되었는지
    created = models.DateTimeField()

    # 누가 작성을 했는지, user라는 객체는 이미 django에서 제공. ForeignKey로 연결함.
    author = models.ForeignKey(User, on_delete=True)

    category = models.ForeignKey(Category, help_text="글의 분류를 설정하세요.", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    #1번 글의 경우 -> post/1
    def get_absolute_url(self):
        return '/blog/{}/'.format(self.pk)

    def get_markdown_content(self):
        return markdown(self.content)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)




