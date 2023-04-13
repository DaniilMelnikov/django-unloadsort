from django.conf import settings
from django.shortcuts import render, redirect
from download_file.forms import DomainForm, UploadFileForm
from download_file.models import Domain, Data
from auth.forms import KeyXmlProxyForms
from django.core.paginator import Paginator
from .models import RegionModel, KeyXmlProxy

import csv
import requests
from random import shuffle
from bs4 import BeautifulSoup


def main(request):
    if request.user.is_authenticated:
        try:
            domain_delete = request.GET.get('domain')
            domain_filter = Domain.objects.filter(user=request.user, name=domain_delete)[0]
            
            if domain_filter:
                Data.objects.filter(user=request.user, domain=domain_filter).delete()
                domain_filter.delete()
                domain_delete = f'Домен {domain_delete} удалён'
            else:
                domain_delete = ''
        except:
            domain_delete = ''

        domains = Domain.objects.filter(user=request.user)

        pagination = Paginator(domains, 10)
        try:
            page_number = request.GET.get('page')
        except:
            page_number = 1

        num_prev = ''
        num_next = ''
        pagination = pagination.get_page(page_number)
        prev = pagination.has_previous()
        if prev:
            num_prev = pagination.previous_page_number()
        next = pagination.has_next()
        if next:
            num_next = pagination.next_page_number()

        form_domain = DomainForm()
        form_upload = UploadFileForm()
        form_xml = KeyXmlProxyForms()
        try:
            request.session['key_success']
            request.session['success_xml_count']

            request.session['success']
            request.session['success_count']
            

            request.session['error_xmlproxy']
            request.session['error_xmlproxy_count']

            request.session['success_result']
            request.session['success_result_count']
            
            request.session['file']
            request.session['file_count']
            
            request.session['domain_list']
            request.session['domain_exist_count']
        except KeyError:
            request.session['success_count'] = 0
            request.session['success_xml_count'] = 0
            request.session['error_xmlproxy_count'] = 0
            request.session['success_result_count'] = 0
            request.session['file_count'] = -5
            request.session['domain_exist_count'] = 0
            request.session['success'] = ''
            request.session['key_success'] = ''
            request.session['error_xmlproxy'] = ''
            request.session['success_result'] = ''
            request.session['file'] = ''
            request.session['domain_list'] = ''
        

        request.session['success'], request.session['success_count'] = current_session(
            request.session['success'], request.session['success_count']
            )
        request.session['key_success'], request.session['success_xml_count'] = current_session(
            request.session['key_success'], request.session['success_xml_count']
            )
        request.session['error_xmlproxy'], request.session['error_xmlproxy_count'] = current_session(
            request.session['error_xmlproxy'], request.session['error_xmlproxy_count']
            )
        request.session['success_result'], request.session['success_result_count'] = current_session(
            request.session['success_result'], request.session['success_result_count']
            )
        request.session['file'], request.session['file_count'] = current_session(
            request.session['file'], request.session['file_count']
            )
        request.session['domain_list'], request.session['domain_exist_count'] = current_session(
            request.session['domain_list'], request.session['domain_exist_count']
            )

        context = {
            'user': request.user,
            'form': form_domain,
            'form_upload': form_upload,
            'form_xml': form_xml,
            'save_domain': '',
            'domain_delete': domain_delete,
            'page': {
                'prev': prev,
                'num_prev': num_prev,
                'next': next,
                'num_next': num_next,
                'domains': pagination.object_list,
                'page_number': page_number
            }
        }

        return render(request, 'main.html', context)
    else:
        return redirect('/login/')


def current_session(session, count):
    if session and count < 1:
        count += 1
    else:
        count = 0
        session = ''
    return session, count


