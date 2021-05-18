from django.db import models
from django.db.models.fields import BooleanField
from category.models import Category
from django.urls import reverse
# Create your models here.


class Product(models.Model):
  product_name=models.CharField(max_length=70,unique=True)
  slug=models.SlugField(max_length=100,unique=True)
  description= models.TextField(max_length=255,blank=True)
  price= models.IntegerField()
  images=models.ImageField(upload_to='photos/products')
  stock= models.IntegerField()
  is_available= models.BooleanField(default=True)
  category=models.ForeignKey(Category, on_delete=models.CASCADE)
  created_date= models.DateTimeField(auto_now_add=True)
  modified_date= models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.product_name

  def get_url(self):
    return reverse('product_detail',args=[self.category.slug, self.slug])
    #adding name


variation_cat_choice=(
  ('color','color'),
  ('size','size'),

)


class Variation(models.Model):
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  var_cat= models.CharField(max_length=70,choices=variation_cat_choice)
  var_value= models.CharField(max_length=70)
  is_active=models.BooleanField(default=True)
  created_date= models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.product.product_name