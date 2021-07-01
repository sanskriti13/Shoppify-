from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,Variation
from carts.models import Cart,CartItem
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required





# We need the session ID to get the cart ID
# We will get the cart using the cart id

def _cart_id(request):
  cart= request.session.session_key
  if not cart:
    cart= request.session.create()
  return cart
  


def cart(request,quant=0,total=0,grand=0,items=None):
  try:
    tax=0
    if request.user.is_authenticated:
      items= CartItem.objects.filter(user=request.user, is_active=True)
    else:
      cart=Cart.objects.get(cart_id= _cart_id(request))
      items= CartItem.objects.filter(cart=cart,is_active=True)
    for i in items:
      quant+= i.quantity
      total+= (i.product.price * i.quantity)
    tax= (total*2)/100
    grand=tax+total
  except ObjectDoesNotExist:
    pass

  context={
    'total':total,
    'quant':quant,
    'items':items,
    'tax':tax,
    'grand':grand,

  }
  
    
  return render(request,'store/cart.html',context)



# Add a particular product to the cart
def add_cart(request, product_id):
  current_user= request.user
  product= Product.objects.get(id=product_id)
  #if the user is authenticated
  if current_user.is_authenticated:
    product_variation=[]
    if request.method=='POST':
      for item in request.POST:
        key= item
        value= request.POST[key]
        print(key,value)
        

        try:
          variation= Variation.objects.get(product=product, var_cat__iexact =key, var_value__iexact= value)
          print(variation,'HI')
          product_variation.append(variation)
        except:
          print('Did not get')
          pass



    is_cart_item_exists=CartItem.objects.filter(product=product, user=current_user).exists()


    if is_cart_item_exists:
      cart_item=CartItem.objects.filter(user=current_user, product= product)
      ex_var_list=[]
      id=[]

      for item in cart_item:
        existing_variation= item.variation.all()
        ex_var_list.append(list(existing_variation))
        id.append(item.id)

      if product_variation in ex_var_list:
        index= ex_var_list.index(product_variation)
        item_id= id[index]
        item= CartItem.objects.get(product=product, id=item_id,user=current_user)
        item.quantity+=1
        item.save()
      
      else:
        item= CartItem.objects.create(product=product, user=current_user, quantity=1)
        if len(product_variation)>0:
          item.variation.clear()
          item.variation.add(*product_variation)
        item.save()
    
    else:
      cart_item= CartItem.objects.create(product=product, user=current_user, quantity=1)
      if len(product_variation)>0:
        cart_item.variation.clear()
        cart_item.variation.add(*product_variation)
      cart_item.save()

    
    #Then we redirect to the cart page
    return redirect('cart')
    #It is going to take us to the view 'cart', and this will redirect to

  else:
    
    product_variation=[]
    if request.method=='POST':
      for item in request.POST:
        key= item
        value= request.POST[key]
        print(key,value)
        

        try:
          variation= Variation.objects.get(product=product, var_cat__iexact =key, var_value__iexact= value)
          print(variation,'HI')
          product_variation.append(variation)
        except:
          print('Did not get')
          pass


    
    
    try:
      cart= Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
      cart= Cart.objects.create(cart_id= _cart_id(request))
    cart.save()


    is_cart_item_exists=CartItem.objects.filter(product=product, cart=cart).exists()


    if is_cart_item_exists:
      cart_item=CartItem.objects.filter(cart= cart, product= product)
      ex_var_list=[]
      id=[]

      for item in cart_item:
        existing_variation= item.variation.all()
        ex_var_list.append(list(existing_variation))
        id.append(item.id)

      if product_variation in ex_var_list:
        index= ex_var_list.index(product_variation)
        item_id= id[index]
        item= CartItem.objects.get(product=product, id=item_id,cart=cart)
        item.quantity+=1
        item.save()
      
      else:
        item= CartItem.objects.create(product=product, cart=cart, quantity=1)
        if len(product_variation)>0:
          item.variation.clear()
          item.variation.add(*product_variation)
        item.save()
    
    else:
      cart_item= CartItem.objects.create(product=product, cart=cart, quantity=1)
      if len(product_variation)>0:
        cart_item.variation.clear()
        cart_item.variation.add(*product_variation)
      cart_item.save()

    
    #Then we redirect to the cart page
    return redirect('cart')
    #It is going to take us to the view 'cart', and this will redirect to




def remove_cart(request,product_id,cart_item_id):
  product= Product.objects.get(id=product_id)
  
  try:
    if request.user.is_authenticated:
      cartitem= CartItem.objects.get(product=product, user=request.user,id=cart_item_id)
    else:
      cart= Cart.objects.get(cart_id=_cart_id(request))
      cartitem= CartItem.objects.get(cart=cart,product=product,id=cart_item_id)
    if cartitem.quantity >1 :
      cartitem.quantity-=1
      cartitem.save()
    else:
      cartitem.delete()
  except:
    pass

  return redirect('cart')




def remove_cart_item(request,product_id,cart_item_id):
  product= get_object_or_404(Product,id=product_id)
  if request.user.is_authenticated:
    cartitem=CartItem.objects.get(user=request.user, product=product, id=cart_item_id )
  else:
    cart= Cart.objects.get(cart_id=_cart_id(request))
    cartitem= CartItem.objects.get(id=cart_item_id, cart=cart, product=product)
  cartitem.delete()
  return redirect('cart')


@login_required(login_url='login')
def checkout(request,quant=0,total=0,grand=0):
  try:
    tax=0
    items= None
    cart=Cart.objects.get(cart_id= _cart_id(request))
    items= CartItem.objects.filter(cart=cart,is_active=True)
    for i in items:
      quant+= i.quantity
      total+= (i.product.price * i.quantity)
    tax= (total*2)/100
    grand=tax+total
  except ObjectDoesNotExist:
    pass

  context={
    'total':total,
    'quant':quant,
    'items':items,
    'tax':tax,
    'grand':grand,

  }
  return render(request,'store/checkout.html',context)