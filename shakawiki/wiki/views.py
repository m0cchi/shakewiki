from core.views import BaseTemplateView
from django.shortcuts import redirect

from wiki.models import Article


class BaseWikiTemplateView(BaseTemplateView):
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context['menu'] = BaseWikiTemplateView.ulrized_tree(self.request.user)

    return context

  def render_to_response(self, context, response_kwargs={}):
    context = self.get_context_data(**context)

    return super().render_to_response(context, **response_kwargs)

  @classmethod
  def ulrized_tree(cls, user):
    if user.is_authenticated:
      queryset = Article.public_objects.private_articles(user)
    else:
      queryset = Article.public_objects.all()

    tree = BaseWikiTemplateView.make_tree(queryset)
    if 'path__/' not in tree:
      return '<ul><li>/</li></ul>'

    html = BaseWikiTemplateView.make_ul('/', tree['path__/'])
    return html

  @classmethod
  def make_ul(cls, name, branch):
    return '<ul>{}</ul>'.format(BaseWikiTemplateView.make_li(name, branch))

  @classmethod
  def make_li(cls, name, branch):
    html = '<li>'
    if 'page' in branch:
      html += '<a href="/article/{}/">{}</a>'.format(branch['page'], name)
    else:
      html += name

    paths = [p for p in branch.keys() if p != 'page']
    if len(paths) > 0:
      html += '<ul>'
    for path in paths:
      next_branch = branch[path]
      html += BaseWikiTemplateView.make_li(path[len('path__'):len(path)],
                                           next_branch)
    if len(paths) > 0:
      html += '</ul>'
    html += '</li>'
    return html

  @classmethod
  def make_tree(cls, queryset):
    pages = queryset.values('id', 'path')
    tree = {}
    for page in pages:
      page['path'] = [p + '/' for p in page['path'].split('/')]
      it = iter(page['path'])
      path = next(it)
      if 'path__' + path in tree:
        current = tree['path__' + path]
      else:
        current = {}
        tree['path__' + path] = current
      while True:
        try:
          path = next(it)
          if 'path__' + path in current:
            current = current['path__' + path]
          else:
            new_current = {}
            current['path__' + path] = new_current
            current = new_current

        except StopIteration:
          current['page'] = page['id']
          break

    return tree


class TopView(BaseWikiTemplateView):

  template_name = "wiki/top.html"

  def get(self, request, **kwargs):
    context = {}
    context['articles'] = Article.public_objects.all().order_by('-updated').values('id', 'path', 'updated')[:30]
    return self.render_to_response(context)


class ArticleView(BaseWikiTemplateView):

  template_name = "wiki/article.html"

  def get(self, request, article_id, **kwargs):
    context = {}
    try:
      article = Article.public_objects.get(request.user, id=article_id)
      context['subtitle'] = article.path
      context['path'] = article.path
      context['body'] = article.body
    except Article.DoesNotExist:
      return redirect('/')
    return self.render_to_response(context)
