from django.shortcuts import redirect 
from .forms import DomainForm
from .models import Domain, Data
from .forms import UploadFileForm


# Create your views here.
def save_domain(request):
    if request.user.is_authenticated:
        form= DomainForm(request.POST or None)
        if form.is_valid():
            domain= form.cleaned_data.get("name")
            limit= form.cleaned_data.get("limit")
        try:
            domain_ = Domain(user=request.user, name=domain, limit=limit)
            domain_.save()
            request.session['success'] = 'Домен сохранён'
        except:
            request.session['success'] = 'Такой домен есть'
        request.session['success_count'] = 0
        return redirect('/start/?page=1')
    else:
        request.session['success'] = 'Не POST запрос'
        return redirect('/start/?page=1')


def uoload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            list_file = request.FILES.getlist('file')
            request.session['domain_list'] = []
            for file in list_file:

                file_ = file._name.split(".")[::-1]

                region = file_[1]

                while True:
                    if file_[0] == "organic":
                        file_.pop(0)
                        break
                    file_.pop(0)
                    
                domain_name = ".".join(file_[::-1])
                
                try:
                    domain = Domain.objects.get(user=request.user, name=domain_name)
                except:
                    if domain_name in request.session['domain_list']:
                        continue
                    request.session['domain_list'].append(domain_name)
                    request.session['domain_exist_count'] = 0
                    continue
                
                data = Data.objects.filter(user=request.user, domain=domain, region=region)
                if data:
                    data.delete()
                handle_uploaded_file(request.user, domain, region, file)
            return redirect('/start/?page=1')
    else:
        form = UploadFileForm()
    return redirect('/start/?page=1')


def handle_uploaded_file(user, domain, region, file):
    for id, el in enumerate(file):
        if not id:
            continue
        el = el.decode('unicode-escape').encode('latin1').decode('utf-8').split(';')
        
        int_position = el[2]
        if int_position[0] == '"':
            int_position = int(int_position[1:-1])
        else:
            int_position = int(int_position)

        if int_position <= 30:
            int_frequency = el[4]
            n_true = int_frequency[-1] == '\n'
            qav_true = int_frequency[0] == '"'

            if n_true and qav_true:
                int_frequency = int(int_frequency[1:-2])
            elif not n_true and qav_true:
                int_frequency = int(int_frequency[1:-1])
            else:
                int_frequency = int(int_frequency)
                
            data = Data(
                        user=user, 
                        domain=domain, 
                        query=el[0][1:-1], 
                        position=int_position, 
                        frequency=int_frequency, 
                        region=region
                        )
            data.save()

