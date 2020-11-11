from django.urls import reverse_lazy
from django.views.generic import DeleteView

from applications.blog.models import Post


class DeletePostView(DeleteView):
    model = Post
    success_url = reverse_lazy("blog:index")
