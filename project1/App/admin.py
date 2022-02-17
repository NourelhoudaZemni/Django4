from django.contrib import admin, messages

# Register your models here.

# definir les models qui seront

from .models import Etudiant, Coach, Projet, MemberShipInProject
# un decorateur il doit etre sur la classe
# TabularInline /stackedInline par rapport inlines pour appeler la classe
# tabular tableau  stacked liste
class MemberShip(admin.TabularInline):
    model=MemberShipInProject
    extra = 1
@admin.register(Projet)
# creer des personalisations  de l entite projet dans la classe
class ProjetAdmin(admin.ModelAdmin):
    inlines = (MemberShip,)
    list_display = (
    'nom_projet', 'duree_projet', 'temps_alloue_par_projet', 'besoin', 'description', 'est_valide', 'createur',)
    fieldsets = (
        ('A propos', {'fields': ('nom_projet', 'besoin', 'description')}),
        ('Etat', {'fields': ('est_valide',)}),
        ('Durée', {'fields': ('duree_projet', 'temps_alloue_par_projet')}),
        (None, {'fields': ('createur', 'superviseur')})
    )
    list_per_page = 2
    def set_to_valid(self,request,queryset):
        queryset.update(est_valide=True)
    set_to_valid.short_description='Validate'


    actions = ['set_to_valid','set_to_no_valide']
    def set_to_no_valide(self,request,queryset):
        row_no_valid=queryset.filter(est_valide=False)
        if(row_no_valid.count()>0):
            messages.error(request,"%s this article are already no valid "%row_no_valid.count())
        else:
            a=queryset.update(est_valide=False)
            if(a!=0):
                messages.success(request,"%s project was updated "%a)

    actions_on_bottom = True
    actions_on_top = False
    list_filter = ('est_valide','createur')
    search_fields = ['nom_projet']
admin.site.register(Etudiant)
admin.site.register(Coach)

