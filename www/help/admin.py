from django.contrib import admin
from help.models import Category, Command, Field, FieldType, Option, Library, RegistryHistory, JarFile


class FieldAdminInline(admin.TabularInline):
    model = Field
    extra = 0


class CommandAdmin(admin.ModelAdmin):
    search_fields = ('command',)
    inlines = (FieldAdminInline, )

class CommandDetailAdmin(admin.ModelAdmin):
    search_fields = ('command__command', 'command_short_description', 'command_explanation', 'command_example',)

class FieldAdmin(admin.ModelAdmin):
    search_fields = ('command__command', 'field_name',)



# Register your models here.
admin.site.register(Library)
admin.site.register(RegistryHistory)
admin.site.register(JarFile)
admin.site.register(Category)
admin.site.register(Command, CommandAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(FieldType)
admin.site.register(Option)