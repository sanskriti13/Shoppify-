from typing import Type
from accounts.forms import RegistrationForm
from django.shortcuts import render,redirect
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


#Email Verification

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def register(request):
  if request.method =='POST':
    form=RegistrationForm(request.POST)
    if form.is_valid():
      first_name= form.cleaned_data['first_name']
      last_name= form.cleaned_data['last_name']
      email= form.cleaned_data['email']
      phone_number= form.cleaned_data['phone_number']
      password= form.cleaned_data['password']
      username= email.split("@")[0]
      

      user=Account.objects.create_user(first_name= first_name, last_name= last_name, email= email, username= username, password= password)
      user.phone_number= phone_number
      user.save()


      #USER AUTHENTICATION

      current_site= get_current_site(request)
      mail_subject= 'Please activate your account'
      message= render_to_string('accounts/account_verification.html',{
        'user':user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
      })
      to_email= email
      send_email= EmailMessage(mail_subject, message, to=[to_email])
      send_email.send()

      # messages.success(request,'Registration Successful. We have sent you an email for verification.')
      return redirect('/accounts/login/?command=verification&email='+email)
      return redirect('register')
  
  else:
      form= RegistrationForm()
  context={
    'form':form
  }
  return render(request,'accounts/register.html',context)


def login(request):
  if request.method =='POST':
    email= request.POST['email']
    print(email)
    username= Account.objects.get(email=email)
    password= request.POST['password']
    print(password)
    x= auth.authenticate(request,email= email, password= password)
    print(x)
    account= Account.objects.get(email=email)

    if x is not None :
      print('There is a user ')
      auth.login(request, x)
      messages.success(request,"You have successfully logged in! ")
      return redirect('dashboard')
    else:
      messages.error(request,'Invalid Login Credentials')
      return redirect('login')
  return render(request,'accounts/login.html')

@login_required(login_url= 'login')
def logout(request):
  auth.logout(request)
  messages.success(request, 'You are logged out! ')
  return redirect('login')


def activate(request,uidb64, token):
  try:
    uid= urlsafe_base64_decode(uidb64).decode()
    user= Account._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
    user=None
  
  if user is not None and default_token_generator.check_token(user, token):
    user.is_active= True
    user.save()
    messages.success(request, 'Congratulations your account stands verified and activated.')
    return redirect('login')
  else:
    messages.error(request, 'Invalid Activation Link')
    return redirect('register')


@login_required(login_url= 'login')
def dashboard(request):
  return render(request, 'accounts/dashboard.html')



def forgot(request):
  if request.method=='POST':
    email= request.POST['email']
    if Account.objects.filter(email=email).exists():
      user= Account.objects.get(email__exact=email)


      #Reset Password Email
      current_site= get_current_site(request)
      mail_subject= 'Reset Your Password'
      message= render_to_string('accounts/reset_validate.html',{
        'user':user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
      })


      to_email= email
      send_email= EmailMessage(mail_subject, message, to=[to_email])
      send_email.send()

      messages.success(request, 'Password reset email has been sent')
      return redirect('login')

    else:
      messages.error(request,'Account Does not exist')
      return redirect('forgot')


  return render(request,'accounts/forgot.html')

def reset_validate(request, uidb64, token):
  try:
    uid= urlsafe_base64_decode(uidb64).decode()
    user= Account.objects.get(pk=uid)
  except(TypeError, ValueError, OverflowError,Account.DoesNotExist):
    user= None
  if user is not None and default_token_generator.check_token(user, token):
    request.session['uid']=uid
    messages.success(request, 'Please reset your password')
    return redirect('reset')
  else:
    messages.error(request, 'The link has expired')
    return redirect('login')

def reset(request):
  if request.method=='POST':
    password =request.POST['password']
    con_pass = request.POST['confirm_password']
    if password == con_pass:
      uid=request.session['uid']
      user= Account.objects.get(pk=uid)
      user.set_password(password)
      user.save()
      messages.success(request,'Password has been reset')
      return redirect('login')
      
    else:
      messages.error(request,'Passwords do not match!')
      return redirect('reset')


  return render(request, 'accounts/reset.html')




# Create your views here.
