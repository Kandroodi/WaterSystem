from django.shortcuts import render

# Create your views here.


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
                        return HttpResponseRedirect(reverse(app_name + ':add_' + model_name.lower()))
                    return HttpResponseRedirect(reverse(
                        app_name + ':edit_' + model_name.lower(),
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
