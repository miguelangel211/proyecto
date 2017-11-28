from __future__ import unicode_literals
from django import template
from django.contrib.auth.models import Group,User
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.views.generic import CreateView, FormView, ListView, DetailView,UpdateView
from home.forms import Usuario_form, Cliente_form, Direccion_form,categoria_form,menu_form,tamano_form
from home.models import Usuario,Direcciones,menu,categoria,Cart,productocarro
from django.core.urlresolvers import reverse_lazy

register = template.Library()

@register.filter(name='to_cents')
def to_cents(value):
	return int(value * 100)

@register.filter(name='pluralize')
def pluralize(value):
	retval=""
	if value > 1:
		retval="s"
	return retval


@register.inclusion_tag('home/registrar_usuario.html',name='forma_cliente',takes_context=True)
def registrar_cliente(context):
	request = context['request']
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
	return ({"form":form})

@register.inclusion_tag('home/registrar_usuario.html',name='forma_repartidor',takes_context=True)
def registrar_repartidor(context):
	request = context['request']
	title="Registrar"
	form=Usuario_form(request.POST or None)
	if form.is_valid():
		user=form.save(commit=False)
		password = form.cleaned_data.get('password')
		groups = 'Repartidor'
		user.set_password(password)
		user.save()
		g=Group.objects.get(name=groups)
		g.user_set.add(user)
	return ({"form":form})

@register.inclusion_tag('home/direccion.html',name='forma_direccion',takes_context=True)
def registrar_direccion(context):
	request = context['request']
	title="direccion"
	form=Direccion_form(request.POST or None)
	if form.is_valid():
		dire=form.save(commit=False)
		dire.usuario=request.user
		dire.save()
	return ({"form":form})

@register.inclusion_tag('home/direccion.html',name='forma_categoria',takes_context=True)
def registrar_categoria(context):
	request = context['request']
	title="categorias"
	form=categoria_form(request.POST or None)
	if form.is_valid():
		dire=form.save(commit=False)
		dire.save()
	return ({"form":form})

@register.inclusion_tag('home/tamano.html',name='forma_tamano',takes_context=True)
def registrar_tamano(context,producto_id):
	request = context['request']
	title="categorias"
	form=tamano_form(request.POST or None)
	if form.is_valid():
		dire=form.save(commit=False)
		dire.articulo=menu.objects.get(pk=producto_id)
		dire.save()
	return ({"form":form})

@register.inclusion_tag('home/producto.html',name='forma_producto',takes_context=True)
def registrar_producto(context,id_categoria):
	p = categoria.objects.get(id=id_categoria)
	request = context['request']
	title="categorias"
	form=menu_form(request.POST or None,request.FILES)
	if form.is_valid():
		dire=form.save(commit=False)
		dire.categoria=p
		dire.save()
	return ({"form":form})

@register.inclusion_tag('home/detail.html',name='detail_direcciones',takes_context=True)
def show_direcciones(context):
	request=context['request']
	u=str(request.user.username)
	p = Direcciones.objects.raw('SELECT * FROM home_direcciones join auth_user on usuario_id=auth_user.id where auth_user.username= %s',[u])
	return{'direcciones':p}

@register.inclusion_tag('home/detail_cliente.html',name='detail_cliente',takes_context=True)
def show_datos_cliente(context):
	request=context['request']
	u=str(request.user.username)
	p = User.objects.raw('SELECT * FROM auth_user where auth_user.username= %s',[u])
	return{'cliente':p}


@register.inclusion_tag('home/detail_categorias.html',name='detail_categorias',takes_context=True)
def show_categorias(context):
	request=context['request']
	p = User.objects.raw('SELECT * FROM home_categoria')
	return{'categorias':p}

@register.inclusion_tag('home/detail_pedidos.html',name='detail_pedidos',takes_context=True)
def show_pedidos(context):
	request=context['request']
	p = Cart.objects.raw('SELECT * FROM home_cart where active=0 and user_id=%s',[request.user.id])
	return{'pedidos':p}

@register.inclusion_tag('home/detail_pedidos.html',name='detail_pedidos_todos',takes_context=True)
def show_pedidos(context):
	request=context['request']
	p = Cart.objects.raw('SELECT * FROM home_cart where active=0 and user_id=%s',[request.user.id])
	return{'pedidos':p}

@register.inclusion_tag('home/detail_productos.html',name='detail_producto',takes_context=True)
def show_productos(context,id_producto):
	u=id_producto
	request=context['request']
	p = menu.objects.raw('SELECT * FROM home_menu where home_menu.categoria_id=%s',[u])
	return{'productos':p}

@register.inclusion_tag('home/detail_tamano.html',name='detail_tamano',takes_context=True)
def show_tamano(context,id_producto):
	u=id_producto
	request=context['request']
	p = menu.objects.raw('SELECT * FROM home_tamanos where home_tamanos.articulo_id=%s',[u])
	return{'productos':p}

@register.inclusion_tag('home/detail_usuario.html',name='detail_usuario',takes_context=True)
def show_datos_usuarios(context):
	request=context['request']
	u='Repartidor'
	p = User.objects.raw('SELECT * FROM auth_user join auth_user_groups on auth_user.id=auth_user_groups.user_id join auth_group on auth_user_groups.group_id=auth_group.id where auth_group.name= %s',[u])
	return{'usuario':p}

@register.filter(name='detail_articulos')
def show_articulos(id_cart):
	p=productocarro.objects.raw('SELECT * FROM home_productocarro where cart_id=%s'[id_cart])
	return{'articulos':p}


@register.inclusion_tag('registrar_post.html',name='forma_post',takes_context=True)
def registrar_post(context):
	request = context['request']
	title="Registrar"
	form=comentario_form(request.POST or None)
	if form.is_valid():
		user=form.save(commit=False)
		user.usuario=request.user
		user.save()
	return ({"form":form})


@register.inclusion_tag('home/detail_posts.html',name='detail_posts',takes_context=True)
def show_post(context):
	request=context['request']
	u=str(request.user.id)
	p = Direcciones.objects.raw('SELECT * FROM home_comentario where usuario_id=%s',[u])
	return{'direcciones':p}