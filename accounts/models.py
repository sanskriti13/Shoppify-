from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from datetime import datetime


class AccManager(BaseUserManager):
  def create_user(self,first_name,last_name,username,email,password=None):
    if not email:
      raise ValueError('Must enter the email ID')

    if not username:
      raise ValueError('Must enter the username')

    user= self.model(
      email=self.normalize_email(email),
      username=username,
      first_name=first_name,
      last_name=last_name,
    )

    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self,first_name,last_name,email,username,password):
    user= self.create_user(
      email=self.normalize_email(email),
      username=username,
      password=password,
      first_name=first_name,
      last_name=last_name,
    )

    user.is_admin=True
    user.is_staff=True
    user.is_active=True
    user.is_superadmin=True
    user.save(using=self._db)
    return user



class Account(AbstractBaseUser):
  first_name= models.CharField(max_length=70)
  last_name= models.CharField(max_length=70)
  username= models.CharField(max_length=70,unique=True)
  email= models.EmailField(unique=True)
  phone_number= models.IntegerField(blank=True,null=True)

  #required fields
  date_joined=models.DateTimeField(auto_now_add=True)
  last_login =models.DateTimeField(auto_now_add=True)


  is_admin= models.BooleanField(default=False)
  is_active= models.BooleanField(default=False)
  is_staff= models.BooleanField(default=False)
  is_superadmin= models.BooleanField(default=False)

  USERNAME_FIELD='email'
  #To specify what is going to be used as the username
  REQUIRED_FIELDS= ['username','first_name','last_name',]
  #To specify the required fields

  objects= AccManager()

  def __str__(self):
    return self.email

  def has_perm(self,perm,obj=None):
    return self.is_admin
  
  def has_module_perms(self,add_label):
    return True

