from django.contrib import admin
from .models import Item, Comment

class CommentInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = Comment
    extra = 1

class ItemInLine(admin.TabularInline):
    model = Item
    extra = 1

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [CommentInline]

admin.site.register(Comment)

