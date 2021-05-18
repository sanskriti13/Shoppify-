from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from carts.models import Cart,CartItem
from django.http import HttpResponse





# We need the session ID to get the cart ID
# We will get the cart using the cart id

def _cart_id(request):
  cart= request.session.session_key
  if not cart:
    cart= request.session.create()
  return cart
  


def cart(request,quant=0,total=0,items=None):
  try:
    tax=0
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
  color= request.GET['color']
  size= request.GET['size']
  product= Product.objects.get(id=product_id)
  
  try:
    cart= Cart.objects.get(cart_id=_cart_id(request))
  except Cart.DoesNotExist:
    cart= Cart.objects.create(cart_id= _cart_id(request))
  cart.save()

  try:
    cart_item=CartItem.objects.get(cart= cart, product= product)
    cart_item.quantity+=1
    cart_item.save()
  except:
    cart_item=CartItem.objects.create(cart=cart,
    product= product,
    quantity=1,)
    cart_item.save()
  
  #Then we redirect to the cart page
  return redirect('cart')
  #It is going to take us to the view 'cart', and this will redirect to




def remove_cart(request,product_id):
  product= Product.objects.get(id=product_id)
  cart= Cart.objects.get(cart_id=_cart_id(request))
  cartitem= CartItem.objects.get(cart=cart,product=product)
  if cartitem.quantity >1 :
    cartitem.quantity-=1
    cartitem.save()
  else:
    cartitem.delete()
  return redirect('cart')




def remove_cart_item(request,product_id):
  product= get_object_or_404(Product,id=product_id)
  cart= Cart.objects.get(cart_id=_cart_id(request))
  cartitem= CartItem.objects.get(cart=cart,product=product)
  cartitem.delete()
  return redirect('cart')