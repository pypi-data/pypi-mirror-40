from django.conf.urls import url

import directory_proxy.views


urlpatterns = [
    url(
        r'^(?P<path>.*)$',
        directory_proxy.views.ProxyView.as_view(),
    )
]
