__author__ = 'a'
#Parse XML directly from the file path

import xml.etree.ElementTree as xml
import os
import shutil


htmlRendrering = ""


def openScreenToPage():
    global htmlRendrering
    htmlRendrering += "<html>\n<head>\n"
    htmlRendrering += '<link href="{{ STATIC_URL }}home.css" rel="stylesheet" type="text/css" media="screen" />'
    htmlRendrering += '</head>\n<body>\n'
    htmlRendrering += '<br/><br/><div align="center">'




def endScreenEndPage():
    global htmlRendrering
    htmlRendrering += "</div></body>\n</html>\n"


def findvalues(e):
    values = e.find('values')
    l = []
    if values is not None:
        for value in values:
            l.append(value.text)
    else:
        l = [""]

    return l


def newScreen():
    global htmlRendrering
    htmlRendrering = ""


def componentType(e):
    if len(e.attrib) != 0:
        return e.attrib['type']
    else:
        return e.find('identifier').text.upper()


def button(e):
    global htmlRendrering
    l = []
    l = findvalues(e)
    htmlRendrering += ' <input type=\"button' + '\" name=\"' + e.find(
        'identifier').text + '\" id =\"' + e.find('identifier').text + '\" value=\"' + e.find(
        'identifier').text + '\"/><br>\n'


def link(e):
    global htmlRendrering
    l = []
    l = findvalues(e)
    htmlRendrering += ' <a href=\"' + e.find('identifier').text + '\">' + e.find('identifier').text + '</a><br/>\n'


def staticText(e):
    global htmlRendrering
    l = []
    l = findvalues(e)
    htmlRendrering += e.find('identifier').text + ': <p' + ' name=\"' + e.find(
        'identifier').text + '\" id =\"' + e.find(
        'identifier').text + '\">' + l[0] + '</p><br/>\n'


def dynamicText(e):
    global htmlRendrering
    l = []
    l = findvalues(e)
    htmlRendrering += e.find('identifier').text + ': <div><span' + ' name=\"' + e.find(
        'identifier').text + '\" id =\"' + e.find(
        'identifier').text + '\">' + l[0] + '</span></div><br/>\n'


def radioButton(e):
    global htmlRendrering
    l = []
    l = findvalues(e)
    for i in l:
        htmlRendrering += e.find('identifier').text + ': <input type=\"radio\"' + ' name=\"' + e.find(
            'identifier').text + '\" id =\"' + e.find(
            'identifier').text + '\" value=\"' + i + '\">' + i + '<br/>\n'


def checkBox(e):
    global htmlRendrering
    l = []
    l = findvalues(e)
    for i in l:
        htmlRendrering += e.find('identifier').text + ': <input type=\"checkbox\"' + ' name=\"' + e.find(
            'identifier').text + '\" id =\"' + e.find(
            'identifier').text + '\" value=\"' + i + '\">' + i + '<br/>\n'


def comboBox(e):
    global htmlRendrering
    htmlRendrering += e.find('identifier').text + ': <select name=\"' + e.find('identifier').text + '\" id=\"' + e.find('identifier').text +'\">\n'
    if not e.find('children'):
        pass
    else:
        for child in e:
             for component1 in child:
                 htmlRendrering += '<option value=\"' + component1.find('identifier').text + '\">' + component1.find('identifier').text + '</option>\n'
    htmlRendrering += '</select><br/>\n'


def tableTag(e):
    global htmlRendrering
    htmlRendrering += e.find('identifier').text + ': <table border=5><br/>\n'
    if e.find('children') is not None:
        for child in e:
            if child.find('component') is not None:
                htmlRendrering += "<tf>\n"
                for component1 in child:
                    htmlRendrering += "<th>"
                    generateRendering(component1)
                    htmlRendrering += "</th>\n"
                htmlRendrering += "</tf>\n"
            else:
                pass

    if e.find('values') is not None:
        for tr in e.find('values'):
            if child.find('tr') is not None:
                htmlRendrering += "<tr>\n"
                for td1 in tr:
                    htmlRendrering += "<td>"
                    htmlRendrering += td1.text
                    htmlRendrering += "</td>\n"
                htmlRendrering += "</tr>\n"

    htmlRendrering += '</table><br/>\n'


