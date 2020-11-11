from django.urls import reverse_lazy
from django.views.generic import CreateView

from applications.blog.models import Post


class NewPostView(CreateView):
    fields = "__all__"
    model = Post
    success_url = reverse_lazy("blog:index")
    extra_context = {
        "action_name": "Create Post",
        "action_url": reverse_lazy("blog:new-post"),
    }
