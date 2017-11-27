# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Direcciones,categoria,menu,tamanos,productocarro,Cart,ingredientes,comentario


admin.site.register(Direcciones)
admin.site.register(categoria)
admin.site.register(menu)
admin.site.register(tamanos)
admin.site.register(productocarro)
admin.site.register(Cart)
admin.site.register(ingredientes)
admin.site.register(comentario)
