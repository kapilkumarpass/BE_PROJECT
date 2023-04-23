from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
 
 
# class SignUpForm(UserCreationForm): 
#     class Meta: 
#         model = User 
#         fields = ('username','email', 'password1', 'password2', ) 
class SignUpForm(UserCreationForm): 
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs.update({ 
            'class': 'form-input form-control', 
            'required':'', 
            'name':'username', 
            'id':'username', 
            'type':'text', 
            'placeholder':'enter username', 
            'maxlength': '16', 
            'minlength': '6', 
            }) 
        self.fields['email'].widget.attrs.update({ 
            'class': 'form-input form-control', 
            'required':'', 
            'name':'email', 
            'id':'email', 
            'type':'email', 
            'placeholder':'enter email', 
            }) 
        self.fields['password1'].widget.attrs.update({ 
            'class': 'form-input form-control', 
            'required':'', 
            'name':'password1', 
            'id':'password1', 
            'type':'password', 
            'placeholder':'enter password', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 
        self.fields['password2'].widget.attrs.update({ 
            'class': 'form-input form-control', 
            'required':'', 
            'name':'password2', 
            'id':'password2', 
            'type':'password', 
            'placeholder':'re-enter password', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 
    class Meta: 
        model = User 
        fields = ('username', 'email', 'password1', 'password2',)
        
class LogInForm(AuthenticationForm): 
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs.update({ 
            'class': 'form-input form-control', 
            'required':'', 
            'name':'username', 
            'id':'username', 
            'type':'text', 
            'placeholder':'enter username', 
            'maxlength': '16', 
            'minlength': '6', 
            }) 
        
        self.fields['password'].widget.attrs.update({ 
            'class': 'form-input form-control', 
            'required':'', 
            'name':'password1', 
            'id':'password1', 
            'type':'password', 
            'placeholder':'enter password', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 
        
    class Meta: 
        model = User 
        fields = ('username','password')
        
class loginForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=10)
    
    def clean_email(self):
        email=self.cleaned_data['email']
        if '@aitpune.edu.in' not in email:
            raise forms.ValidationError("Emails from aitpune.edu.in are allowed")
        return email
    
    
    


    
