from django.conf.urls import patterns
from .views import image_create

urlpatterns = patterns(
    '',
    (r'^image/(?P<article_pk>\d+)/$', image_create, {}, 'upload-new'),
    (r'^image/$', image_create, {}, 'upload-new-images'),
    # (r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), {}, 'upload-delete'),
)
