# coding: utf-8

from opps.images.models import Image
from opps.articles.models import Album, ArticleImage
from django.views.generic import CreateView

from django.http import HttpResponse
from django.utils import simplejson


def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"


class ImageCreateView(CreateView):
    model = Image
    template_name = 'fileupload/image_form.html'

    def form_valid(self, form):
        f = self.request.FILES.get('image')
        self.object = form.save()
        print self.kwargs.get('album_pk')

        data = [{'name': f.name,
                 'url': "%s" % self.object.image.url,
                 'thumbnail_url': "%s" % self.object.image.url,
                 "delete_url": "",
                 "delete_type": "DELETE"}]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def get_context_data(self, **kwargs):
        context = super(ImageCreateView, self).get_context_data(**kwargs)
        # context['pictures'] = []Image.objects.all()
        album_pk = self.kwargs.get('album_pk')
        try:
            context['album'] = Album.objets.get(pk=int(album_pk))
        except:
            context['album'] = None
        return context


class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self, obj='', json_opts={}, mimetype="application/json",
                 *args, **kwargs):
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)
