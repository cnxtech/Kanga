import pprint
from os import listdir

from django.db import transaction
from os.path import isfile, join

from help.models import *
from kanga import settings
from workspace.builder import builder
import xml.etree.ElementTree as et
import zipfile
import os
import tempfile
import time
import shutil
import glob
from lxml import etree, objectify


def validate_xml(params):
    dtd_file = params['dtd_file']
    xml_file = params['xml_file']
    tmp_target_path = params['tmp_target_path']
    try:
        dtd = etree.DTD(open(dtd_file, 'rb'))
        tree = objectify.parse(open(xml_file, 'rb'))
        ret = dtd.validate(tree)
        if not ret:
            return False
        jar_files = [f for f in listdir(tmp_target_path) if isfile(join(tmp_target_path, f)) and f.endswith('.jar')]
        if not jar_files:
            return False
    except Exception as e:
        raise Exception("validation is failed due to " + e.message)
    return True

def rollback_library_register():
    #to do something
    print 'rollback_library_register'

# @transaction.commit_manually
@transaction.atomic
def clean_up_previous_base_library(params):
    xml_file = params['xml_file']
    jar_target_path = params['jar_target_path']
    try:
        root = et.parse(xml_file).getroot()
        if (root.attrib['type']=='base_library'):
            Library.objects.filter(library_type=Library.BASE_LIBRARY_TYPE).delete()
            if os.path.exists(join(jar_target_path,'base')):
                shutil.rmtree(join(jar_target_path,'base'))
    except Exception as e:
        raise Exception("Base Library cleansing is failed due to: " + str(e))


# @transaction.commit_manually
@transaction.atomic
def register_library_xml_to_db(params, user):
    library_zip_file = params['library_zip_file']
    library_zip_file_path = params['library_zip_file_path']
    target_zip_file_path = params['target_zip_file_path']
    xml_file = params['xml_file']
    tmp_md_target_path = params['tmp_md_target_path']
    md_target_path = params['md_target_path']
    tmp_target_path = params['tmp_target_path']
    jar_target_path = params['jar_target_path']
    try:
        root = et.parse(xml_file).getroot()
        library_id = root.attrib['name'] + "_" + root.attrib['version']
        library_type=Library.BASE_LIBRARY_TYPE
        if (root.attrib['type']!='base_library'):
            library_type=Library.THIRD_PARTY_LIBRARY_TYPE
        library = Library(id=library_id,
                          name=root.attrib['name'],
                          version=root.attrib['version'],
                          user=user,
                          library_type=library_type)
        library.save()
        for processor in root:
            if not Category.objects.filter(pk=processor.attrib['category']).exists():
                category = Category(category=processor.attrib['category'],
                                    library=library,
                                    category_text=processor.attrib['category'].replace('_',' ').title())
                category.save()
            else:
                category = Category.objects.get(category=processor.attrib['category'])
            command = Command(category=category,
                              command=processor.find('name').text,
                              bolt_name=processor.find('class_name').text,
                              md_file=processor.find('md_file').text,
                              node_type=processor.attrib['node_type'],
                              storm_node_type=processor.attrib['storm_node_type'])
            command.save()
            for item in processor.findall('field'):
                place_holder = '' if item.find('placeholder') is None else item.find('placeholder').text
                is_mandatory = True if item.attrib['mandatory'] == 'true' else False
                file_type = FieldType.objects.get(field_type=item.attrib['type'])
                field = Field(id=processor.find('name').text + "_" + item.find('field_name').text,
                              command=command,
                              field_name=item.find('field_name').text,
                              field_type=file_type,
                              default_value=item.attrib['default'],
                              is_mandatory=is_mandatory,
                              placeholder=place_holder)
                field.save()
                if item.find('options'):
                    for each_option in item.find('options'):
                        option = Option(id=command.command+"_"+item.find('field_name').text+"_"+each_option.text,
                                        option_value=each_option.text,
                                        field=field)
                        option.save()
        description = "["+library_id+"] is successfully registered"
        package_location = target_zip_file_path.replace('##library_id##',library_id)
        registry_history = RegistryHistory(description=description,
                                           user=user,
                                           package_location=package_location,
                                           package_filename=library_zip_file,
                                           library_id=library_id)
        registry_history.save()
        zip_files = [f for f in listdir(tmp_target_path) if isfile(join(tmp_target_path, f)) and f.endswith('.zip')]
        for zip_file in zip_files:
            node_codes_zip_file_path = join(tmp_target_path,zip_file)
            print node_codes_zip_file_path
            with zipfile.ZipFile(node_codes_zip_file_path,'r') as z:
                z.extractall(join(jar_target_path,'base'))
                # cmd = 'cd '+join(jar_target_path,'base')+'; npm install'
                cmd = 'cd '+join(jar_target_path,'base')
                print cmd
                builder.command(cmd)
            '''
            jf = JarFile(library=library,zip_file=zip_file)
            jf.save()
            zip_file_path = join(tmp_target_path, zip_file)
            shutil.copy2(zip_file_path, jar_target_path)
            '''
        library.description = library_id + ' is successfully registered'
        library.package_location=package_location
        library.package_filename=library_zip_file
        library.save()
        if not os.path.exists(os.path.dirname(package_location)):
            os.makedirs(os.path.dirname(package_location))
        else:
            shutil.rmtree(os.path.dirname(package_location))
            os.makedirs(os.path.dirname(package_location))
        shutil.copyfile(library_zip_file_path, package_location) # package repository
        for md_file in glob.iglob(tmp_md_target_path):
            shutil.copy2(md_file, md_target_path)
        return library
    except Exception as e:
        raise Exception("DB insertion is failed due to: " + str(e))


