# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Group,User
from django.shortcuts import render,redirect
from django.views.generic import CreateView, FormView, ListView, DetailView,UpdateView,DeleteView
from .forms import Usuario_form, Cliente_form, comentario_form,menu_form,tamano_form
from .models import *
from django.core.urlresolvers import reverse_lazy,reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import paypalrestsdk,stripe
from django.http import JsonResponse
# Create your views here.
def checkout(request,processor):
	if request.user.is_authenticated():
		cart=Cart.objects.filter(user=request.user.id,active=True)
		orders =productocarro.objects.filter(cart=cart)
		total=0
		for order in orders:
			total+=((order.producto.precio+order.tamano.precio)*order.cantidad)
		if processor=="paypal":
			redirect_url = checkout_paypal(request,cart,orders)
			return redirect(redirect_url)
		elif processor =="stripe":
			token=request.POST['stripeToken']
			status = checkout_stripe(cart,orders,token)
			if status:
				return redirect(reverse('process_order',args=['stripe']))
			else:
				return redirect('order_error',context={"message":"Ha habido un problema con el proceso de tu pago"})
		elif processor=="efectivo":
			cart=Cart.objects.get(user=request.user.id,active=True)
			cart.active=False
			cart.order_date=timezone.now()
			cart.payment_type="efectivo"
			cart.total=total
			cart.algo="proceso"
			cart.save()
			return redirect('index_view')
	else:
		return redirect('index_view')


def checkout_paypal(request,cart,orders):
	if request.user.is_authenticated():
		items=[]
		total=0
		for order in orders:
			total += ((order.producto.precio+order.tamano.precio)*order.cantidad)
			articulo=order.producto
			item={
			'name': articulo.articulo,
			'sku': articulo.categoria.nombre,
			'price':str(articulo.precio+order.tamano.precio),
			'currency':'MXN',
			'quantity': order.cantidad,
			}
			items.append(item)

		paypalrestsdk.configure({
		"mode":"sandbox",
		"client_id":"Abyp2qG0EBt29VGd8UHLnxcqBaEyrMOlXyMOIsuxzcA0jy8Mj4G5i5FdrqeJ-wKsibuPyzTKOpU3eqsu",
		"client_secret":"ENUeag1x2HvYJiP0EjcDovLAmnsEzoEFwseOV7Q1Rfjqc8DTWipsehR6anEzaFpGWSsBh_W_FzjhP9r5"})
		payment = paypalrestsdk.Payment({
			"intent": "sale",
			"payer":{
			"payment_method":"paypal"},
			"redirect_urls":{
			"return_url":"http://localhost:8000/process/paypal",
			"cancel_url":"http://localhost:8000/cart"},
			"transactions":[{
			"item_list":{
			"items":items},
			"amount":{
			"total": str(total),
			"currency":"MXN"
			},
			"description":"orden"
			}
			]
			})
		if payment.create():
			cart_instance = cart.get()
			cart_instance.payment_id=payment.id
			cart_instance.save()
			for link in payment.links:
				if link.method == "REDIRECT":
					redirect_url=(str(link.href))
					return redirect_url
		else:
			return reverse("order_error")
	else:
		return redirect('index_view')

def order_error(request):
	if request.user.is_authenticated():
		return render(request,'home/order_error.html')
	else:
		return redirect('index_view')

def process_order(request, processor):
	if request.user.is_authenticated():
		if processor == "paypal":
			payment_id=request.GET.get('paymentId')
			cart=Cart.objects.filter(payment_id=payment_id)
			orders = productocarro.objects.filter(cart=cart)
			total=0
			for order in orders:
				total+=((order.producto.precio+order.tamano.precio)*order.cantidad)
			context ={
			'cart':orders,
			'total':total,
			}
			return render(request,'home/process_order.html',context)
		elif processor == "stripe":
			return JsonResponse({'redirect_url':reverse('complete_order',args=['stripe'])})

	else:
		return redirect('index_view')

