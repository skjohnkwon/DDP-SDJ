from django.contrib import admin
from .models import Item, Comment

class CommentInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = Comment
    extra = 1  # This determines the number of empty forms presented in the interface.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [CommentInline]

admin.site.register(Comment)
