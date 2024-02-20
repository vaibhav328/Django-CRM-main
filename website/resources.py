from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from .models import Product, ProductCategory
from import_export.admin import ImportExportModelAdmin



class ProductCategoryResource(resources.ModelResource):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'is_active')
        import_id_fields = ('name',)

class categoryadmin(ImportExportModelAdmin):
   resource_class = ProductCategoryResource


class ProductResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(ProductCategory, field='name'))
    def get_import_id_fields(self):
        return []
    class Meta:
        model = Product
        fields = ( 'category', 'name', 'description', 'cost', 'color', 'gender')
     
class productadmin(ImportExportModelAdmin):
   resource_class = ProductResource   
