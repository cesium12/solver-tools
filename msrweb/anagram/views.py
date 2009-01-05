# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from anagram import AnagramDict, AnagramWord
from django import forms

dictfile = '/usr/share/dict/words'
min_letters = 2
max_letters = 80
adict = AnagramDict.new_from_file(dictfile, min_letters, max_letters)

class AnagramForm(forms.Form):
    word = forms.CharField()
    mode = forms.ChoiceField(choices=[(0,'Find words'),(1,'Find phrases')])

def main_index(request):
    return render_to_response('index.html', {})

def anag_index(request):
    if 'word' in request.GET:
        form = AnagramForm(request.GET)
        if form.is_valid():
            word = form.cleaned_data['word']
            mode = form.cleaned_data['mode']
            if mode =='1':
                return HttpResponseRedirect('/anagram/%s/phrases'%word)
            else:
                return HttpResponseRedirect('/anagram/%s/'%word)
        else:
            raise Exception()
    else:
        form = AnagramForm()
        return render_to_response('anag_form.html', {'form':form})

def anag_words(request,word):
    return render_to_response('anag_list.html', 
                              {'word' : word,
                               'results' : adict.find_words(word)})

def anag_phrases(request,word):
    return render_to_response('anag_list.html', 
                              {'word' : word,
                               'results' : adict.find_phrases(word)})

