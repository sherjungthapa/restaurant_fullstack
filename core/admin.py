from django.contrib import admin
from .models import Category,Momo,Review
# Register your models here.
admin.site.register(Category)

@admin.register(Momo)
class MomoAdmin(admin.ModelAdmin):
    list_display=['id','name','desc','price']

admin.site.register(Review)
