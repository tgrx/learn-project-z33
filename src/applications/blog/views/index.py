from django.views.generic import ListView

from applications.blog.models import Post


class IndexView(ListView):
    template_name = "blog/index.html"
    queryset = Post.objects.filter(visible=True)
