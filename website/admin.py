from django.contrib import admin
from .models import *
from .resources import *
from import_export.admin import ImportExportActionModelAdmin

admin.site.register(Record)
admin.site.register(Consumer)
admin.site.register(Dealer)
admin.site.register(ProductCategory,categoryadmin)
admin.site.register(Product,productadmin)
admin.site.register(Order)
admin.site.register(UserProfile)
# admin.site.register(categoryadmin)
# admin.site.register(productadmin)
