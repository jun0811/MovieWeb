from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserCrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name',)


class CustomUserChangeForm(UserChangeForm):

    password = None

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)