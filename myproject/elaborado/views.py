from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from models import Table
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def login(request):
    if request.user.is_authenticated():
        message = "You're: " + request.user.username
        link = "/admin/logout/"
        name = "Logout"
    else:
        message = "You aren't registred"
        link = "/admin/"
        name = "Login"
    return (message, link, name, request.user.username)


def all(request):
    (message, link, name, user) = login(request)
    list = Table.objects.all()
    template = get_template("index.html")
    c = Context({'contenido': "Todos tus numeros son:",
                 'lista': list,
                 'recurso': "Numeros guardados",
                 'mensaje_out': message,
                 'link_out': link,
                 'name_out': name})
    return HttpResponse(template.render(c))


@csrf_exempt
def address(request, peticion, recurso):
    if request.method == "GET":
        if peticion == "agenda":
            list = Table.objects.filter(name=recurso)
            if not list:
                address = "Not found: " + recurso
            else:
                address = ""
                for i in list:
                    address += i.name + ": " + i.address
        if peticion == "css":
            try:
                out = Table.objects.get(name=recurso)
                out = out.address
            except ObjectDoesNotExist:
                #css por defecto
                out = ("body {" +
                       "margin: 10px 20% 50px 70px;" +
                       "font-family: sans-serif;" +
                       "color: black;" +
                       "background: white;" +
                       "}")
            return HttpResponse(out, content_type='text/css')
    if request.method == "PUT":
        if request.user.is_authenticated():
            new = Table(name=recurso, address=request.body)
            new.save()
            address = ("Saved Page, check it with GET")
        else:
            address = ("You must be registred")
    (message, link, name, user) = login(request)
    template = get_template("index.html")
    c = Context({'address': address,
                 'mensaje_out': message,
                 'link_out': link,
                 'name_out': name})
    return HttpResponse(template.render(c))


def notfound(request, recurso):
    out = ("Not found: " + recurso)
    return HttpResponseNotFound(out)
