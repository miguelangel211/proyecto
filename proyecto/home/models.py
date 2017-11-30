# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User,Group
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
# Create your models here.
class sucursal(models.Model):
	sucursal=models.CharField(max_length=30)
	nombre=models.CharField(max_length=30)
	calle=models.CharField(max_length=30)
	numero_exterior=models.CharField(max_length=30)
	numero_interior=models.CharField(max_length=30,blank=True,null=True)
	Referencias=models.CharField(max_length=100,blank=True,null=True)
	cp=models.CharField(max_length=30)
	colonia=models.CharField(max_length=30)
	telefono=models.CharField(max_length=15)
	imagen=models.ImageField(upload_to='sucursal')
	def url(self):
			if self.ofertas and hasattr(self.ofertas, 'url'):
				return self.ofertas.url


class Usuario(models.Model):
	usuario = models.OneToOneField(User, on_delete=models.CASCADE)
	edad = models.PositiveIntegerField(blank=True,null=True)
	telefono = models.CharField(max_length=15,blank=True,null=True)
	celular=models.CharField(max_length=15,blank=True,null=True)


class repartidor(models.Model):
	usuario=models.OneToOneField(User, on_delete=models.CASCADE)
	trabajando=models.BooleanField(default=False)
	disponibilidad=models.BooleanField(default=False)

class caja_repartidor(models.Model):
	usuario=models.OneToOneField(User, on_delete=models.CASCADE)
	def add_to_caja(self,cart_id):
		cart=Cart.objects.get(pk=cart_id)
		cart.algo="Enviado"
		cart.caja=self
		cart.save()
	def remove_from_caja(self,cart_id):
		cart=Cart.objects.get(pk=cart_id)
		try:
			cart.caja=None
			cart.algo="proceso"
			cart.save() 
		except:
			pass

class Direcciones(models.Model):
	alias=models.CharField(max_length=50,null=True)
	usuario = models.ForeignKey(User,on_delete=models.CASCADE)
	calle=models.CharField(max_length=100)
	numero_exterior=models.CharField(max_length=30)
	numero_interior=models.CharField(max_length=30,blank=True,null=True)
	referencias=models.CharField(max_length=30,blank=True,null=True)
	cp=models.CharField(max_length=30)
	colonia=models.CharField(max_length=30)

class categoria(models.Model):
	nombre= models.CharField(max_length=30,unique=True)
	imagen=models.ImageField(null=True)
	def url(self):
		if self.imagen and hasattr(self.imagen, 'url'):
			return self.imagen.url	

class menu(models.Model):
	categoria=models.ForeignKey(categoria,on_delete=models.CASCADE,default=True)
	articulo= models.CharField(max_length=30)
	descripcion=models.CharField(max_length=100,null=True)
	precio=models.PositiveIntegerField(default=0)
	imagen=models.ImageField(upload_to='menu')
	combinada=models.BooleanField(default=False)
	def __unicode__(self):
		return self.articulo
	def url(self):
		if self.imagen and hasattr(self.imagen, 'url'):
			return self.imagen.url


class tamanos(models.Model):
	articulo=models.ForeignKey(menu,on_delete=models.CASCADE)
	tamano=models.CharField(max_length=200)
	precio=models.PositiveIntegerField()
	descripcion=models.CharField(max_length=200)
class pedido(models.Model):
	num_pedido=models.PositiveIntegerField(unique=True)
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	estado=models.PositiveIntegerField()
	costo=models.DecimalField(max_digits=9, decimal_places=2)






#class ofertas(models.Model):
#	oferta=models.PositiveIntegerField()
#	Descripcion=models.CharField(max_length=500)
#	imagen=models.ImageField(upload_to='ofertas')
#	def url(self):
#			if self.ofertas and hasattr(self.ofertas, 'url'):
#				return self.ofertas.url
class vehiculo(models.Model):
	numero=models.CharField(max_length=12)
	modelo=models.CharField(max_length=13)
	estado=models.CharField(max_length=30)

class Cart(models.Model):
	user= models.ForeignKey(User)
	active= models.BooleanField(default=True)
	order_date = models.DateField(null=True)
	payment_type=models.CharField(max_length=100,null=True)
	payment_id= models.CharField(max_length=100,null=True)
	order_date=models.DateTimeField(null=True)
	total=models.PositiveIntegerField(null=True)
	direccion=models.ForeignKey(Direcciones,null=True)
	algo=models.CharField(max_length=34,null=True)
	caja=models.ForeignKey(caja_repartidor,null=True)
	fallo=models.CharField(max_length=200,null=True)
	def add_to_cart(self,producto_id,id_tamano):
		producto=menu.objects.get(pk=producto_id)
		tamano=tamanos.objects.get(pk=id_tamano)
		try:
			preexisting_order=productocarro.objects.get(producto=producto,cart=self,tamano=tamano)
			preexisting_order.cantidad +=1
			preexisting_order.save()
		except productocarro.DoesNotExist:
			new_order=productocarro.objects.create(
				producto=producto,
				tamano=tamano,
				cart=self,
				cantidad=1,
				)
			new_order.save()
	def remove_from_cart(self, producto_id,id_tamano):
		producto=menu.objects.get(pk=producto_id)
		tamano=tamanos.objects.get(pk=id_tamano)
		try:
			preexisting_order = productocarro.objects.get(producto=producto, cart=self,tamano=tamano)
			if preexisting_order.cantidad > 1:
				preexisting_order.cantidad -=1
				preexisting_order.save()
			else:
				preexisting_order.delete()
		except productocarro.DoesNotExist:
			pass

	def add_to_cart_combinada(self,producto_id,id_tamano):
		producto=menu.objects.get(pk=producto_id)
		tamano=tamanos.objects.get(pk=id_tamano)
		try:
			preexisting_order=productocarro.objects.get(producto=producto,cart=self,tamano=tamano)
			preexisting_order.cantidad +=1
			preexisting_order.save()
		except productocarro.DoesNotExist:
			new_order=productocarro.objects.create(
				producto=producto,
				tamano=tamano,
				cart=self,
				cantidad=1,
				)
			new_order.save()

	def add_direccion(self,direccion):
		dire=Direcciones.objects.get(id=direccion)
		self.direccion=dire
		self.save()


class pedido_repartidor(models.Model):
	Usuario=models.ForeignKey(User, on_delete=models.CASCADE)
	cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)

class productocarro(models.Model):
	producto=models.ForeignKey(menu)
	tamano=models.ForeignKey(tamanos,null=True)
	cart=models.ForeignKey(Cart)
	cantidad=models.PositiveIntegerField()


class ingredientes(models.Model):
	menu=models.ForeignKey(menu,on_delete=models.CASCADE)
	productocarro=models.ForeignKey(productocarro,on_delete=models.CASCADE,null=True)



class comentario(models.Model):
	usuario=models.ForeignKey(User)
	cart=models.ForeignKey(Cart,null=True)
	post=models.CharField(max_length=400)
	parent=models.ForeignKey('self',null=True,blank=True)
	timestamp=models.DateTimeField(auto_now_add=True,null=True)
	def children(self):
		return comentario.objects.filter(parent=self)
	def is_parent(self):
		if self.parent is not None:
			return False
		return True