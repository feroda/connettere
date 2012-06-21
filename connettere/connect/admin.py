from django.contrib import admin

from connect.models import AThing,AGroup,WeightedThing


class WeightedThingInLine(admin.TabularInline):
    model = WeightedThing
    extra = 1

######################MODEL-ADMIN###########################

class AGroupAdmin(admin.ModelAdmin):
    inlines = (WeightedThingInLine,)

class AThingAdmin(admin.ModelAdmin):
    inlines = (WeightedThingInLine,)


admin.site.register(AThing,AThingAdmin)
admin.site.register(AGroup,AGroupAdmin)
