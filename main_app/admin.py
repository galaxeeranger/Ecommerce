from django.contrib import admin
from .models import *
from django.utils.html import format_html


class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']

admin.site.register(Customer, CustomerModelAdmin)                     # to register model with fields in admin panel


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'contents', 'price', 'category', 'Photos', 'edit_product']
    # readonly_fields = ('Photos',) # list can also be used in place of tuple
    # fields = ('title', 'content')  # to show perticular fields on Edit field
    # exclude = ('title',)  # to hide perticular fields on Edit field
    # list_display = ['title', 'contents', "Photos" , 'edit_blog', 'history'] # to show fields on list view
    # list_display_links = ['title', 'contents'] # set a link to edit page
    list_filter = ['category', 'brand']  # for empty contents ('created_at' , admin.EmptyFieldListFilter)
    search_fields = ['title', 'brand'] # search by title
    # radio_fields = ('tags': admin.VERTICAL) # to show choices for radio fields in (VERTICAL --, HORIZONTAL |)
    # save_on_top = True # to show save buttons on top
    list_per_page = 5


    def contents(self, obj):
        return format_html(f'<span>{obj.description[:10]}</span>')  # slice character of cotent - useing html for styleing

    def price(self, obj):
        return format_html(f'<span style="text-align:right;">{obj.discounted_price}</span>')  # slice character of cotent - useing html for styleing

    def edit_product(self, obj):
        return format_html(f'<a href="/admin/main_app/product/{obj.id}/change/">edit</a>') 

    

    def Photos(self, obj):
        return format_html(f'<a href="/media/{obj.product_image}" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-images" viewBox="0 0 16 16"><path d="M4.502 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/><path d="M14.002 13a2 2 0 0 1-2 2h-10a2 2 0 0 1-2-2V5A2 2 0 0 1 2 3a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v8a2 2 0 0 1-1.998 2zM14 2H4a1 1 0 0 0-1 1h9.002a2 2 0 0 1 2 2v7A1 1 0 0 0 15 11V3a1 1 0 0 0-1-1zM2.002 4a1 1 0 0 0-1 1v8l2.646-2.354a.5.5 0 0 1 .63-.062l2.66 1.773 3.71-3.71a.5.5 0 0 1 .577-.094l1.777 1.947V5a1 1 0 0 0-1-1h-10z"/></svg></a>')

admin.site.register(Product, ProductModelAdmin) 


class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

admin.site.register(Cart, CartModelAdmin)

class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'oreder_date', 'status']

admin.site.register(OrderPlaced, OrderPlacedModelAdmin)
