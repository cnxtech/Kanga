import markdown2
from django.http import HttpResponse
from django.db.models import Q
from help.models import Category, Command, Field, Option, FieldType
from django.core.urlresolvers import reverse
import json
import os
from knowledge.models import RealtimeQuery
from kanga import settings


def tag_html(tag):
    return "<i class='fa fa-tag'></i> "+tag if tag else ""


def filter_categories(request, category_id='all'):
    if category_id and category_id != "all":
        commands = Command.objects.filter(category_id=category_id)
    else:
        commands = Command.objects.all()
    command_json_array = []
    node = {"data" : command_json_array}
    for command in commands:
        href = reverse('help:tutorial-details', kwargs={'category_id': command.category.category,
                                                   'command_id': command.command})
        command_json_array.append(
            {
                "command": "<a href='"+href+"'>"+command.command+"</a>",
                "short_description": command.command_short_description,
                "category": command.category.category_text,
                "label": tag_html(command.command_tag)
            }
        )
    return HttpResponse(json.dumps(node, indent=4), content_type='application/json')



def filter_labels(request, label):
    commands = Command.objects.filter(command_tag=label)
    command_json_array = []
    node = {"data" : command_json_array}
    for command in commands:
        href = reverse('help:tutorial-details', kwargs={'category_id': command.category.category,
                                                           'command_id': command.command})
        command_json_array.append(
            {
                "command": "<a href='"+href+"'>"+command.command+"</a>",
                "short_description": command.command_short_description,
                "category": command.category.category_text,
                "label": tag_html(command.command_tag)
            }
        )
    return HttpResponse(json.dumps(node, indent=4), content_type='application/json')

def processors(request):
    categories = Category.objects.filter(~Q(category="builtin"))
    categories_json_array = []
    node = {"items" : categories_json_array}
    for category in categories:
        tcategory = \
            {
                "category": category.category,
                "label": category.category_text,
                "processors": []
            }
        for command in Command.objects.filter(category=category.category):
            tcommand = \
                {
                    "bolt_name": command.bolt_name,
                    "name": command.command,
                    "icon": command.command,
                    "node_type": command.node_type,
                    "args": []
                }
            for field in Field.objects.filter(command=command.command):
                tfield = \
                    {
                        "name": field.field_name,
                        "type": field.field_type_id,
                        "placeholder": field.placeholder,
                        "default": field.default_value,
                        "is_mandatory": field.is_mandatory,
                        "options": []
                    }
                if field.id == 'dummy_macro_choose_index':
                    for id in RealtimeQuery.objects.all():
                        toption = \
                            {
                                "text": id.name,
                                "value": str(id.id) + '_' + str(id.name)
                            }
                        tfield['options'].append(toption)
                    tcommand['args'].append(tfield)
                else:
                    for option in Option.objects.filter(field=field.id):
                        toption = \
                            {
                                "text": option.option_value,
                                "value": option.option_value
                            }
                        tfield['options'].append(toption)
                    tcommand['args'].append(tfield)
            tcategory['processors'].append(tcommand)
        categories_json_array.append(tcategory)

    tcategory = \
        {
            "category": "macro",
            "label": "Macro",
            "processors": []
        }
    tcommand1 = \
        {
            "bolt_name": "",
            "name": "dummy_input",
            "icon": "dummy_input",
            "node_type": "SOURCE",
            "args": []
        }
    tcommand2 = \
        {
            "bolt_name": "",
            "name": "dummy_output",
            "icon": "dummy_output",
            "node_type": "SINK",
            "args": []
        }
    tcommand3 = \
        {
            "bolt_name": "",
            "name": "macro",
            "icon": "macro",
            "node_type": "NORMAL",
            "args": []
        }
    tfield = \
        {
            "name": "macro_name",
            "type": "dropdown",
            "placeholder": "",
            "default": "",
            "is_mandatory": 1,
            "options": []
        }
    for id in RealtimeQuery.objects.all():
        toption = \
            {
                "text": id.name,
                "value": str(id.id) + '_' + str(id.name)
            }
        tfield['options'].append(toption)
    tcommand3['args'].append(tfield)
    tcategory['processors'].append(tcommand1)
    tcategory['processors'].append(tcommand2)
    tcategory['processors'].append(tcommand3)
    categories_json_array.append(tcategory)
    return HttpResponse(json.dumps(node, indent=4), content_type='application/json')


def help_doc(request):
    try:
        content = ''
        command_id =  request.POST.get('command_id', request.GET.get('command_id', ''))
        command = Command.objects.get(command=command_id)
        md_file = os.path.normpath(os.path.join(settings.BASE_DIR,'help','doc',command.md_file))
        content = markdown2.markdown_path(md_file,extras=["tables"])
        return HttpResponse(content)
    except Exception as e:
        print e
        return HttpResponse('<h1>Help doc is not found</h1>')