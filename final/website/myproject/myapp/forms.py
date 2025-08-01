from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User
from .models import Customer , ContactMessage

class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message'] 

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus' : 'True', 'class' : 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    password2 = forms.CharField(label='confirm password',widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class MyPasswordChangeForm(PasswordChangeForm):  
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'autofocus' : 'True', 'autocomplete':'current-password' ,'class' : 'form-control'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={ 'autocomplete':'current-password' ,'class' : 'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password' ,'class' : 'form-control'}))      

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))




class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={ 'autocomplete':'current-password' ,'class' : 'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password' ,'class' : 'form-control'}))      


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields=['name','locality','city','mobile','state','zipcode']
        widgets={
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
        }

def custom_password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            print("Email entered for password reset:", email)
            form.save(
                request=request,
                email_template_name='myapp/password_reset_email.html'
            )
    else:
        form = PasswordResetForm()
    return render(request, 'myapp/password_reset.html', {'form': form})


