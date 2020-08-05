import markdown
from django.db import models
from mdx_gfm import GithubFlavoredMarkdownExtension
from core.models import User

class AdminArticleManager(models.Manager):
  def get_queryset(self):
    return super().get_queryset()

class PublicArticleManager(models.Manager):
  def get_queryset(self):
    return super().get_queryset().filter(private=False)

  def private_articles(self, user):
    return super().get_queryset().filter(
      models.Q(private=False) | models.Q(private=True, by=user))

  def get(self, user, **kwargs):
    return self.private_articles(user).get(**kwargs)


class Article(models.Model):
  path = models.CharField(max_length=512)
  body = models.TextField(blank=True)
  markdown_body = models.TextField(blank=True)
  private = models.BooleanField(default=False)
  by = models.ForeignKey(User, related_name='articles', on_delete=models.SET_NULL, null=True)

  objects = AdminArticleManager()
  public_objects = PublicArticleManager()

  def save(self):
    self.body = markdown.markdown(
        self.markdown_body, extensions=[GithubFlavoredMarkdownExtension()])
    return super().save()

  def __str__(self):
    return '{} - {}'.format(self.path[0:30], self.body[0:30])
