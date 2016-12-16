import os, json, re
import xml.etree.ElementTree as et
from django.db import transaction
from django.conf import settings
import libxml2, tarfile, zipfile, markdown2
from django.utils.safestring import mark_safe
from help.models import Category, Command, Field, Option, Library, RegistryHistory

def validate_xml(dtd_file,xml_file):
    result = {'result':'success','message':'complete DTD validation'}
    try:
        dtd = libxml2.parseDTD(None, dtd_file)
        ctxt = libxml2.newValidCtxt()
        doc = libxml2.parseFile(xml_file)
        ret = doc.validateDtd(ctxt, dtd)
        if ret != 1:
            print "error doing DTD validation"
            result['result'] =  "fail"
            result['message'] =  "error doing DTD validation"

        doc.freeDoc()
        dtd.freeDtd()
        del dtd
        del ctxt
    except Exception as e:
            result['result'] =  "fail"
            result['message'] =  "error doing DTD validation: " + e.message
    return result

@transaction.commit_manually
def deleteLibrary(libraryname):
    result = {'result':'success','message':'Completed Library version deletion'}
    try:
        insertRegistryHistory( libraryname + " deletion is completed!")
        q = Library.objects.get(libname=libraryname)
        q.delete()
        transaction.commit()
    except Exception as e:
        result['result'] = 'fail'
        result['message'] = 'Failed Library version deletion: ' + e.message
        transaction.rollback()
    return result

@transaction.commit_manually
def changeLibstate(libraryname,state):
    result = {'result':'success','message':'Completed Library version state change'}
    try:
        q = Library.objects.get(libname=libraryname)
        q.state = state
        q.save()
    except Exception as e:
        result['result'] = 'fail'
        result['message'] = 'Failed Library version change: ' + e.message
        transaction.rollback()
    else:
        transaction.commit()
    return result

def insertRegistryHistory(content):
    q = RegistryHistory(content = content)
    q.save()

def insertLibrary(key, state='active', description=''):
    q = None
    if state:
        q = Library(pk=key,state=state,description=description)
    else:
        q = Library(pk=key)
    q.save()
    # return q

def insertCategory(key, libversion_id, category_text='', category_colour=''):
    q = None
    if category_text:
        q = Category(pk=key,category_text=category_text,libversion_id=libversion_id)
        # q = Category(category=key,category_text=category_text,libversion_id=libversion_id)
    elif category_colour:
        q = Category(pk=key,category_colour=category_colour,libversion_id=libversion_id)
        # q = Category(category=key,category_colour=category_colour,libversion_id=libversion_id)
    else:
        q = Category(pk=key,libversion_id=libversion_id)
        # q = Category(category=key,libversion_id=libversion_id)
    q.save()
    # return q

def insertCommand(key,command_tag,bolt_name,storm_node_type,category_id,node_type):
    q = Command(pk=key,command_tag=command_tag,bolt_name=bolt_name,storm_node_type=storm_node_type,category_id=category_id,node_type=node_type)
    # q = Command(command=key,command_tag=command_tag,bolt_name=bolt_name,storm_node_type=storm_node_type,category_id=category_id,node_type=node_type)
    q.save()
    # return q

def insertField(key,field_name,default_value,is_mandatory,command_id,field_type_id,short_description='',placeholder=''):
    q = None
    if short_description:
        q = Field(pk=key,field_name=field_name,default_value=default_value,is_mandatory=is_mandatory,command_id=command_id,field_type_id=field_type_id,short_description=short_description)
        # q = Field(field=key,field_name=field_name,default_value=default_value,is_mandatory=is_mandatory,command_id=command_id,field_type_id=field_type_id,short_description=short_description)
    elif placeholder:
        q = Field(pk=key,field_name=field_name,default_value=default_value,is_mandatory=is_mandatory,command_id=command_id,field_type_id=field_type_id,placeholder=placeholder)
        # q = Field(field=key,field_name=field_name,default_value=default_value,is_mandatory=is_mandatory,command_id=command_id,field_type_id=field_type_id,placeholder=placeholder)
    q.save()
    # return q


def insertOption(key,option_value,field_name_id):
    q = Option(pk=key,option_value=option_value,field_name_id=field_name_id)
    # q = Option(option=key,option_value=option_value,field_name_id=field_name_id)
    q.save()
    # return q


@transaction.commit_manually
def insertXmlToDB(xml_file):
    result = {'result': 'success','message':'Insert library data success!!'}

    root = et.parse(xml_file).getroot()
    libname = root.attrib['name'] + "_" + root.attrib['version']

    try:
        insertRegistryHistory(libname + " insertion is completed")
        insertLibrary(libname)
        for processor in root:
            insertCategory(processor.attrib['category'],libname)
            insertCommand(processor.find('name').text,processor.attrib['tag'],processor.find('class_name').text,processor.attrib['node'],processor.attrib['category'],processor.attrib['type'])
            for items in processor.findall('field'):
                shortDescription = ''
                placeHolder = ''
                if items.find('placeholder'):
                    placeHolder = items.find('placeholder').text
                elif items.find('shortdescription') != None:
                    shortDescription = items.find('shortdescription').text


                insertField(processor.find('name').text + "_" + items.find('field_name').text,items.find('field_name').text,items.attrib['default'],items.attrib['mandatory'],processor.find('name').text,
                            items.attrib['type'],shortDescription,placeHolder)

                if items.find('options') != None:
                    for option in items.find('options'):
                        insertOption(processor.find('name').text + "_" + items.find('field_name').text + "_" + option.text, option.text, processor.find('name').text + "_" + items.find('field_name').text)
    except Exception as e:
        transaction.rollback()
        result['result'] = 'fail'
        result['message'] = 'Insert library data fail!!  (' + e.message + ')'
    else:
        transaction.commit()

    return result

