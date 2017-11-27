from django import forms
from .models import Usuario,Direcciones,categoria,menu,tamanos,comentario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Usuario_form(forms.ModelForm):
	CATH_CHOICES=(
			('Gerencia','Gerencia'),
			('Cajero','Cajero'),
			('Repartidor','Repartidor'),
			)
	username=forms.CharField(label='Usuario')
	email=forms.EmailField(label='Correo')
	email2=forms.EmailField(label='comfirmar correo')
	password=forms.CharField(label='contrasena',widget=forms.PasswordInput)
	password2=forms.CharField(label='confirmar contrasena',widget=forms.PasswordInput)
	first_name=forms.CharField(label='Nombre')
	last_name=forms.CharField(label='Apellidos')
	def __init__(self,*args,**kwargs):
		super(Usuario_form,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
				})
	class Meta:
		model = User
		fields = [
		'username',
		'email','email2',
		'password','password2',
		'first_name',
		'last_name',
		]
	def clean(self):
		email=self.cleaned_data.get('email')
		email2=self.cleaned_data.get('email2')
		password=self.cleaned_data.get('password')
		password2=self.cleaned_data.get('password2')
		password2=self.cleaned_data.get('password2')
		if email != email2:
			raise forms.ValidationError("Los correos no coinciden")
		if password != password2:
			raise forms.ValidationError("Las contrasenas no coinciden")
		return self.cleaned_data
	
class Cliente_form(forms.ModelForm):

	username=forms.EmailField(label='Correo')
	email=forms.EmailField(label='comfirmar correo')
	password=forms.CharField(label='contrasena',widget=forms.PasswordInput)
	password2=forms.CharField(label='confirmar contrasena',widget=forms.PasswordInput)
	first_name=forms.CharField(label='Nombre')
	last_name=forms.CharField(label='Apellidos')
	def __init__(self,*args,**kwargs):
		super(Cliente_form,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
				})
	class Meta:
		model = User
		fields = [
		'username',
		'email',
		'password','password2',
		'first_name',
		'last_name',
		]
	def clean(self):
		username=self.cleaned_data.get('username')
		email=self.cleaned_data.get('email')
		password=self.cleaned_data.get('password')
		password2=self.cleaned_data.get('password2')
		password2=self.cleaned_data.get('password2')
		if username != email:
			raise forms.ValidationError("Los correos no coinciden")
		if password != password2:
			raise forms.ValidationError("Las contrasenas no coinciden")
		return self.cleaned_data

class Direccion_form(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		super(Direccion_form,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
				})
	class Meta:
		model=Direcciones
		fields=[
		'calle',
		'numero_exterior',
		'numero_interior',
		'cp',
		'colonia',
		'referencias',
		]
	
class categoria_form(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		super(categoria_form,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
				})
	class Meta:
		model=categoria
		fields="__all__"

class tamano_form(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		super(tamano_form,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
				})
	class Meta:
		model=tamanos
		fields=[
		'tamano',
		'precio',
		'descripcion',
		]

class menu_form(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		super(menu_form,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
				})
	class Meta:
		model=menu
		fields=[
		'articulo',
		'precio',
		'imagen',
		]

class comentario_form(forms.ModelForm):
	post=forms.CharField(widget=forms.Textarea(attrs={'cols':80,'rows':3}))
	def __init__(self,*args,**kwargs):
		super(comentario_form,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class':'form-control'
				})
	class Meta:
		model= comentario
		fields=[
		'post',
		]