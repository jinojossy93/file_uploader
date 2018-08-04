# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.views.generic import View
from django.core.files.uploadhandler import FileUploadHandler
from django.core.cache import cache


# Create your views here.
class ServeFiles(View):
    def get(self, request, *args, **kwargs):
        print request.GET, args, kwargs
        print request.__dict__
        return render("index.html")

    def post(self, request):
        progress_id = ''
        if 'X-Progress-ID' in request.GET:
            progress_id = request.GET['X-Progress-ID']
        elif 'X-Progress-ID' in request.META:
            progress_id = request.META['X-Progress-ID']
        if progress_id:
            from django.utils import simplejson
            cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
            data = cache.get(cache_key)
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')



class UploadProgressCachedHandler(FileUploadHandler):
    """
    Tracks progress for file uploads.
    The http post request must contain a header or query parameter, 'X-Progress-ID'
    which should contain a unique string to identify the upload to be tracked.
    """

    def __init__(self, request=None):
        super(UploadProgressCachedHandler, self).__init__(request)
        self.progress_id = None
        self.cache_key = None

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        self.content_length = content_length
        if 'X-Progress-ID' in self.request.GET:
            self.progress_id = self.request.GET['X-Progress-ID']
        elif 'X-Progress-ID' in self.request.META:
            self.progress_id = self.request.META['X-Progress-ID']
        if self.progress_id:
            self.cache_key = "%s_%s" % (self.request.META['REMOTE_ADDR'], self.progress_id)
            cache.set(self.cache_key, {
                'length': self.content_length,
                'uploaded': 0
            })

    def new_file(self, field_name, file_name, content_type, content_length, charset=None):
        pass

    def receive_data_chunk(self, raw_data, start):
        if self.cache_key:
            data = cache.get(self.cache_key)
            data['uploaded'] += self.chunk_size
            cache.set(self.cache_key, data)
        return raw_data

    def file_complete(self, file_size):
        pass

    def upload_complete(self):
        if self.cache_key:
            cache.delete(self.cache_key)
