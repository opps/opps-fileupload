from django.conf.urls import patterns
from .views import ImageCreateView

urlpatterns = patterns(
    '',
    (r'^new/$', ImageCreateView.as_view(), {}, 'upload-new'),
    # (r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), {}, 'upload-delete'),
)