def decompression(file,targetPath):
    result = {'result':'success', 'message':''}

    extension = os.path.splitext(file)[1]

    if 'zip' in extension:
        result['message'] = extractZip(file,targetPath)
    elif 'gz' in extension:
        result['message'] = extractTar(file,targetPath)

    return result


def extractTar(file,targetPath):
    result = 'Extract tar is completed'
    try:
        tar = tarfile.open(file)
        tar.extractall(targetPath)
        tar.close()
    except Exception as tarerror:
        result = 'Extract tar is failed: ' + tarerror.message
    return result

def extractZip(file,targetPath):
    result = 'Extract zip is completed'
    try:
        with zipfile.ZipFile(file,'r') as z:
            z.extractall(targetPath)
    except Exception as ziperror:
        result = 'Extract zip is failed: ' + ziperror.message
    return result

def createHTMLFromMD(md_file):
    #------------------ These path must be changed -----------------------##
    static_imgpath = "uiapp/image/"
    static_templatepath = "plugin"
    #------------------ These path must be changed -----------------------##

    result = {'result':'success', 'message':'HTML creation is completed!'}

    content = markdown2.markdown_path(md_file,extras=["tables"])

    #------------------ change "<img src=image/xxxxx.png ~~~>" to "<img src={%static 'uiapp~~~~' %} ----------#
    imgre = re.search(r'<img.*?src="([^"]*)"',content)
    imgfile = str(imgre.group()).replace('"','')
    imgfile = imgfile.split('/')
    imgfilename = imgfile[1]
    imagepath = r'<img src="{% static' + " '" + static_imgpath + imgfilename +"'" + ' %}"'
    content = re.sub(r'<img.*?src="([^"]*)"', imagepath ,content)
    #------------------ change "<img src=image/xxxxx.png ~~~>" to "<img src={%static 'uiapp~~~~' %} ----------#

    #----------------- Add css and  {% load staticfiles %} ---------------------------#
    content = '{% load staticfiles %}\r\n<!DOCTYPE html>\r\n<html>\r\n' + '<head>\r\n<style type="text/css">\r\ntable {max-width: 95%;border: 1px solid #ccc;}\r\nth {background-color: #000000;color: #ffffff;}\r\ntd {background-color: #dcdcdc; text-align:center;}\r\n</style>\r\n</head>\r\n<body>\r\n' + content
    content = content + '</body>\r\n</html>'
    #----------------- Add css and  {% load staticfiles %} ---------------------------#

    #------------------ File(HTML) Creation ---------------------#
    try:
        htmlfilename = (imgfilename.split('.'))[0] + ".html"
        with open(settings.TEMPLATE_DIRS[0] + '\\' + static_templatepath + '\\' + htmlfilename,'w') as htmlfile:
            htmlfile.write(mark_safe(content))
    except Exception as mderror:
        result = {'result':'fail', 'message':'HTML creation is failed!' + mderror.message}
    else:
      result['filepath'] = settings.TEMPLATE_DIRS[0] + '\\' + static_templatepath + '\\' + htmlfilename
    #------------------ File(HTML) Creation ---------------------#

    return result





# @transaction.commit_manually
# def insertXmlToDB_initial(xml_file):
#     result = {'result': 'success','message':'Insert library data success!!'}
#
#     root = et.parse(xml_file).getroot()
#     libVersion = root.attrib['name'] + "_" + root.attrib['version']
#
#     try:
#         insertLibrary(libVersion)
#         for processor in root:
#             qCategory = insertCategory(processor.attrib['category'],libVersion)
#             qCommand = insertCommand(processor.find('name').text,processor.attrib['tag'],processor.find('class_name').text,processor.attrib['node'],qCategory.id,processor.attrib['type'])
#             for items in processor.findall('field'):
#                 print items.find('placeholder').text
#                 shortDescription = ''
#                 placeHolder = ''
#                 if items.find('placeholder') != None:
#                     placeHolder = items.find('placeholder').text
#                 elif items.find('shortdescription') != None:
#                     shortDescription = items.find('shortdescription').text
#
#                 qField = insertField(processor.find('name').text + "_" + items.find('field_name').text,items.find('field_name').text,items.attrib['default'],items.attrib['mandatory'],qCommand.id,
#                             items.attrib['type'],shortDescription,placeHolder)
#
#                 if items.find('options') != None:
#                     for option in items.find('options'):
#                         insertOption(processor.find('name').text + "_" + items.find('field_name').text + "_" + option.text, option.text, qField.id)
#     except Exception as e:
#         transaction.rollback()
#         result['result'] = 'fail'
#         result['message'] = 'Insert library data fail!!  (' + e.message + ')'
#     else:
#         transaction.commit()
#
#     return result
