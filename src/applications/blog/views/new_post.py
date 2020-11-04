from django.urls import reverse_lazy
from django.views.generic import CreateView

from applications.blog.models import Post


class NewPostView(CreateView):
    model = Post
    fields = "__all__"
    success_url = reverse_lazy("blog:index")
