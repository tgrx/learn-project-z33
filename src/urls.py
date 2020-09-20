from framework import static
from views import hello
from views import index
from views import theme

urlpatterns = {
    "/": index.index,
    "/hello-reset/": hello.reset,
    "/hello-update/": hello.update,
    "/hello/": hello.index,
    "/i/": static.handle_static_from_prefix("images"),
    "/s/": static.handle_static_from_prefix("styles"),
    "/theme/": theme.switch,
}
