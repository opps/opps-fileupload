# coding: utf-8

from opps.images.models import Image
from opps.articles.models import ArticleImage
from django.views.generic import CreateView, DeleteView

from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.urlresolvers import reverse

from django.conf import settings


def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"


class ImageCreateView(CreateView):
    model = Image
    template_name = 'fileupload/image_form.html'

    def form_valid(self, form):
        self.object = form.save()
        f = self.request.FILES.get('file')
        data = [{'name': f.name,
                 'url': settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"),
                 'thumbnail_url': settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"),
                 'delete_url': '',
                 'delete_type': "DELETE"}]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def get_context_data(self, **kwargs):
        context = super(ImageCreateView, self).get_context_data(**kwargs)
        # context['pictures'] = []Image.objects.all()
        context['pictures'] = []
        return context


# class PictureDeleteView(DeleteView):
#     model = Image

#     def delete(self, request, *args, **kwargs):
#         """
#         This does not actually delete the file, only the database record.  But
#         that is easy to implement.
#         """
#         self.object = self.get_object()
#         self.object.delete()
#         if request.is_ajax():
#             response = JSONResponse(True, {}, response_mimetype(self.request))
#             response['Content-Disposition'] = 'inline; filename=files.json'
#             return response
#         else:
#             return HttpResponseRedirect('/upload/new')


class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self, obj='', json_opts={}, mimetype="application/json",
                 *args, **kwargs):
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)
