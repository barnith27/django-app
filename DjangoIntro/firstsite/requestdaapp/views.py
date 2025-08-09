from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render

from .forms import UserBioForm, UploadFileForm


# Create your views here.
def process_get_view(request: HttpRequest)-> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'b': b,
        'result': result,
    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)

def user_form(request: HttpRequest)-> HttpResponse:
    context = {
        'form': UserBioForm(),
    }
    return render(request, 'requestdataapp/user-bio-form.html', context=context)

def handle_file_upload(request: HttpRequest)-> HttpResponse:
    print('dfg')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            myfile = form.cleaned_data['file']
            file_size = myfile.size / 1024 / 1024
            if file_size < 1:
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                print('saved file', filename)
                return render(request, 'requestdataapp/file-upload.html')
            else:
                return HttpResponseForbidden("Файл слишком большой (максимум 1 МБ)")
    else:
        form = UploadFileForm()
    context = {
        'form': form,
        }
    return render(request, 'requestdataapp/file-upload.html', context=context)

