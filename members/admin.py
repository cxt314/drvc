from django.contrib import admin
from .models import Member, MemberAlias

# Register your models here.
class MemberAliasInline(admin.StackedInline):
    model = MemberAlias
    extra = 1

class MemberAdmin(admin.ModelAdmin):
    fields = ["name", "email"]
    inlines = [MemberAliasInline]

admin.site.register(Member, MemberAdmin)