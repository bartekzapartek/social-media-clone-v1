from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
       

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # for fieldname in ['password2']:
        self.fields['password2'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None

        self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True, 'placeholder': 'enter the username'})
        self.fields['password1'].widget.attrs.update({'placeholder':'enter the password'})
        self.fields['password2'].widget.attrs.update({'placeholder':'confirm the password'})
                                                                          

   
        