def add_xml_view(request):
    if request.method == 'POST':
        form = KeyXmlProxyForms(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            key = form.cleaned_data.get("key")
        try:
            KeyXmlProxy.objects.get(user=request.user)
            request.session['key_success'] = 'Такой ключ есть'
        except:
            KeyXML = KeyXmlProxy(user=request.user, email=email, key=key)
            KeyXML.save()
            request.session['key_success'] = 'Ключ сохранён'

        request.session['success_xml_count'] = 0
        return redirect('/start/?page=1')
    else:
        request.session['success_xml_count'] = 'Не POST запрос'
        return redirect('/start/?page=1')


def sort_unload_views(request):
    if request.user.is_authenticated:
        data_dict = select_data(request)
        data_dict = select_limit(data_dict, request)
        sort_list = select_result(data_dict, request)
        if not sort_list:
            return redirect('/start/?page=1')

        create_csv(sort_list, request)
        request.session['success_result'] = 'Успешно файл сформирован'
        request.session['success_result_count'] = 0
        return redirect('/start/?page=1')
    else:
        return redirect('/login/')


def select_data(request):
    data_dict = {}
    region_list = RegionModel.objects.all()
    domains_list = request.POST['domains'].split(';')

    for domain_name in domains_list:
        if domain_name:
            domain = Domain.objects.get(
                    user=request.user, 
                    name=domain_name,
                    )
            count = 0
            data_dict[domain_name] = {}

            for region in region_list:
                data = Data.objects.filter(
                    user=request.user, 
                    domain=domain, 
                    region=region.region
                    )
                    
                if data:
                    count += 1
                    data_dict[domain_name][region.region] = []

                    for el in data:
                        frequency = round(el.frequency/300)
                        if not frequency:
                            frequency = 1
                        data_dict[domain_name][region.region].append(
                            [el.query, frequency, f'&lr={region.number}']
                        )
                    shuffle(data_dict[domain_name][region.region])

            try:
                if count:
                    data_dict[domain_name]['count'] = count
                else:
                    del data_dict[domain_name]
            except KeyError:
                pass
        
    return data_dict


def select_limit(data_dict, request):
    for domain_name, dict in data_dict.items():
            counter = dict['count']
            list_limit = []
            if counter:
                domain = Domain.objects.get(
                    user=request.user, 
                    name=domain_name,
                    )
                domain.limit

                target_int = domain.limit / counter
                round_int = round(target_int)
                diff_int = target_int - round_int
                range_int = round(diff_int * counter)

                for int in range(counter):
                    list_limit.append(round_int)

                if range_int < 0:
                    range_int = range_int*(-1)
                    enum_element = -1
                else:
                    enum_element = 1

                for id in range(range_int):
                    list_limit[id] += enum_element

                shuffle(list_limit)

                data_dict[domain_name]['count'] = list_limit
    
    return data_dict


def select_result(data_dict, request):
    sort_list = []
    counter_id = 0
    for domain_name, dict in data_dict.items():
        id = 0
        for key, list in dict.items():
            if key == "count":
                continue
            counter_limit = 0
            key_xml = KeyXmlProxy.objects.get(user=request.user)
            for el in list:
                counter_cache = counter_limit

                try:
                    xml_data = request_xmlproxy(
                        query=el[0],
                        user=key_xml.email,
                        key=key_xml.key,
                        region=el[2]
                    ).decode('unicode-escape').encode('latin1').decode('utf-8')
                except:
                    continue
                    
                counter_id, counter_limit, sort_list, current = parser_xml(
                    counter_id=counter_id, 
                    counter_limit=counter_limit,
                    domain_=domain_name,
                    xml_data=xml_data,
                    row=el,
                    sort_list=sort_list
                )

                if counter_limit == data_dict[domain_name]['count'][id]:
                    break

                if counter_limit > data_dict[domain_name]['count'][id]:
                    counter_limit = counter_cache
                    continue

                if current:
                    print(current)
                    request.session['error_xmlproxy'] = current[0]
                    request.session['error_xmlproxy_count'] = 0
                    return 0
            id += 1

    return sort_list


def request_xmlproxy(query, user, key, region):
        """
        POST запрос на сервер xmlproxy.ru. Отправляем xml.
        Передаются имя юзера, токен ключ, которые введёте.
        """
        url = f'http://xmlproxy.ru/search/xml?user={user}&key={key}' + region

        headers = {'Content-Type': 'application/xml; charset=utf-8'}

        data = f'''<?xml version="1.0" encoding="UTF-8"?> 
            <request>   
                <query>{query}</query>
                <sortby>rlv</sortby>
                <maxpassages>0</maxpassages>
                <page>0</page> 
                <groupings>
                    <groupby attr="d" mode="deep" groups-on-page="30" docs-in-group="1" /> 
                </groupings>        
            </request>
            '''
        return requests.post(
            url=url, 
            data=data.encode('utf-8'), 
            headers=headers
            ).content


def parser_xml(counter_id, counter_limit, domain_, xml_data, row, sort_list):
        """
        Парсинг XML файла принятый из xmlproxy.ru. Ищем домен в первой 30.
        """
        soup = BeautifulSoup(xml_data, 'xml')
        error = soup.find_all('error')
        if error and error != None:
            return counter_id, counter_limit, sort_list, error[0].contents
        try:
            domains = soup.find_all('domain')
        except:
            pass
        current = False
        for domain in domains:
            if str(domain_.encode('idna').decode('ascii')).lower() in str(domain).lower():
                current = True
                break
        
        if current:
            counter_id += 1
            visit = row[1]

            counter_limit += visit
            sort_list.append(
                {
                    'id': counter_id,
                    'домен': domain_,
                    'запросы': row[0],
                    'доп приписка': f'| {domain_}',
                    'кол-во заходов': visit,
                    'регион': row[2],
                }
            )
        return counter_id, counter_limit, sort_list, False


def create_csv(sort_list, request):
    """
    Создаём итоговый файл с названием result.csv и записываем данные
    """
    with open(f'media/file_excel/result_{request.user.username}.csv', 'w+', encoding="cp1251", newline='') as csvfile:
        fieldnames = [
                'id', 
                'домен', 
                'запросы', 
                'доп приписка', 
                'кол-во заходов', 
                'регион'
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for row in sort_list:
            try:
                writer.writerow(row)
            except:
                pass
        HOST = ':'.join(settings.ALLOWED_HOSTS)
        request.session['file'] = f'http://{HOST}\\media\\file_excel\\result_{request.user.username}.csv'
        request.session['file_count'] = -5