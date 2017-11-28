"""proyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import login, logout_then_login
from home import views 
from home.templatetags import forma
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index_view'),
    url(r'^registrar_usuario/$', views.registrar_usuario, name='registrar_usuario'),
    url(r'^registrar_cliente/$', views.registrar_cliente, name='registrar_cliente'),
    url(r'^login/$',login, {'template_name' : 'home/login.html'}, name='login'),
    url(r'^logout/$',logout_then_login, name='logout_view'),
    url(r'^administrador/$',views.administrador, name='administrador'),
    url(r'^menu/(\d+)$',views.Menu, name='menu'),
    url(r'^cliente/$',views.cliente, name='cliente_view'),
    url(r'^direcciones/$',views.direcciones, name='direcciones'),
    url(r'^datos_cliente/$',views.datos_cliente, name='datos_cliente'),
    url(r'^add/(\d+)/(\d+)',views.add_to_cart,name='add_to_cart'),
    url(r'^articulo/(\d+)',views.articulo,name='articulo'),
    url(r'^remove/(\d+)/(\d+)',views.remove_from_cart,name='remove_from_cart'),
    url(r'^clean',views.clean_cart,name='clean_cart'),
    url(r'^cart/',views.cart,name='cart'),
    url(r'^asignar_direccion',views.asignar_direccion,name='asignar_direccion'),
    url(r'delete_direccion/(?P<pk>[-\w]+)/$',views.requestDeleteView.as_view(),name='delete_direccion_view'),
    url(r'update_direccion/(?P<pk>[-\d]+)/$',views.Update_direccion.as_view(),name='update_direccion_view'),
    url(r'^producto_categorias/(?P<pk>[-\d]+)/$',views.producto_categorias,name='producto_categorias_view'),
    url(r'^tamanos_producto/(?P<pk>[-\d]+)/$',views.tamanos_producto,name='tamanos_producto_view'),
    url(r'^checkout/(\w+)',views.checkout,name='checkout'),
    url(r'^process/(\w+)',views.process_order,name='process_order'),
    url(r'^order_error/',views.order_error,name='order_error'),
    url(r'^lista_compras/(\d+)',views.lista_compras,name='lista_compras'),
    url(r'complete_order/(\w+)',views.complete_order,name='complete_order'),
    url(r'^add_direccion/(\d+)',views.add_direccion,name='add_direccion'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG is True:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)