import os
import pprint

import markdown2
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from help.models import Category, Command
from kanga import settings


@login_required
def tutorials(request, command_id='all'):
    help_doc = 'Help document will be displayed here'
    command_name = 'Please choose a command'
    command = None
    commands = list()
    all_commands = Command.objects.all()
    error_message = ''
    try:
        if command_id=='all':
            for item in all_commands:
                command = item
                break
        else:
            command = Command.objects.get(command=command_id)
        md_file = os.path.normpath(os.path.join(settings.BASE_DIR,'help','doc',command.md_file))
        help_doc = markdown2.markdown_path(md_file,extras=["tables"])
        command_name = command.command
        for item in all_commands:
            t = dict()
            t['category'] = item.category
            print '1111'
            command_url = reverse('help:tutorials', args=(item.command,))
            print 'command_url'
            t['command_url'] = "<a href='"+command_url+"'>"+item.command+"</a>"
            t['node_type'] = item.node_type
            pprint.pprint(t)
            commands.append(t)
        pprint.pprint(commands)
    except Exception as e:
        error_message = str(e)
        print e
    context = {'commands': commands, 'command_name': command_name, 'help_doc': help_doc, 'error_message': error_message}
    return render(request, 'help/tutorials.html', context)


def labels(request, label_id='frequently used'):
    categories = Category.objects.all()
    num_commands = Command.objects.count()
    context = {'num_commands': num_commands, 'categories': categories, 'label_id': label_id}
    return render(request, 'help/tutorial_labels.html', context)


def tutorial_details(request, category_id, command_id):
    categories = Category.objects.all()
    num_commands = Command.objects.count()
    command = get_object_or_404(Command, pk=command_id)
    context = {'num_commands': num_commands, 'categories': categories, 'category_id': category_id, 'command': command}
    return render(request, 'help/tutorial_details.html', context)




def contacts(request):
    return render(request, 'help/contacts.html')


def recommended_process(request):
    return render(request, 'help/recommended_process.html')


def index(request):
    return render(request, 'help/index.html')














