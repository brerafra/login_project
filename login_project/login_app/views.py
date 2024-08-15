from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from datetime import datetime
from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import User

class SignupView(FormView):
    #Signup view for our Custom User
    form_class = forms.SignupForm
    template_name = 'signup.html'
    success_url = reverse_lazy('dashboard')


    def form_valid(self, form):
        user = form.save(commit=False)
        now = datetime.now()

        #Creating an unique user using name+year+month+day+hour+min+second
        user_temp= user.name+str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
        user.user = user_temp
        user.is_staff = False
        user.save()
        login(self.request, user)
        if user is not None:
            return HttpResponseRedirect(self.success_url)

        return super().form_valid(form)


def Dashboard(request):
    #Dashboard where we can see all the actived users sessions

    active_sessions = Session.objects.filter(expire_date__gte = timezone.now())
    user_active_list =[]
    for session in active_sessions:
        data = session.get_decoded()
        user_active_list.append(data.get('_auth_user_id', None))

    usuarios = User.objects.filter(id__in=user_active_list)
    context = {
        'active_users':usuarios,
    }
    return render(request, 'dashboard.html', context=context)


def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('dashboard'))


class LoginView(FormView):

    form_class = forms.LoginForm
    success_url = reverse_lazy('dashboard')
    template_name = 'login.html'

    def form_valid(self, form):
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.INFO, 'Credenciales incorrectas\
                                Por favor intentelo de nuevo')
            return HttpResponseRedirect(reverse_lazy('login_app:login'))