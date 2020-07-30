import markdown
from django.db import models
from mdx_gfm import GithubFlavoredMarkdownExtension


class Article(models.Model):
  path = models.CharField(max_length=512)
  body = models.TextField(blank=True)
  markdown_body = models.TextField(blank=True)

  def save(self):
    self.body = markdown.markdown(
        self.markdown_body, extensions=[GithubFlavoredMarkdownExtension()])
    return super().save()

  def __str__(self):
    return '{} - {}'.format(self.path[0:30], self.body[0:30])
