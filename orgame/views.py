# -*- coding: utf-8 -*-
from django.shortcuts import render


def main(request):
    return render(request, 'index.html')


def handler404(request):
    return render(request, '404.html')