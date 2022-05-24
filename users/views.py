from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from users.forms import SignupForm, ProfileForm


User = get_user_model()


class SignupView(View):
    form_class = SignupForm
    template_name = 'users/signup.html'

    def get(self, request):
        form = self.form_class()

        context = {
            'form': form
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            repeat_password = form.cleaned_data['password2']

            user = User.objects.filter(username=username)

            if len(user) == 0:
                if password == repeat_password:
                    User.objects.create_user(username=username, email=email, password=password)

        context = {
            'form': form
        }

        return render(request, template_name=self.template_name, context=context)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    form_class = ProfileForm
    template_name = 'users/profile.html'
    
    @staticmethod
    def get_queryset(request):
        user = User.objects.filter(id=request.user.id)

        return user[0]

    def get(self, request):
        form = self.form_class()

        context = {
            'form': form,
            'user': self.get_queryset(request)
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            birthday = form.cleaned_data['birthday']
            form.save()

            profile = request.user.profile
            profile.birthday = birthday
            profile.save(update_fields=['birthday'])

        context = {
            'form': form,
            'user': self.get_queryset(request)
        }

        return render(request, template_name=self.template_name, context=context)