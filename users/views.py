import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from .models import Users
from .forms import LoginForm, RegistrationForm, ResumeForm
import hashlib
from django.views.generic import DetailView, UpdateView
from datetime import date
from django.template.loader import get_template
from django.template import Context
import pdfkit


def index(request):
    if 'user_id' not in request.session or request.session['user_id'] is None:
        return HttpResponseRedirect(reverse_lazy("login"))
    else:
        user = Users.objects.filter(id=request.session['user_id']).values()
        if user[0]['name'] is None or user[0]['name'] == "":
            return redirect(reverse('resume_update', args=(user[0]['id'],)))
        else:
            return redirect('resume', pk=user[0]['id'])


def login(request):
    data = {'error': ""}
    if request.method == 'POST':
        info = request.POST
        form = LoginForm(request.POST)
        user = Users.objects.filter(login=info['login']).values()
        if form.is_valid() and len(user) > 0 and user[0]['password'] == hashlib.md5(
                info['password'].encode()).hexdigest():
            request.session['user_id'] = user[0]['id']
            return redirect('resume', pk=user[0]['id'])
        else:
            data['error'] = "Неправильный логин или пароль"

    form = LoginForm()
    data['form'] = form
    return render(request, 'users/login.html', data)


def register(request):
    data = {}
    data['error'] = ""
    if request.method == 'POST':
        info = request.POST
        form = RegistrationForm(request.POST)
        data['error'] = info
        user = Users.objects.filter(login=info['login']).values()
        if len(user) > 0:
            data['error'] = "Пользователь с таким логином уже существует"
        elif info['password'] != info['repeat_password']:
            data['error'] = "Пароли не совпадают"
        elif form.is_valid():
            new_user = Users(login=info['login'], password=hashlib.md5(info['password'].encode()).hexdigest())
            new_user.save()
            user = Users.objects.filter(login=info['login']).values()
            request.session['user_id'] = user[0]['id']
            return redirect(reverse('resume_update', args=(user[0]['id'],)))
        else:
            data['error'] = "Ошибка ввода данных"

    form = RegistrationForm()
    data['form'] = form
    return render(request, 'users/register.html', data)


class UsersDetailView(DetailView):
    model = Users
    template_name = 'users/resume.html'

    def age(self, birthdate):
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

    def get(self, *args, **kwargs):
        if 'user_id' not in self.request.session or self.kwargs['pk'] != self.request.session['user_id']:
            return HttpResponseRedirect(reverse_lazy("login"))
        context = {}
        context["users"] = Users.objects.filter(id=self.request.session['user_id']).values()[0]
        if context['users']['name'] == "" or context['users']['name'] is None:
            return super(UsersDetailView, self).get(self, *args, **kwargs)
        return super(UsersDetailView, self).get(self, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = {}
        context["users"] = Users.objects.filter(id=self.request.session['user_id']).values()[0]
        if context["users"]['birth_date'] != "" and context["users"]['birth_date'] is not None:
            context["users"]['age'] = self.age(context["users"]['birth_date'])

        template = get_template("users/resume_pdf.html")
        context = {}
        context["users"] = Users.objects.filter(id=self.request.session['user_id']).values()[0]
        if context["users"]['birth_date'] != "" and context["users"]['birth_date'] is not None:
            context["users"]['age'] = self.age(context["users"]['birth_date'])
        html = template.render(context)
        filename = 'resume' + str(self.request.session['user_id']) + '.pdf'
        pdf = pdfkit.from_string(html, 'personal/static/personal/' + filename)
        context["users"]['filename'] = filename
        return context


class UsersUpdateView(UpdateView):
    model = Users
    template_name = 'users/resume_update.html'
    form_class = ResumeForm

    def get(self, *args, **kwargs):
        if 'user_id' not in self.request.session or self.kwargs['pk'] != self.request.session['user_id']:
            return HttpResponseRedirect(reverse_lazy("login"))
        context = {}
        context["users"] = Users.objects.filter(id=self.request.session['user_id']).values()[0]
        if context['users']['name'] == "" or context['users']['name'] is None:
            return super(UsersUpdateView, self).get(self, *args, **kwargs)
        return super(UsersUpdateView, self).get(self, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'update_resume' in request.POST:
            info = request.POST
            info_pic = ResumeForm(request.POST, request.FILES)
            if info_pic.is_valid():
                info_pic.save()
            profile_pic = Users.objects.latest('id').profile_pic
            Users.objects.filter(id=self.request.session['user_id']).update(name=info['name'],
                                                                            last_name=info['last_name'],
                                                                            birth_date=info['birth_date'],
                                                                            login=info['login'], about=info['about'],
                                                                            github_link=info['github_link'],
                                                                            phone_number=info['phone_number'],
                                                                            specialization=info['specialization'],
                                                                            email=info['email'],
                                                                            telegram=info['telegram'],
                                                                            profile_pic=profile_pic)
            return HttpResponseRedirect(reverse_lazy("resume", args=(self.request.session['user_id'],)))
        else:
            return HttpResponse("121")
