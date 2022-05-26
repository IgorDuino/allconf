from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class ProfileForm(UserChangeForm):
    username = None
    password = None

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
