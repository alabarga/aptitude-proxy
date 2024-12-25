from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Registro, Tema, Paciente, Visita, _NO_YES_U
from .models import Pregunta, Evaluacion, Cuestionario, Componente, Opcion, Intervencion
from aptitude_crd import models
from admin_ordering.admin import OrderableAdmin
from suit_redactor.widgets import RedactorWidget

from import_export.admin import ExportActionMixin
from django import forms
from profile.models  import Profile

class AgeRangeFilter(admin.SimpleListFilter):
    title = 'is_very_benevolent'
    parameter_name = 'is_very_benevolent'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(benevolence_factor__gt=75)
        elif value == 'No':
            return queryset.exclude(benevolence_factor__gt=75)
        return queryset


class UserProfileInline(admin.StackedInline):
    model = Profile
    verbose_name_plural = 'Información adicional'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Tema)
class TemasAdmin(admin.ModelAdmin):
    pass


@admin.register(Registro)
class RegistroAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'email', 'rango_edad',)
    list_filter = ('sexo',)
    filter_horizontal = ('temas', )


class ComponenteInline(admin.StackedInline):
    model = Componente
    extra = 0

class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 0


class ComponenteForm(forms.ModelForm):
    model = Componente
    class Meta:
        widgets = {
            'descripcion': RedactorWidget(editor_options={'lang': 'es'})
        }

@admin.register(Componente)
class ComponenteAdmin(admin.ModelAdmin):
    form = ComponenteForm
    list_display = ('cuestionario', 'nombre', 'order', )
    list_filter = ('cuestionario',)
    inlines = [OpcionInline, ]

class CuestionarioForm(forms.ModelForm):
    model = Cuestionario
    class Meta:
        widgets = {
            'descripcion': RedactorWidget(editor_options={'lang': 'es'})
        }

@admin.register(Cuestionario)
class CuestionarioAdmin(admin.ModelAdmin, OrderableAdmin):
    form = CuestionarioForm
    inlines = [ComponenteInline, ]
    ordering_field = 'order'
    list_display = ('nombre', 'dominio', 'order', 'activo', )
    list_editable = ('order', 'dominio', 'activo',)


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('componente', 'valor', )

@admin.register(Intervencion)
class IntervencionAdmin(admin.ModelAdmin):
    pass

@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    list_display = ('componente','nombre',)

class EntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        print("EntryForm")
        if hasattr(self.instance, 'componente'):
            print(self.instance)
            if self.instance.componente.tipo == 'LIST':
                lista = getattr(models,self.instance.componente.lista)
                self.fields['valor'] = forms.ChoiceField(choices=lista)
        else:
            print("Empty form")
        # self.fields['valor'].widget = forms.RadioSelect()

    class Meta:
        model = Pregunta
        fields = ['valor', ]

class EntryInline(admin.TabularInline):
    model = Pregunta
    fields = ['valor', ]
    form = EntryForm
    extra = 0

class EntradaInline(admin.TabularInline):
    model = Pregunta
    fields = ['componente', ]
    show_change_link = False
    extra = 0

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'visita', 'cuestionario']
    list_filter = ['cuestionario__nombre', 'completada', 'visita__user__username', 'visita__fecha']
    search_fields = ['visita__paciente__codigo', 'visita__fecha', ]
    readonly_fields=['paciente', 'puntuacion',]

    inlines = [EntryInline, ]
    view_on_site = True

    def puntuacion(self, obj):
        return obj.puntuacion

    def paciente(self, obj):
        return obj.visita.paciente

class EvaluacionInline(admin.TabularInline):
    model = Evaluacion
    show_change_link = False
    extra = 0
    list_display = ()

@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    inlines = [EvaluacionInline, ]
    filter_horizontal = ('cuestionarios',)
    view_on_site = True

class PacienteForm(forms.ModelForm):
    # internet  = forms.ChoiceField(choices=_NO_YES_U, widget=forms.RadioSelect)
    class Meta:
        model = Paciente
        fields = ('__all__')
        # widgets = {
        #     'internet': forms.RadioSelect(),
        #  }

class VisitaInline(admin.StackedInline):
    model = Visita
    show_change_link = True
    extra = 0

@admin.register(Paciente)
class PacienteAdmin(ExportActionMixin, admin.ModelAdmin):
    form = PacienteForm
    list_display = ('codigo', 'sexo', 'fecha_nacimiento',)
    search_fields = ('codigo', )
    list_filter = ('sexo',)
    inlines = [VisitaInline, ]