def listBox(e):
    global htmlRendrering
    htmlRendrering += e.find('identifier').text + ': <select multiple=\"multiple\"><br/>\n'
    l = []
    l = findvalues(e)
    if len(l) != 0:
        for i in l:
            htmlRendrering += '<option value=\"' + i + '\">' + i + '</option>\n'
    htmlRendrering += '</select><br/>\n'


def editText(e):
    global htmlRendrering
    l = []
    l = findvalues(e)
    htmlRendrering += e.find('identifier').text + ': <input type=\"text' + '\" name=\"' + e.find(
        'identifier').text + '\" id =\"' + e.find('identifier').text + '\" value=\"' + l[0] + '\"/><br/>\n'


def passwordText(e):
    global htmlRendrering
    l = []
    l = findvalues(e)
    htmlRendrering += e.find('identifier').text + ': <input type=\"password' + '\" name=\"' + e.find(
        'identifier').text + '\" id =\"' + e.find('identifier').text + '\" value=\"' + l[0] + '\"/><br/>\n'


def imageTag(e):
    global htmlRendrering
    l = []
    l = findvalues(e)
    htmlRendrering += '<img src=\"' + "{{ STATIC_URL }}python.jpg" + '\" alt =\"the image alternative is ' + e.find(
        'identifier').text + '\"/><br/>\n'


def simpleTag(e):
    global htmlRendrering
    l = []
    l = findvalues(e)
    htmlRendrering += e.find('identifier').text + ': <div  name=\"' + e.find(
        'identifier').text + '\" id =\"' + e.find('identifier').text + '\" >' + l[0] + '<br/>'
    for child in e:
        for component1 in child:
            generateRendering(component1)
    htmlRendrering += '</div><br/>'


def checkBoxes(e):
    global htmlRendrering
    l = []
    l = findvalues(e)
    if not e.find('children'):
        checkBox(e)
    else:
        htmlRendrering += e.find('identifier').text + ': <br/>'
        for child in e:
            for component1 in child:
                generateRendering(component1)
    htmlRendrering += '<br/>'


def radioButtons(e):
    global htmlRendrering
    l = []
    l = findvalues(e)
    if not e.find('children'):
        radioButton(e)
    else:
        htmlRendrering += e.find('identifier').text + ': <br/>'
        for child in e:
            for component1 in child:
                generateRendering(component1)
    htmlRendrering += '<br/>'

def ConfigureMysiteUrls():
    urlsFile = open('mysite/mysite/urls.py' , 'w')
    urlcontent = 'from django.conf.urls import patterns, include, url\n'
    urlcontent += "urlpatterns = patterns('',url(r'^webApp/', include('webApp.urls')),)\n"
    urlsFile.write(urlcontent)
    urlsFile.close()


def listTag(e):
    global htmlRendrering
    l = []
    l = findvalues(e)
    htmlRendrering += e.find('identifier').text + ': <ol  name=\"' + e.find(
        'identifier').text + '\" id =\"' + e.find('identifier').text + '\" >' + l[0] + '<br/>\n'
    for child in e:
        for component1 in child:
            htmlRendrering += "<li>"
            generateRendering(component1)
            htmlRendrering += "</li>\n"
    htmlRendrering += '</ol><br/>\n'


def buildingDjangoFramework():


    try:
        shutil.rmtree('mysite')
    except:
        pass

    creatingDjandoProject = "django-admin.py startproject mysite"
    os.system(creatingDjandoProject)

    os.chdir("mysite")


    creatingDjangoApp = "python manage.py startapp webApp"
    os.system(creatingDjangoApp)

    os.chdir("webApp")
    try:
        os.makedirs("static")
    except:
        pass

    try:
        shutil.copyfile('../../home.css', 'static/home.css')
    except:
        pass

    try:
        shutil.copyfile('../../python.jpg', 'static/python.jpg')
    except:
        pass

    try:
        os.makedirs("templates")
    except:
        pass

    os.chdir("templates")

    try:
        os.makedirs("rendering")
    except:
        pass
    os.chdir("../../../")



