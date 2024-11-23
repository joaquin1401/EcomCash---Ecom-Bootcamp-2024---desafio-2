# renderizar una pagina html, redireccionara  auna pagina
from django.shortcuts import render, redirect

# funcion para autenticar provista por django, devuelve un user
# funcion login provista por django
from django.contrib.auth import authenticate, login as login_django


def prueba(request):
    lista_usuarios = [
        {"nombre": "joaquin", "apellido": "desza"},
        {"nombre": "ernesto", "apellido": "desza"},
        {"nombre": "camilo", "apellido": "desza"},
        {"nombre": "marcelino", "apellido": "desza"}

    ]
    contexto = {
        "usuario": "joaquiin jaja",
        "todos_los_usuarios": lista_usuarios
    }
    return render(request, "base.html", contexto)