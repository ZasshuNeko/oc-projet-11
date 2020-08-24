from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import Edit, SearchMenu

# Create your views here.


@login_required(login_url="/auth_app/log_in/")
def get_compte(request, user_name):
    ''' Affiche le compte de l'utilisateur
    Displays user account '''
    user_current = request.user

    login = user_current.username
    first_name = user_current.first_name
    last_name = user_current.last_name
    email = user_current.email

    name = affiche_nom(first_name, last_name, login)
    data_compte = {'email': email, 'name': name}

    return render(
        request, 'compte.html', {
            'formMenu': SearchMenu(), 'data': data_compte})


@login_required(login_url="/auth_app/log_in/")
def edit_compte(request, username):
    ''' Permet d'éditer le compte utilisateur
    Allows you to edit the user account '''
    user_current = request.user

    default_data = {
        "last_name": user_current.last_name,
        "first_name": user_current.first_name,
        "email": user_current.email}

    form = Edit(default_data)

    return render(
        request, 'compte_edit.html', {
            'formMenu': SearchMenu(), 'form': form})


@login_required(login_url="/auth_app/log_in/")
def edit_valide(request, username):
    ''' Est appelé quand l'édition d'un compte est valide
    Is called when the edition of an account is valid '''

    user_current = request.user

    if request.method == 'POST':
        form = Edit(request.POST)
        email = request.POST['email']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        pass_first = request.POST['pass_first']
        pass_second = request.POST['pass_second']

        password = False
        if pass_first == pass_second:
            if len(pass_first) > 0:
                password = True
                pass_final = pass_first


        user_current.email = email
        user_current.last_name = last_name
        user_current.first_name = first_name

        if password:
            user_current.set_password(pass_final)
            user_current.save()
            messages.add_message(
                    request,
                    messages.INFO,
                    "Mot de passe modifié ! Reconnectez-vous")
        elif len(pass_first) > 0:
            messages.add_message(
                request,
                messages.INFO,
                "Vos mots de passe sont différents ! Enregistrement annulé")
        else:

            user_current.save()
            messages.add_message(
                    request,
                    messages.INFO,
                    "Vos informations ont été modifiées")
        
    name = affiche_nom(
        user_current.first_name,
        user_current.last_name,
        user_current.username)

    data_compte = {
        'email': user_current.email,
        'name': name,
        'formMenu': SearchMenu()}

    url_redirect = '/compte/get_compte/' + user_current.username + '/'

    return HttpResponseRedirect(url_redirect, data_compte)


def affiche_nom(first_name, last_name, login):

    if first_name == "" and last_name == "":
        name = login
    elif first_name != "" and last_name == "":
        name = first_name
    elif first_name == "" and last_name != "":
        name = last_name
    elif first_name != "" and last_name != "":
        name = first_name + " " + last_name
    else:
        name = "Incognito"

    return name
