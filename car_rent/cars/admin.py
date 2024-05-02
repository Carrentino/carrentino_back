from django.contrib import admin

from .models import *


class BrandPhotoInline(admin.TabularInline):
    model = BrandPhoto


class BrandAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    inlines = [BrandPhotoInline,]


admin.site.register(Brand, BrandAdmin)


class CarModelPhotoInline(admin.TabularInline):
    model = CarModelPhoto


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'type_of_fuel', 'hp')
    search_fields = ('title', 'brand.title')
    list_filter = ('hp', 'type_of_fuel')
    inlines = [CarModelPhotoInline, ]


admin.site.register(CarModel, CarModelAdmin)

admin.site.register(Car)
