from django.urls import reverse_lazy
from django.views.generic import UpdateView

from applications.blog.models import Post


class UpdatePostView(UpdateView):
    fields = [Post.title.field.name, Post.content.field.name]
    model = Post
    success_url = reverse_lazy("blog:index")
    extra_context = {"action_name": "Update Post"}