def complete_order(request, processor):
	if request.user.is_authenticated():
		cart=Cart.objects.get(user=request.user.id,active=True)
		orders = productocarro.objects.filter(cart=cart)
		total=0
		for order in orders:
			total+=((order.producto.precio+order.tamano.precio)*order.cantidad)
		if processor=='paypal':
			payment=paypalrestsdk.Payment.find(cart.payment_id)
			if payment.execute({"payer_id":payment.payer.payer_info.payer_id}):
				message="Tu orden se ha completado Payment ID:%s"%(payment.id)
				cart.active=False
				cart.order_date=timezone.now()
				cart.payment_type="paypal"
				cart.total=total
				cart.algo="proceso"
				cart.save()
				
			else:
				message = "Ha habido un problema en la transaccion. Error: %s"%(payment.error.message)
			context={
				'message':message,
				}
			return render(request,'home/order_complete.html',context)
		elif processor == 'stripe':
			cart.active=False
			cart.order_date = timezone.now()
			cart.payment_type="stripe"
			cart.total=total
			cart.algo="proceso"
			cart.save()
			message=message="Tu orden se ha completado Payment ID:%s"%(cart.payment_id)
			context={
				'message':message,
				}
			return render(request,'home/order_complete.html',context)
	else:
		return redirect('index_view')


def checkout_stripe(cart,orders,token):
	stripe.api_key ="sk_test_Xzz6rkykp79JcN4P0toC9qZJ"
	total=0
	for order in orders:
		total +=((order.producto.precio+order.tamano.precio)*order.cantidad)
	status=True
	try:
		charge = stripe.Charge.create(
			amount=int(total*100),
			currency="MXN",
			source=token,
			metadata={'order_id':cart.get().id}
			)
		cart_instance = cart.get()
		cart_instance.payment_id=charge.id
		cart_instance.save()
	except stripe.error.CardError as e:
		status=False
	return status


class requestDeleteView(DeleteView):
	model=Direcciones
	success_url='/cliente/#direcciones'
class delete_usuario(DeleteView):
	model=User
	success_url='/administrador/'
class delete_categoria(DeleteView):
	model=categoria
	success_url='/administrador/#menu'
class delete_producto(DeleteView):
	model=menu
	success_url='/administrador/#menu'

class delete_tamano(DeleteView):
	model=tamanos
	success_url='/administrador/#menu'

def index(request):
	p=categoria.objects.raw('SELECT * FROM home_categoria')
	return render(request,'home/index.html',{'categoria':p})

def Menu(request,categoria_id):
	p=menu.objects.raw('SELECT * from home_menu where home_menu.categoria_id=%s',[categoria_id])
	return render(request,'home/menu.html',{'menu':p})

def articulo(request,id_articulo):
	articulo=menu.objects.get(pk=id_articulo)
	p=tamanos.objects.raw('SELECT * from home_tamanos where articulo_id =%s',[id_articulo])
	ingredientes = menu.objects.raw('SELECT * from home_menu where categoria_id=%s',[articulo.categoria.id])
	context={
	'tamano':p,
	'articulo':articulo,
	'ingredientes':ingredientes
	}
	return render(request,'home/articulo.html',context)

def add_to_cart(request,producto_id,tamano_id):
	if request.user.is_authenticated():
		try:
			producto = menu.objects.get(pk=producto_id)
			tamano=tamanos.objects.get(pk=tamano_id)
		except ObjectDoesNotExist:
			pass
		else:
			try:
				cart=Cart.objects.get(user=request.user, active=True)
			except ObjectDoesNotExist:
				cart=Cart.objects.create(
					user=request.user
				)
				cart.save()
			cart.add_to_cart(producto_id,tamano_id)
		return redirect('cart')
	else:
		return redirect('index_view')

def clean_cart(request):
	if request.user.is_authenticated():
		cart=Cart.objects.get(user=request.user.id,active=True)
		orders =productocarro.objects.filter(cart=cart)
		for order in orders:
			cart.remove_from_cart(order.producto_id,order.tamano_id)
		return redirect('cart')
	else:
		return redirect('index_view')
def remove_from_cart(request,producto_id,tamano_id):
	if request.user.is_authenticated():
		try:
			producto=menu.objects.get(pk=producto_id)
			tamano=tamanos.objects.get(pk=tamano_id)
		except ObjectDoesNotExist:
			pass
		else:
			cart=Cart.objects.get(user=request.user,active=True)
			cart.remove_from_cart(producto_id,tamano_id)
		return redirect('cart')
	return redirect('index_view')