def generateRendering(component):
    global htmlRendrering
    if componentType(component) == 'BUTTON':
        button(component)
    else:
        if componentType(component) == 'LINK':
            link(component)
        else:
            if componentType(component) == 'STATIC_TEXT':
                staticText(component)
            else:
                if componentType(component) == 'RADIO_BUTTON':
                    radioButton(component)
                else:
                    if componentType(component) == 'CHECK_BOX':
                        checkBox(component)
                    else:
                        if componentType(component) == 'COMBO_BOX':
                            comboBox(component)
                        else:
                            if componentType(component) == 'LIST_BOX':
                                listBox(component)
                            else:
                                if componentType(component) == 'EDIT_BOX':
                                    editText(component)
                                else:
                                    if componentType(component) == 'TEXT_AREA':
                                        textArea(component)
                                    else:
                                        if componentType(component) == 'PASSWORD':
                                            passwordText(component)
                                        else:
                                            if componentType(component) == 'DYNAMIC_TEXT':
                                                dynamicText(component)
                                            else:
                                                if componentType(component) == 'SIMPLE':
                                                    simpleTag(component)
                                                else:
                                                    if componentType(component) == 'LIST':
                                                        listTag(component)
                                                    else:
                                                        if componentType(component) == 'IMAGE':
                                                            imageTag(component)
                                                        else:
                                                            if componentType(component) == 'CHECK_BOXES':
                                                                checkBoxes(component)
                                                            else:
                                                                if componentType(component) == 'RADIO_BUTTONS':
                                                                    radioButtons(component)
                                                                else:
                                                                    if componentType(component) == 'TABLE':
                                                                        tableTag(component)


def textArea(e):
    global htmlRendrering
    htmlRendrering += '<textArea name=\"' + e.find(
        'identifier').text + '\" id =\"' + e.find('identifier').text + '\">\n'
    l = []
    l = findvalues(e)
    htmlRendrering += l[0] + '\n</textarea>\n'


def mainFunction():
    buildingDjangoFramework()
    viewsFile = open('mysite/webApp/views.py', 'w')
    viewsContent = 'from django.http import HttpResponse\n'
    viewsContent += 'from django.shortcuts import render\n'
    viewsContent +='def index(request):\n'
    viewsContent += "\treturn render(request, 'index.html')\n\n"

    urlsFile = open('mysite/webApp/urls.py' , 'w')
    urlcontent = 'from django.conf.urls import patterns, url\n'
    urlcontent += 'from webApp import views\n'
    urlcontent += "urlpatterns = patterns('',url(r'^$', views.index, name='index'),\n"

    index = '<html>\n<head>\n'
    index += '<link href="{{ STATIC_URL }}home.css" rel="stylesheet" type="text/css" media="screen" />'
    index += '</head>\n<body>\n'
    index += '<br/>\n<br/>\n<div align="center">\n'
    global htmlRendrering
    tree = xml.parse("tar.xml")
    #Get the root node
    rootElement = tree.getroot()
    #print rootElement
    #Get a list of children elements with tag == "Books"
    screen = rootElement.findall("screen")
    i = 0
    if screen != None:
        for screen in screen:
            linkName = screen.find('name').text

            fileName = "html"
            djangoPurpose=fileName + str(i)
            viewsContent +='def ' + djangoPurpose + '(request):\n'
            fileName = fileName + str(i) + '.html'
            viewsContent += "\treturn render(request, 'rendering/"+fileName+"')\n\n"

            urlcontent += "url(r'rendering/" + djangoPurpose + "' , views." + djangoPurpose + " , name ='"+djangoPurpose+"'),\n"

            i += 1
            openScreenToPage()
            for child in screen:
                for component in child:
                    generateRendering(component)
            endScreenEndPage()
            file = open('mysite/webApp/templates/rendering/' + fileName, 'w')
            index += '<a href=\"rendering/'+ djangoPurpose + '\">' + linkName + "</a><br/>\n"
            file.write(htmlRendrering)
            file.close()
            print htmlRendrering
            newScreen()
        index += '</div></body>\n</html>\n'
        fileIndex = open('mysite/webApp/templates/index.html' , 'w')
        fileIndex.write(index)
        fileIndex.close()
        viewsFile.write(viewsContent)
        viewsFile.close()
        urlcontent += ")"
        urlsFile.write(urlcontent)
        urlsFile.close()
        ConfigureMysiteUrls()
























