from django.contrib import admin
from .models import Member, MemberAlias

# Inline for MemberAlias within Member
# This allows adding/editing aliases directly from the Member form
class MemberAliasInline(admin.TabularInline):
    model = MemberAlias
    extra = 1 # How many empty forms to display
    fields = ('name',)


# --- ModelAdmin for each model ---

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'updated_at')
    search_fields = ('name', 'email')
    inlines = [MemberAliasInline] # Show aliases directly under a member
    readonly_fields = ('created_at', 'updated_at')

# @admin.register(MemberAlias)
# class MemberAliasAdmin(admin.ModelAdmin):
#     list_display = ('name', 'member')
#     search_fields = ('name', 'member__name')
#     list_filter = ('member',)