def add_direccion(request,direccion):
	if request.user.is_authenticated():
		cart=Cart.objects.get(user=request.user,active=True)
		cart.add_direccion(direccion)
		return redirect('cart')
	else:
		return redirect('index_view')

def cart(request):
	if request.user.is_authenticated():
		try:
			cart=Cart.objects.get(user=request.user.id, active=True)
		except ObjectDoesNotExist:
			return redirect('index_view')
		if not cart.direccion:
			return redirect('asignar_direccion')
		else:
			orders = productocarro.objects.filter(cart=cart)
			total=0
			count=0
			for order in orders:
				total +=((order.producto.precio+order.tamano.precio) * order.cantidad)
				count += order.cantidad
			context={
			'cart': orders,
			'total':total,
			'count': count,
			'carrito':cart,
			}
			return render(request,'home/cart.html',context)
	else:
		return redirect('index_view')





def producto_categorias(request,pk):
	p = categoria.objects.get(id=pk)
	form=menu_form(request.POST or None,request.FILES)
	if form.is_valid():
		dire=form.save(commit=False)
		dire.categoria=p
		dire.save()
	return render(request,'home/productos.html',{'pk':pk})

def tamanos_producto(request,pk):
	p=menu.objects.get(id=pk)
	form=tamano_form(request.POST or None)
	if form.is_valid():
		dire=form.save(commit=False)
		dire.articulo=p
		dire.save()
	return render(request,'home/tamanos.html',{'pk':pk})

def direcciones(request):
	u=str(request.user.username)
	p = Direcciones.objects.raw('SELECT * FROM home_direcciones join auth_user on usuario_id=auth_user.id where auth_user.username= %s',[u])
	return render(request,'home/detail.html',{'direcciones':p})

def datos_cliente(request):
	u=str(request.user.username)
	p = User.objects.raw('SELECT * FROM auth_user where auth_user.username= %s',[u])
	return render(request,'home/detail_cliente.html',{'cliente':p})

def cliente(request):
	name=None
	first_name=None
	last_name=None
	if request.user.is_authenticated():
		username = request.user.username
		fisrt_name=request.user.first_name
		last_name=request.user.last_name
	form=comentario_form(request.POST or None)
	if form.is_valid():
		post=form.save(commit=False)
		carro=Cart.objects.get(pk=request.POST.get("cart"))
		post.usuario=request.user
		post.cart=carro
		post.save()
	context = {
	"email":username,
	"nombre":first_name,
	"apellido":last_name,
	"form":form
	}
	return render(request,'home/cliente.html',context)

def registrar_usuario(request):
	if not request.user.groups.filter(name='administrador'):
		return redirect('index_view')

	title="Registrar"
	form=Usuario_form(request.POST or None)
	if form.is_valid():
		user=form.save(commit=False)
		password = form.cleaned_data.get('password')
		groups = form.cleaned_data.get('groups')
		user.set_password(password)
		user.save()
		g=Group.objects.get(name=groups)
		g.user_set.add(user)
	return render(request, 'home/registrar_usuario.html',{"form":form})

def administrador(request):
	if request.user.groups.filter(name="administrador"):
		form=Usuario_form(request.POST or None)
		if form.is_valid():
			user=form.save(commit=False)
			password = form.cleaned_data.get('password')
			groups = request.POST.get('grupo','')
			user.set_password(password)
			user.save()
			if groups=="Repartidor":
				caja_repartidor.objects.create(usuario=user)
				repartidor.objects.create(usuario=user)
			g=Group.objects.get(name=groups)
			g.user_set.add(user)
		return render(request,'home/administrador.html')
	else:
		return redirect('cajero')



def registrar_cliente(request):
	title="Registrar"
	form=Cliente_form(request.POST or None)
	if form.is_valid():
		user=form.save(commit=False)
		password = form.cleaned_data.get('password')
		groups = 'Cliente'
		user.set_password(password)
		user.save()
		g=Group.objects.get(name=groups)
		g.user_set.add(user)
		return redirect('login')
	return render(request, 'home/registrar_cliente.html',{"form":form})

