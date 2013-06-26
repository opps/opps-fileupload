# coding: utf-8
import random

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.text import slugify

from opps.images.models import Image
from opps.articles.models import Article, ArticleImage
from opps.sources.models import Source
from opps.images.generate import image_url


def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"


@csrf_exempt
def image_create(request, article_pk):

    article = get_object_or_404(Article, pk=int(article_pk))

    if request.method == "POST":
        f = request.FILES.get('image')

        title = request.POST.get('title') or article.title
        caption = request.POST.get('caption', '')

        source = request.POST.get('source', None)
        if source:
            qs = Source.objects.filter(name=source, site=article.site)
            if qs:
                source = qs[0]
            else:
                source = Source.objects.create(
                    name=source,
                    slug=slugify(source),
                    published=True
                )

        slug = slugify(title)
        slug = "{0}-{1}".format(slug, random.getrandbits(32))

        instance = Image(
            site=article.site,
            user=article.user,
            date_available=article.date_available,
            title=title,
            slug=slug,
            image=f,
            published=True,
        )
        if source:
            instance.source = source

        instance.save()

        order = request.POST.get('order', 0)
        ArticleImage.objects.create(
            article=article,
            image=instance,
            caption=caption,
            order=int(order)
        )

        data = [{'name': f.name,
                 'url': "%s" % instance.image.url,
                 'thumbnail_url': "%s" % image_url(
                     instance.image.url,
                     width=60,
                     height=60
                 ),
                 "delete_url": "",
                 "delete_type": "DELETE"}]
        response = JSONResponse(data, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    else:
        return render(request, 'fileupload/image_form.html',
                      {'article': article})


class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self, obj='', json_opts={}, mimetype="application/json",
                 *args, **kwargs):
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)
