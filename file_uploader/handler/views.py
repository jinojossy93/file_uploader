# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from handler.forms import FileForm
from handler.models import File


class ProgressBarUploadView(View):
    def get(self, request):
        file_list = File.objects.all()
        return render(self.request, 'index.html', {'files': file_list})

    def post(self, request):
        form = FileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            file = form.save()
            data = {'is_valid': True, 'name': file.file.name, 'url': file.file.url}
        else:
            data = {'is_valid': False}
        return HttpResponse(data)