class Update_direccion(UpdateView):
	template_name="home/update_direccion.html"
	model = Direcciones
	fields=[
		'calle',
		'numero_exterior',
		'numero_interior',
		'cp',
		'colonia',
		'referencias',
		]
	success_url=reverse_lazy("cliente_view")

class Update_cliente(UpdateView):
	template_name="home/update_cliente.html"
	model = User
	fields=[
		'username',
		'first_name',
		'last_name',
		'password',
		]
	success_url=reverse_lazy("cliente_view")

class Update_repartidor(UpdateView):
	template_name="home/update_cliente.html"
	model = User
	fields=[
		'first_name',
		'last_name',
		'password',
		'email'
		]
	success_url=reverse_lazy("administrador")

class Update_categoria(UpdateView):
	template_name="home/update_cliente.html"
	model = categoria
	fields="__all__"
	success_url=reverse_lazy("administrador/#menu")

class Update_producto(UpdateView):
	template_name="home/update_cliente.html"
	model = menu
	fields="__all__"
	success_url=reverse_lazy("administrador/#menu")

class Update_tamano(UpdateView):
	template_name="home/update_cliente.html"
	model = tamanos
	fields="__all__"
	success_url=reverse_lazy("administrador/#menu")


def asignar_direccion(request):
	p=Direcciones.objects.filter(usuario=request.user)
	return render(request,'home/asignar_direccion.html',{'direcciones':p})

def lista_compras(request,id_cart):
	p=productocarro.objects.raw('SELECT * FROM home_productocarro where cart_id=%s',[id_cart])
	return render(request,'home/detail_articulos.html',{'articulos':p})
def cajero(request):
	if request.user.groups.filter(name="Cajero"):
		grupo='Repartidor'
		p=User.objects.raw('SELECT * FROM auth_user join auth_user_groups on auth_user.id=user_id join auth_group on group_id=auth_group.id where auth_group.name=%s',[grupo])
		context={
		'repartidores':p
		}
		return render(request,'home/cajero.html',context)
	else:
		return redirect('repartidor')

def add_to_caja(request,id_repartidor,id_cart):
	if request.user.is_authenticated():
		us=User.objects.get(pk=id_repartidor)
		caja=caja_repartidor.objects.get(usuario=us)
		caja.add_to_caja(id_cart)
		return redirect('cajero')
	else:
		return redirect('index_view')

def remove_from_caja(request,id_cart):
	if request.user.is_authenticated():
		cart=Cart.objects.get(pk=id_cart)
		cart.algo="proceso"
		cart.caja=None
		cart.save()
		return redirect('cajero')
	else:
		return redirect('index_view')

def completar_orden(request,id_cart):
	if request.user.is_authenticated():
		cart=Cart.objects.get(pk=id_cart)
		cart.algo="completado"
		cart.caja=None
		cart.save()
		return redirect('repartidor')
	else:
		return redirect('cajero')

def problema_orden(request,id_cart):
	if request.user.is_authenticated():
		cart=Cart.objects.get(pk=id_cart)
		cart.algo="fallo"
		cart.caja=None
		cart.save()
		return redirect('repartidor')
	else:
		return redirect('cajero')



def repartidor(request):
	if request.user.groups.filter(name="Repartidor"):
		q=caja_repartidor.objects.get(usuario=request.user)
		recibido='Enviado'
		p = Cart.objects.filter(caja=q,active=0,algo="Enviado")
		return render(request,'home/repartidor.html',{'pedidos':p})
	else:
		return redirect('cliente_view')

def hilo(request,id_post):
	if request.user.is_authenticated():
		com=comentario.objects.get(pk=id_post)
		form=comentario_form(request.POST or None)
		if form.is_valid():
			post=form.save(commit=False)
			post.usuario=request.user
			try:
				papa=comentario.objects.get(pk=request.POST.get("parent_id"))
				post.parent=papa
			except:
				pass
			post.save()
		context={
		"form":form,
		"p":com
		}
		return render(request,'home/hilo.html',context)
	else:
		return redirect('index')