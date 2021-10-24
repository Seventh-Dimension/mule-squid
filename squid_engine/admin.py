from django.contrib import admin
from .models import *
from django.forms import TextInput, Textarea

class RuleAdmin(admin.ModelAdmin):
    save_as_continue = False
    list_display = ('Name','Description','Gatekeeper','Location')
    list_filter = ('Gatekeeper',)
    radio_fields = {'Gatekeeper':admin.HORIZONTAL}
    search_fields = ['Name']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '50','style':'height:1.5em;'})},
    }
    fieldsets = (
        ('Rule Details',{
        'description':'Please provide Rule details such as name, Proper Description to be shown in the result, Criticality value and the path to scan the particular XPath condition',
        'classes':('wide',),
        'fields':('Name','Description','Gatekeeper','Location')
        }),
        ('Rule Condition',{
            'classes':('wide'),
            'fields':(('Condition','Comparator','Expected_Value'),)
        })
    )

class RuleAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Description', 'Gatekeeper', 'Location')
    search_fields = ['Name']

class LevelAdmin(admin.ModelAdmin):
    filter_horizontal = ('Rules',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ("Name","Value")

admin.site.site_header= "SQUID ADMIN"
admin.site.register(Code_Rule,RuleAdmin)
admin.site.register(Security_Rule,RuleAdmin)
admin.site.register(Folder_Structure_Rule,RuleAdmin)
admin.site.register(Raml_Rule,RuleAdmin)
admin.site.register(Platform_Rule,RuleAdmin)
admin.site.register(Location)
admin.site.register(Gatekeeper)
admin.site.register(Level,LevelAdmin)
admin.site.register(Rule,RuleAdmin)
