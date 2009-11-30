from django import forms
from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.db.models import DoesNotExist

from echo.models import UserProfile

class RegistrationForm(forms.Form):
    firstName = forms.CharField(max_length=80, 
                                label='First Name',
                                error_messages={
                                    'required' : 'Please provide your first name'
                                })
    lastName = forms.CharField(max_length=80, 
                               label='Last Name',
                               error_messages={
                                     'required' : 'Please provide your last name'
                               })
    email = forms.EmailField(label='Email Address',
                             error_messages={
                                'required' : 'You must provide a valid email address'
                             })
    username = forms.CharField(max_length=20, 
                               label='Username',
                               required=False,
                               help_text="If you don't specify a username, your email address will be used.")
                               
    company = forms.CharField(max_length=50,
                              label='Company',
                              required=False)
                               
    
    def saveUnvalidatedUser(self):
        if self.is_valid():
            random_pass = User.objects.make_random_password()
            if self.cleaned_data['username']:
                usr = self.cleaned_data['username']
            else:
                usr = self.cleaned_data['email']
                
            newuser = User.objects.create_user(usr,self.cleaned_data['email'],random_pass)
            newuser.is_active = False
            newuser.first_name = self.cleaned_data['firstName']
            newuser.last_name = self.cleaned_data['lastName']
            newuser.save()
            try:
                p = newuser.get_profile()
                p.company = self.cleaned_data['company']
                p.save()
            except SiteProfileNotAvailable, DoesNotExist:
                pass
            self.emailPassword(random_pass)
            
    def emailPassword(self, newpassword):
        if self.is_valid():
            subject = 'Complete your registration...'
            from_email = 'rob@openecho.org'
            to = self.cleaned_data['email']
            activation_url = reverse('/confirmRegistration')
            
            text_content = 'Your temporary password is %s' % newpassword
            html_content = '<p>Your temporary password is %s. <a href="%s">Click here to activate your account</a></p>' % newpassword, activation_url
            
            msg = EmailMultiAlternatives(subject,text_content,from_email,[to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
class ConfirmRegistration(forms.Form):
    password1 = forms.CharField(max_length=20,
                                label='Password',
                                error_messages={
                                    'required' : 'You must provide a password'
                                },
                                widget=PasswordInput(render_value=False))
                                
    password2 = forms.CharField(max_length=20,
                                label='Repeat Password',
                                error_messages={
                                    'required' : 'You must type your password twice'
                                },
                                widget=PasswordInput(render_value=False))
                                
    activation_key = forms.CharField(max_length=50,
                                     widget=HiddenInput())
    
    user_name = forms.CharField(max_length=50,
                                widget=HiddenInput())
                                
    def validateUserRegistration(self):
        if self.is_valid():
            u = User.objects.get(username=self.cleaned_data['user_name'])
            if not u:
                raise DoesNotExist
            else:
                u.is_active = True
                u.set_password(self.cleaned_data['password1'])
                u.save()
    
    def clean(self):
        cleaned_data = self.cleaned_data
        pass1 = cleaned_data.get("password1")
        pass2 = cleaned_data.get("password2")
        
        if pass1 and pass2: 
            #that is, only bother if the fields themselves have validated...
            if pass1 <> pass2:
                raise forms.ValidationError("Passwords must match!")
        
        return cleaned_data