def update_build_xml(params):
    try:
        library_line = ''
        include_line = ''
        includes = list()
        template = ''
        build_template = params['build_template']
        build_xml = params['build_xml']
        build_xml = open(build_xml,'w+')
        library_pattern = '<property name="lib.to.include.#N#" value="##plugin_library##"/>'
        include_pattern = '<zipgroupfileset dir="${env.KANGA_LIB_PATH}" includes="##includes##" excludes="META-INF/*.SF"/>'
        jar_files = JarFile.objects.all()
        sequence = 1
        for f in jar_files:
            library_line += '\n' + library_pattern.replace('##plugin_library##',f.jar_file).replace('#N#',str(sequence))
            includes.append('${lib.to.include.'+str(sequence)+'}')
            sequence += 1
        with open(build_template, 'r') as f:
            template = f.read()
        template = template.replace('##library_pattern##',library_line)
        include_line = include_pattern.replace('##includes##',','.join(includes))
        template = template.replace('##include_pattern##',include_line)
        build_xml.write(template)
    except Exception as e:
        raise Exception("Building environment setup is failed due to: " + str(e))



def set_parameters(library_zip_file):
    params = dict()
    params['dtd_file'] = os.path.normpath(settings.BASE_DIR + '/kanga/library.dtd')
    params['library_zip_file'] = library_zip_file
    params['library_zip_file_path'] = os.path.normpath(settings.BASE_DIR + '/' + params['library_zip_file'])
    params['target_zip_file_path'] = os.path.normpath(settings.BASE_DIR + '/system/packages/##library_id##/' + params['library_zip_file'])
    params['jar_target_path'] = os.path.normpath(settings.BASE_DIR + '/workspace/builder/lib')
    params['build_xml_path'] = os.path.normpath(settings.BASE_DIR + '/workspace/builder/tmp')
    params['tmp_base_folder'] = os.path.normpath(settings.BASE_DIR + '/system/tmp')
    params['tmp_file_prefix'] = 'library_'+time.strftime('%Y%m%d_%H%M%S')+'_'
    params['tmp_target_path'] = tempfile.mkdtemp(prefix=params['tmp_file_prefix'], dir=params['tmp_base_folder'])
    params['xml_file'] = os.path.normpath(params['tmp_target_path']+'/library.xml')
    params['tmp_md_target_path'] = os.path.normpath(params['tmp_target_path']+'/doc/*.md')
    params['md_target_path'] = os.path.normpath(settings.BASE_DIR+'/help/doc/')
    params['build_xml_path'] = os.path.normpath(settings.BASE_DIR+'/workspace/builder/tmp')
    params['build_template'] = os.path.normpath(settings.BASE_DIR+'/workspace/builder/tmp/build.xml.template')
    params['build_xml'] = os.path.normpath(settings.BASE_DIR+'/workspace/builder/tmp/build.xml')
    print '------------------------------'
    print 'dtd_file = '+params['dtd_file']
    print 'library_zip_file_path = '+params['library_zip_file_path']
    print 'target_zip_file_path = '+params['target_zip_file_path']
    print 'tmp_base_folder = '+params['tmp_base_folder']
    print 'xml_file = '+params['xml_file']
    print '------------------------------'
    return params


def unzip(params):
    # local variables
    library_zip_file_path = params['library_zip_file_path']
    tmp_target_path = params['tmp_target_path']
    try:
        with zipfile.ZipFile(library_zip_file_path,'r') as z:
            z.extractall(tmp_target_path)
    except Exception as e:
        print e.message


def register(params,user):
    # local variables
    try:
        ## step 2.1 - validate
        validate_xml(params)
        ## step 2.2 - clean up (uninstall previous package)
        clean_up_previous_base_library(params)
        ## step 2.3 - clean up (uninstall previous package)
        register_library_xml_to_db(params, user)
        update_build_xml(params)
    except Exception as e:
        print e.message



def clean_tmp_files(params):
    library_zip_file_path = os.path.dirname(params['library_zip_file_path'])
    tmp_target_path = params['tmp_target_path']
    try:
        if os.path.exists(library_zip_file_path):
            shutil.rmtree(library_zip_file_path)
        if os.path.exists(tmp_target_path):
            shutil.rmtree(tmp_target_path)
    except Exception as e:
        print e.message
    print 'ended....'
    
def npm_install(params):
    jar_target_path = params['jar_target_path']    
    print 'jar_target_path=' + jar_target_path
    try:
        package_json_path=join(jar_target_path,'base/' + 'package.json')
        print package_json_path
        shutil.copy2(package_json_path, jar_target_path)   
        cmd = 'cd '+ jar_target_path +' && npm install'
        #cmd = 'cd '+join(jar_target_path,'base')+' && npm install ' + jar_target_path        
        print cmd
        builder.command(cmd)
    except Exception as e:
        print 'npm_install' + e.message



