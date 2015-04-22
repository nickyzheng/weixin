from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'weixin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^wx', 'wxapp.views.home'),
    url(r'^detail/(\d+)$', 'wxapp.views.clothes_detail'),
    url(r'^test/', 'wxapp.views.test'),
]
