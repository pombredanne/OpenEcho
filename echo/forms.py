from django import forms
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

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
            self.emailPassword(random_pass)
            
    def emailPassword(self, newpassword):
        if self.is_valid():
            subject = 'Complete your registration...'
            from_email = 'rob@openecho.org'
            to = self.cleaned_data['email']
            
            text_content = 'Your temporary password is %s' % newpassword
            html_content = '<p>Your temporary password is %s</p>' % newpassword
            
            msg = EmailMultiAlternatives(subject,text_content,from_email,[to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()