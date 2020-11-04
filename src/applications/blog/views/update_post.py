from django.urls import reverse_lazy
from django.views.generic import UpdateView

from applications.blog.models import Post


class UpdatePostView(UpdateView):
    fields = [Post.title.field.name, Post.content.field.name]
    model = Post
    success_url = reverse_lazy("blog:index")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx.update(
            {
                "action_name": "Update Post",
                "action_url": reverse_lazy(
                    "blog:update-post",
                    kwargs={
                        "pk": self.object.pk,
                    },
                ),
            }
        )

        return ctx
