from django.http import HttpResponse as hr
from django.shortcuts import render

def index1(request):
    return render(request, 'index1.html')

def analyze(request):
    return hr("hello I am manav")

def removepunc(request):
    res = request.POST.get('text', 'default')
    rm = request.POST.get('rm', 'off')
    capital = request.POST.get('capital', 'off')

    if rm == 'on':
        punc = '''!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~'''
        purpose = 'Text after removing punctuations'
        text = ''
        for char in res:
            if char not in punc:
                text += char
        params = {'purpose': purpose, 'text': text}
        return render(request, 'show.html', params)

    elif capital == 'on':
        purpose = 'Capitalized Text'
        text = ''
        for char in res:
            text += char.upper()

        params = {'purpose': purpose, 'text': text}
        return render(request, 'show.html', params)

    else:
        return hr("error")