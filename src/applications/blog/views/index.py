from django.views.generic import ListView

from applications.blog.models import Post


class IndexView(ListView):
    queryset = Post.objects.filter(visible=True)
    template_name = "blog/index.html"
