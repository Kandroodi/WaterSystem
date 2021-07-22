from django.apps import apps
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from utils import view_util
from utils.view_util import Crud, Cruds, make_tabs, FormsetFactoryManager
from .models import copy_complete
from utilities.search import Search
from django.db.models import CharField, ForeignKey
from partial_date import PartialDateField
from django.db.models import Q
import unidecode


def list_view(request, model_name, app_name):
    '''list view of a model.'''
    s = Search(request, model_name, app_name)
    instances = s.filter()
    if model_name == 'UserLoc': model_name = 'location'
    var = {model_name.lower() + '_list': instances, 'page_name': model_name,
           'order': s.order.order_by, 'direction': s.order.direction,
           'query': s.query.query, 'nentries': s.nentries}
    print(s.notes, 000)
    return render(request, app_name + '/' + model_name.lower() + '_list.html', var)


# @permission_required('utilities.add_generic')
def edit_model(request, name_space, model_name, app_name, instance_id=None,
               formset_names='', focus='', view='complete'):
    '''edit view generalized over models.
    assumes a 'add_{{model_name}}.html template and edit_{{model_name}} function
    and {{model_name}}Form
    '''
    names = formset_names
    model = apps.get_model(app_name, model_name)
    modelform = view_util.get_modelform(name_space, model_name + 'Form')
    instance = model.objects.get(pk=instance_id) if instance_id else None
    crud = Crud(instance) if instance else None
    ffm, form = None, None
    if request.method == 'POST':
        focus, button = getfocus(request), getbutton(request)
        if button in 'delete,cancel,confirm_delete':
            return delete_model(request, name_space, model_name, app_name, instance_id)
        if button == 'saveas' and instance: instance = copy_complete(instance)
        form = modelform(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            print('form is valid: ', form.cleaned_data, type(form))

            instance = form.save()
            if view == 'complete':
                ffm = FormsetFactoryManager(name_space, names, request, instance)
                valid = ffm.save()
                if valid:
                    show_messages(request, button, model_name)
                    if button == 'add_another':
                        # return HttpResponseRedirect(reverse(app_name + ':add_' + model_name.lower()))
                        return HttpResponseRedirect(reverse(app_name + ':' + model_name.lower() + '-insert'))
                    # return HttpResponseRedirect(reverse(
                    #     app_name + ':edit_' + model_name.lower(),
                    #     kwargs={'pk': instance.pk, 'focus': focus}))
                    return HttpResponseRedirect(reverse(
                        app_name + ':' + model_name.lower() + '-update',
                        kwargs={'pk': instance.pk, 'focus': focus}))
                else:
                    print('ERROR', ffm.errors)
            else:
                return HttpResponseRedirect('/utilities/close/')
    if not form: form = modelform(instance=instance)
    if not ffm: ffm = FormsetFactoryManager(name_space, names, instance=instance)
    tabs = make_tabs(model_name.lower(), focus_names=focus)
    page_name = 'Edit ' + model_name.lower() if instance_id else 'Add ' + model_name.lower()
    args = {'form': form, 'page_name': page_name, 'crud': crud,
            'tabs': tabs, 'view': view}
    args.update(ffm.dict)
    return render(request, app_name + '/add_' + model_name.lower() + '.html', args)


# @permission_required('utilities.add_generic')
def add_simple_model(request, name_space, model_name, app_name, page_name):
    '''Function to add simple models with only a form could be extended.
    request 	django object
    name_space 	the name space of the module calling this function (to load forms / models)
    model_name 	name of the model
    app_name 	name of the app
    page_name 	name of the page
    The form name should be of format <model_name>Form
    '''
    modelform = view_util.get_modelform(name_space, model_name + 'Form')
    form = modelform(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, model_name + ' saved')
            return HttpResponseRedirect('/utilities/close/')
    model = apps.get_model(app_name, model_name)
    instances = model.objects.all().order_by('name')
    var = {'form': form, 'page_name': page_name, 'instances': instances}
    return render(request, 'utilities/add_simple_model.html', var)


# @permission_required('utilities.delete_generic')
def delete_model(request, name_space, model_name, app_name, pk):
    model = apps.get_model(app_name, model_name)
    instance = get_object_or_404(model, id=pk)
    focus, button = getfocus(request), getbutton(request)
    print(request.POST.keys())
    print(99, instance.view(), instance, 888)
    print(button)
    if request.method == 'POST':
        if button == 'cancel':
            show_messages(request, button, model_name)
            # return HttpResponseRedirect(reverse(
            #     app_name + ':edit_' + model_name.lower(),
            #     kwargs={'pk': instance.pk, 'focus': focus}))
            return HttpResponseRedirect(reverse(
                app_name + ':' + model_name.lower() + '-update',
                kwargs={'pk': instance.pk, 'focus': focus}))
        if button == 'confirm_delete':
            instance.delete()
            show_messages(request, button, model_name)
            return HttpResponseRedirect('/' + app_name + '/' + model_name.lower())
    info = instance.info
    print(1, info, instance, pk)
    var = {'info': info, 'page_name': 'Delete ' + model_name.lower()}
    print(2)
    return render(request, 'utilities/delete_model.html', var)


def getfocus(request):
    '''extracts focus variable from the request object to correctly set the active tabs.'''
    if 'focus' in request.POST.keys():
        return request.POST['focus']
    else:
        return 'default'


# Create your views here.
def getbutton(request):
    if 'save' in request.POST.keys():
        return request.POST['save']
    else:
        return 'default'


def show_messages(request, button, model_name):
    '''provide user feedback on submitting a form.'''
    if button == 'saveas':
        messages.warning(request,
                         'saved a copy of ' + model_name + '. Use "save" button to store edits to this copy')
    elif button == 'confirm_delete':
        messages.success(request, model_name + ' deleted')
    elif button == 'cancel':
        messages.warning(request, 'delete aborted')
    else:
        messages.success(request, model_name + ' saved')


def close(request):
    '''page that closes itself for on the fly creation of model instances (loaded in a new tab).'''
    return render(request, 'utilities/close.html')


# simple search methods
def search(request, app_name, model_name):
    '''Search function between all fields in a model.
    app_name : application name
    model_name : model name for search
    '''
    model = apps.get_model(app_name, model_name)
    query = request.GET.get("q", "")
    order_by = request.GET.get("order_by", "id")
    query_set = model.objects.all().order_by(order_by)
    # Extract all fields except the relations
    # to include relations, use sorted(model._meta.concrete_fields + model._meta.many_to_many)
    # all_fields = [field.name for field in sorted(model._meta.concrete_fields)]

    ####### General way to implement search----------------------
    # if query is not None:
    #     fields_cf = [f for f in model._meta.fields if isinstance(f, CharField)]  # cf: CharField
    #     queries = [Q(**{f.name: query}) for f in fields_cf]
    #
    #     fields_fk = [f for f in model._meta.fields if isinstance(f, PartialDateField)]  # cf: CharField
    #     queries.append([Q(**{f.name: PartialDateField(query)}) for f in fields_fk])
    #
    #     print(fields_fk)
    #     print(queries)
    #
    #     qs = Q()
    #     for que in queries:
    #         qs = qs | que
    #
    #     query_set = model.objects.filter(qs)
    # -----------------------------------------------------------
    queries = query.split()
    if query is not None:
        query_setall = model.objects.none()
        for qs in queries:
            query_seti = query_set.filter(
                Q(name__icontains=qs) |
                Q(un_name__icontains=qs) |
                Q(watersystem__original_term__icontains=qs) |
                Q(watersystem__un_original_term__icontains=qs) |
                Q(construction_date_lower__icontains=qs) |
                Q(construction_date_upper__icontains=qs) |
                Q(first_reference_lower__icontains=qs) |
                Q(first_reference_upper__icontains=qs) |
                Q(end_functioning_year_lower__icontains=qs) |
                Q(end_functioning_year_upper__icontains=qs) |
                Q(city__name__icontains=qs) |
                Q(purpose__name__icontains=qs) |
                Q(neighbourhood__neighbourhood_number__icontains=qs) |
                Q(latitude__icontains=qs) |
                Q(longitude__icontains=qs) |
                Q(institution_as_location__name__icontains=qs) |
                Q(secondary_literature__title__icontains=qs) |
                Q(secondary_literature__author__icontains=qs) |
                Q(comment__icontains=qs) |
                Q(un_comment__icontains=qs)

            )
            query_setall = query_setall | query_seti
        query_set = query_setall.order_by(order_by)
    if query == "":
        query_set = model.objects.all().order_by(order_by)
        # query_set = query_set.filter(
        #     Q(name__icontains=query) |
        #     Q(watersystem__original_term__icontains=query) |
        #     Q(construction_date_lower__icontains=query) |
        #     Q(construction_date_upper__icontains=query) |
        #     Q(first_reference_lower__icontains=query) |
        #     Q(first_reference_upper__icontains=query) |
        #     Q(end_functioning_year_lower__icontains=query) |
        #     Q(end_functioning_year_upper__icontains=query) |
        #     Q(city__name__icontains=query) |
        #     Q(purpose__name__icontains=query)
        # ).order_by(order_by)

    return query_set


def institutionsimplesearch(request):
    '''
    Simple search function between specified fields in the institution model.
    Simple search return the OR result between the search result for each field
    '''
    model = apps.get_model('installations', 'institution')  # app_name, model_name
    query = request.GET.get("q", "")
    order_by = request.GET.get("order_by", "id")
    query_set = model.objects.all().order_by(order_by)

    queries = query.split()
    if query is not None:
        query_setall = model.objects.none()
        for qs in queries:
            query_seti = query_set.filter(
                Q(name__icontains=qs) |
                Q(un_name__icontains=qs) |
                Q(type_many__name__icontains=qs) |
                Q(type_many__un_name__icontains=qs) |
                Q(purpose__name__icontains=qs) |
                Q(city__name__icontains=qs) |
                Q(neighbourhood__neighbourhood_number__icontains=qs) |
                Q(latitude__icontains=qs) |
                Q(longitude__icontains=qs) |
                Q(start_date_lower__icontains=qs) |
                Q(start_date_upper__icontains=qs) |
                Q(first_reference_lower__icontains=qs) |
                Q(first_reference_upper__icontains=qs) |
                Q(end_date_lower__icontains=qs) |
                Q(end_date_upper__icontains=qs) |
                Q(religion__name__icontains=qs) |
                Q(secondary_literature__title__icontains=qs) |
                Q(secondary_literature__author__icontains=qs) |
                Q(comment__icontains=qs) |
                Q(un_comment__icontains=qs)

            )
            query_setall = query_setall | query_seti
        query_set = query_setall.order_by(order_by)
    if query == "":
        query_set = model.objects.all().order_by(order_by)

    return query_set


# methods for unaccent the fields for search
def unaccent_installations(request, app_name, model_name):
    """"This method copies unaccented version of the data to a new un_<field name> which will used for search without
    diacritics. For instance, if field <name> has a diacritics then <un_name> field won't.
    Search fields for installation are:
    - name --> un_name
    - comment --> un_comment

    """
    model = apps.get_model(app_name, model_name)
    query_set = model.objects.all()
    for query in query_set:
        if query.name is not None:
            query.un_name = unidecode.unidecode(query.name)
            query.save()
        if query.comment is not None:
            query.un_comment = unidecode.unidecode(query.comment)
            query.save()


def unaccent_institution(request, app_name, model_name):
    """"This method copies unaccented version of the data to a new un_<field name> which will used for search without
        diacritics. For instance, if field <name> has a diacritics then <un_name> field won't.
        Search fields for institution are:
        - name --> un_name
        - comment --> un_comment

        """
    model = apps.get_model(app_name, model_name)
    query_set = model.objects.all()
    for query in query_set:
        if query.name is not None:
            query.un_name = unidecode.unidecode(query.name)
            query.save()
        if query.comment is not None:
            query.un_comment = unidecode.unidecode(query.comment)
            query.save()


def unaccent_person(request, app_name, model_name):
    """"This method copies unaccented version of the data to a new un_<field name> which will used for search without
        diacritics. For instance, if field <name> has a diacritics then <un_name> field won't.
        Search fields for person are:
        - name --> un_name
        - role --> un_role
        - comment --> un_comment

        """
    model = apps.get_model(app_name, model_name)
    query_set = model.objects.all()
    for query in query_set:
        if query.name is not None:
            query.un_name = unidecode.unidecode(query.name)
            query.save()
        if query.role is not None:
            query.un_role = unidecode.unidecode(query.role)
            query.save()
        if query.comment is not None:
            query.un_comment = unidecode.unidecode(query.comment)
            query.save()


def unaccent_evidence(request, app_name, model_name):
    """"This method copies unaccented version of the data to a new un_<field name> which will used for search without
        diacritics. For instance, if field <name> has a diacritics then <un_name> field won't.
        Search fields for evidence are:
        - title --> un_title
        - author --> un_author
        - description --> un_description

        """
    model = apps.get_model(app_name, model_name)
    query_set = model.objects.all()
    for query in query_set:
        if query.title is not None:
            query.un_title = unidecode.unidecode(query.title)
            query.save()
        if query.author is not None:
            query.un_author = unidecode.unidecode(query.author)
            query.save()
        if query.description is not None:
            query.un_description = unidecode.unidecode(query.description)
            query.save()


def unaccent_watersystem(request, app_name, model_name):
    """"This method copies unaccented version of the data to a new un_<field name> which will used for search without
        diacritics. For instance, if field <name> has a diacritics then <un_name> field won't.
        Search fields for water system are:
        - original_term --> un_original_term

        """
    model = apps.get_model(app_name, model_name)
    query_set = model.objects.all()
    for query in query_set:
        if query.original_term is not None:
            query.un_original_term = unidecode.unidecode(query.original_term)
            query.save()


def unaccent_institutiontype(request, app_name, model_name):
    """"This method copies unaccented version of the data to a new un_<field name> which will used for search without
        diacritics. For instance, if field <name> has a diacritics then <un_name> field won't.
        Search fields for institution type are:
        - name --> un_name
        -

        """
    model = apps.get_model(app_name, model_name)
    query_set = model.objects.all()
    for query in query_set:
        if query.name is not None:
            query.un_name = unidecode.unidecode(query.name)
            query.save()
