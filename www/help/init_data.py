from help.models import Category, Command, Field, FieldType, Option
from django.http import HttpResponse
import os
import csv


def create(request):
    delete_everything()
    create_category()
    create_command()
    create_fieldtype()
    create_field()
    create_option()
    return HttpResponse("ok")


def delete_everything():
    Option.objects.all().delete()
    FieldType.objects.all().delete()
    Field.objects.all().delete()
    Command.objects.all().delete()
    Category.objects.all().delete()




def create_category():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'category.tsv')
    with open(file_path, 'r') as csv_file:
        categories = csv.reader(csv_file, delimiter='^')
        for category in categories:
            if not Category.objects.filter(category=category[0]).exists():
                Category.objects.create(category=category[0],
                                        category_text=category[1],
                                        category_colour=category[2])


def create_command():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'command.tsv')
    with open(file_path, 'r') as csv_file:
        commands = csv.reader(csv_file, delimiter='^')
        for command in commands:
            if not Command.objects.filter(command=command[1]).exists():
                Command.objects.create(category=Category.objects.get(category=command[0]),
                                        command=command[1],
                                        command_short_description="",
                                        command_explanation="",
                                        command_example="",
                                        command_tag=command[2])


def create_field():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'field.tsv')
    with open(file_path, 'r') as csv_file:
        fields = csv.reader(csv_file, delimiter='^')
        for field in fields:
            command = Command.objects.get(command=field[3])
            if not Field.objects.filter(id=field[0]).exists() and command:
                Field.objects.create(command=command,
                                    id=field[0],
                                    field_name=field[1],
                                    field_type=FieldType.objects.get(field_type=field[2]),
                                    short_description=field[4])


def create_fieldtype():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'fieldtype.tsv')
    with open(file_path, 'r') as csv_file:
        fieldtypes = csv.reader(csv_file, delimiter='^')
        for fieldtype in fieldtypes:
            if not FieldType.objects.filter(field_type=fieldtype[0]).exists():
                FieldType.objects.create(field_type=fieldtype[0],
                                    has_options=str2bool(fieldtype[1]))


def create_option():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'option.tsv')
    with open(file_path, 'r') as csv_file:
        options = csv.reader(csv_file, delimiter='^')
        for option in options:
            if not Option.objects.filter(id=option[0]).exists():
                Option.objects.create(id=option[0],
                                        field_name=Field.objects.get(id=option[1]),
                                        option_value=option[2])


def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")