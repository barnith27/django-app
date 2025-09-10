from http.client import responses

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView

from .models import Profile

class AboutMeView(UpdateView):
    model = Profile
    fields = ['avatar']
    template_name = 'myauth/about-me.html'
    success_url = reverse_lazy('myauth:about-me')

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response

def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('myauth:login'))

class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')

class UsersProfile(ListView):
    model = Profile
    template_name = 'myauth/users-profile.html'
    context_object_name = 'profiles'

class UserDetailView(DetailView):
    template_name = 'myauth/user-details.html'
    model = Profile
    context_object_name = 'profile'

class UserUpdateView(UpdateView):
    model = User
    fields = 'first_name', 'last_name', 'email'
    template_name = 'myauth/user_update_form.html'

    def get_success_url(self):
        return reverse('myauth:users-profile')

class ProfileUpdateView(UpdateView):
    model = Profile
    fields = 'avatar', 'bio'
    template_name = 'myauth/profile_update_form.html'

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        profile, created = Profile.objects.get_or_create(user=user)
        return profile

    def get_success_url(self):
        return reverse('myauth:users-profile')

@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value: {value!r}')

@permission_required('myauth.view_profile', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Session set!')

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'Session value: {value!r}')