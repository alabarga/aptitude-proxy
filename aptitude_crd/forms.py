from django import forms
from django.forms import SelectDateWidget, HiddenInput
from .models import Evaluacion, Pregunta, Componente, Registro
from django.utils.translation import gettext as _

from registration.forms import RegistrationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Paciente

_COMP_TYPES = (
    ('TEXT', _("Texto")),
    ('NUM', _("Numérico")),
    ('VAL', _("Lista_Valor")),
	('LIST', _("Lista")),
    ('CALC', _("Calculado")),
    )

# Field classes for all available field types.
_FIELD_CLASSES = {
    'TEXT': forms.CharField,
    'NUM': forms.FloatField,
    'VAL': forms.ChoiceField,
    'LIST': forms.ChoiceField,
    'EMAIL': forms.EmailField,
    'CHECKBOX': forms.BooleanField,
    'MULTIPLE': forms.MultipleChoiceField,
    'CHECKBOX_MULTIPLE': forms.MultipleChoiceField,
    'SELECT_MULTIPLE': forms.MultipleChoiceField,
    'FILE': forms.FileField,
    'DATE': forms.DateField,
    'DATE_TIME': forms.DateTimeField,
    'DOB': forms.DateField,
    'HIDDEN': forms.CharField,
    'NUMBER': forms.FloatField,
    'URL': forms.URLField,
}

_DOMINIOS = {
     'cognition_alert': 'Deterioro cognitivo', 
     'nutrition_alert': 'Nutrición deficiente', 
     'vision_alert': 'Pérdida de visión', 
     'hearing_alert': 'Pérdida auditiva', 
     'psychologie_alert': 'Síntomas depresivos', 
     'locomotion_alert': 'Limitación en la movilidad'
}

class CustomRegistrationForm(RegistrationForm):
    location = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'location', 'password1', 'password2')

    def save(self, commit=True):
        with transaction.atomic():
            user = super(CustomRegistrationForm, self).save()
            user.refresh_from_db()  # very important! this will load the profile instance created by the signal
            user.profile.location = self.cleaned_data.get('location')
            # set here all other values
            user.save()
            return user

class SearchForm(forms.Form):
    
    apellidos = forms.CharField(required = False)
    fecha_nac = forms.DateField(input_formats=('%d/%m/%Y', ), 
                                required = False,
                                widget=forms.TextInput(attrs={
                                        'placeholder': 'dd/mm/yyyy'  # Date format hint
                                            })
                                )
    dni = forms.CharField(required = False)
    codigo = forms.CharField(required = False)

    def clean(self):
     
        cleaned_data = super().clean()
        print('SearchView CLEAN')

        apellidos = cleaned_data.get('apellidos')
        fecha_nac = cleaned_data.get('fecha_nac')
        dni = cleaned_data.get('dni')
        codigo = cleaned_data.get('codigo')

        if codigo:
            try:
                paciente = Paciente.objects.get(codigo=codigo)
                return cleaned_data
            except:
                raise ValidationError('Paciente no encontrado.')


        # Check that either dni is provided, or both apellidos and fecha_nac are provided
        if not dni and not (apellidos and fecha_nac):
            print('Error')
            raise ValidationError('You must provide either DNI or both Apellidos and Fecha Nacimiento.')

        # If fecha_nac is provided, validate it's in the correct date format (dd/mm/yyyy)
        # if fecha_nac:
        #     try:
        #         datetime.strptime(fecha_nac, '%d/%m/%Y')
        #     except ValueError:
        #         raise ValidationError('Fecha de Nacimiento must be in the format dd/mm/yyyy.')

        return cleaned_data


class RegistroForm(forms.ModelForm):

    fecha_nacimiento = forms.DateField(input_formats=('%d/%m/%Y', ))
    check = forms.BooleanField(required = True)
    class Meta:
        model = Registro
        fields = '__all__'

class ScreeningForm(forms.ModelForm):

    todo_ok = forms.BooleanField(required = False)
    class Meta:
        model = Evaluacion
        fields = '__all__'


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        preguntas = Pregunta.objects.filter(
            evaluacion=self.instance
        )

        for field in self.fields:
            self.fields[field].widget = HiddenInput()

        for pregunta in preguntas:
            field_name = pregunta.componente.nombre #'pregunta_%s' % (pregunta.id,)

            self.fields[field_name] = forms.BooleanField(required = False)
            self.initial[field_name] = pregunta.valor == 'SI'

    def clean(self):
        cleaned_data = super().clean()
        visita = cleaned_data.get('visita')
        cuestionario = cleaned_data.get('cuestionario')
        evaluacion = Evaluacion.objects.get(visita=visita, cuestionario=cuestionario)

        self.cleaned_data['completada'] = True

        preguntas = Pregunta.objects.filter(
            evaluacion=evaluacion
        )

        for pregunta in preguntas:
            field_name = pregunta.componente.nombre # 'pregunta_%s' % (pregunta.id,)
            if self.cleaned_data.get(field_name):
                # id = field_name.split('_')[1]
                #pregunta = evaluacion.preguntas.filte(cuestionario__nombre = ) # Pregunta.objects.get(id=id)
                self.cleaned_data[field_name] = 'SI'
            else:
                self.cleaned_data[field_name] = 'NO'

    def save(self, commit=True):

        instance = super(ScreeningForm, self).save(commit=True)

        for field, value in self.cleaned_data.items():
            if field not in ('visita', 'cuestionario', 'completada', 'todo_ok'):
                pregunta = instance.preguntas.get(componente__nombre = field)
                pregunta.valor = value
                pregunta.save()



        for componente in instance.cuestionario.componentes.filter(order__lt=0):
            pregunta = Pregunta.objects.get_or_create(
                evaluacion=self,
                componente=componente,
            )

            pregunta.valor = 'SI'
            pregunta.save()


        # for domain, label in _DOMINIOS.items():
        #     pregunta = instance.preguntas.get(componente__nombre = domain)

        #     # if instance.preguntas.get(componente__nombre = field)
        #     pregunta.valor = 'SI'
        #     pregunta.save()

        return instance


class EvaluacionForm(forms.ModelForm):

    class Meta:
        model = Evaluacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        preguntas = Pregunta.objects.filter(
            evaluacion=self.instance
        ).filter(componente__order__gte=0)

        # for field in self.form_fields:
        #     field_key = field.slug
        #     field_class = fields.CLASSES[field.field_type]
        #     field_widget = fields.WIDGETS.get(field.field_type)
        #     field_args = {"label": field.label, "required": field.required,
        #                   "help_text": field.help_text}
        #     arg_names = field_class.__init__.__code__.co_varnames
        #     if "max_length" in arg_names:
        #         field_args["max_length"] = settings.FIELD_MAX_LENGTH
        #     if "choices" in arg_names:
        #         choices = list(field.get_choices())
        #         if field.field_type == fields.SELECT and not (field.required and field.default):
        #             # The first OPTION with attr. value="" display only if...
        #             #   1. ...the field is not required.
        #             #   2. ...the field is required and the default is not set.
        #             text = "" if field.placeholder_text is None else field.placeholder_text
        #             choices.insert(0, ("", text))
        #         field_args["choices"] = choices
        #     if field_widget is not None:
        #         field_args["widget"] = field_widget

        for field in self.fields:
            self.fields[field].widget = HiddenInput()

        for pregunta in preguntas.order_by('componente__bloque', 'componente__order', 'componente__pk'):

            field_name = 'pregunta_%s' % (pregunta.id,)

            if pregunta.componente.tipo == 'TEXT':
                self.fields[field_name] = forms.CharField(required=pregunta.componente.required)
                self.initial[field_name] = pregunta.valor

            elif pregunta.componente.tipo == 'NUM':
                self.fields[field_name] = forms.FloatField(required=pregunta.componente.required)
                self.initial[field_name] = pregunta.valor or 0

            elif pregunta.componente.tipo == 'VAL':
                choices = pregunta.componente.get_choices()

                self.fields[field_name] = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple(), initial=[pregunta.valor], required=pregunta.componente.required)
                self.initial[field_name] = [pregunta.valor]

            elif pregunta.componente.tipo == 'LIST':
                choices = pregunta.componente.get_choices()
                self.fields[field_name] = forms.ChoiceField(choices=choices, widget=forms.Select(), required=pregunta.componente.required)
                # self.fields[field_name] = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple(), required=pregunta.componente.required)
                self.initial[field_name] = [pregunta.valor]

            elif pregunta.componente.tipo == 'CHECK':
                
                choices = [('SI', 'Sí'), ('NO', 'No')] # pregunta.componente.get_choices()               
                self.fields[field_name] = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple(), required=pregunta.componente.required)
                self.initial[field_name] = [pregunta.valor]

            elif pregunta.componente.tipo == 'MULTIPLE':
                
                choices = pregunta.componente.get_choices()              
                self.fields[field_name] = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple(), required=pregunta.componente.required)
                self.initial[field_name] = [pregunta.valor]

            elif pregunta.componente.tipo == 'CALC':
                
                if pregunta.componente.nombre == 'sppb_navarra':
                    
                    sppb = self.instance.visita.evaluaciones.filter(cuestionario__nombre='Short Physical Performance Battery (SPPB)').order_by('-pk').first()
                    puntuacion = sppb.puntuacion
                    vivifrail = sppb.preguntas.filter(componente__nombre='sppb_alert').first().valor

                    valor = f'{vivifrail} ({puntuacion} puntos)'
                else:
                    valor = ''

                self.fields[field_name] = forms.CharField(required=pregunta.componente.required)
                self.initial[field_name] = valor

            else:
                self.fields[field_name] = forms.CharField(required=pregunta.componente.required)
                self.initial[field_name] = pregunta.valor

            self.fields[field_name].navarra = pregunta.componente.nombre.endswith('_navarra')
            self.fields[field_name].alert = pregunta.componente.nombre.endswith('_alert')
            self.fields[field_name].tipo = pregunta.componente.tipo
            self.fields[field_name].label = pregunta.componente.titulo
            self.fields[field_name].help_text = pregunta.componente.help_text
            self.fields[field_name].bloque = pregunta.componente.bloque
            self.fields[field_name].opciones = pregunta.componente.get_choices()


    def clean(self):
        cleaned_data = super().clean()
        visita = cleaned_data.get('visita')
        cuestionario = cleaned_data.get('cuestionario')
        evaluacion = Evaluacion.objects.get(visita=visita,cuestionario=cuestionario)

        self.cleaned_data['completada'] = True

        preguntas = Pregunta.objects.filter(
            evaluacion=evaluacion
        )

        for pregunta in preguntas:
            field_name = 'pregunta_%s' % (pregunta.id,)
            id = field_name.split('_')[1]
            pregunta = Pregunta.objects.get(id=id)
            # DEBUG
            # print(field_name, pregunta.componente.nombre, 'ok' if cleaned_data.get(field_name) else 'no')
            
            if pregunta.componente.tipo in ('CHECK', ):
                o = pregunta.componente.opciones.first().valor
                n = 'NO' if o == 'SI' else 'SI'
                if self.cleaned_data.get(field_name):
                    self.cleaned_data[field_name] = o
                else:
                    self.cleaned_data[field_name] = n

            if self.cleaned_data.get(field_name):
                if pregunta.componente.tipo in ('VAL', 'LIST'):
                    self.cleaned_data[field_name] = self.cleaned_data[field_name][0]
                elif pregunta.componente.tipo in ('MULTIPLE', ):
                    if self.cleaned_data.get(field_name):
                        self.cleaned_data[field_name] = 'SI'
                    else:
                        self.cleaned_data[field_name] = 'NO'
                    # self.cleaned_data[field_name] = ','.join(self.cleaned_data[field_name])
            elif pregunta.componente.tipo in ('NUM', ):
                self.cleaned_data[field_name] = 0
            elif pregunta.componente.tipo in ('MULTIPLE', ):
                self.cleaned_data[field_name] = 'SI'
            else:
                self.cleaned_data[field_name] = ''


    def save(self, commit=True):
        instance = super(EvaluacionForm, self).save(commit=True)

        # instance.course = self.course
        # instance.user = self.user
        # if commit:
        #     instance.save()



        # set evaluacion fields
        # evaluacion.first_name = self.cleaned_data[“first_name”]

        # preguntas = Pregunta.objects.filter(
        #     evaluacion=self.instance.evaluacion
        # )

        for field, value in self.cleaned_data.items():
            if field.startswith('pregunta'):
                pk = field.split('_')[1]
                pregunta = Pregunta.objects.get(pk=pk)
                pregunta.valor = value
                pregunta.save()

        for componente in instance.cuestionario.componentes.filter(order__lt=0):
            pregunta, _ = Pregunta.objects.get_or_create(
                evaluacion=instance,
                componente=componente,
            )

            preguntas = instance.preguntas.filter(componente__bloque = pregunta.componente.bloque) \
                                .exclude(componente__nombre__endswith='navarra') \
                                .exclude(componente__nombre__endswith='alert')
            
            pregunta.valor = 'SI' if any([p.valor == p.componente.opciones.first().valor for p in preguntas ]) else 'NO'
            
            pregunta.save()

        # for pregunta in preguntas:
        #     field_name = 'pregunta_%s' % (pregunta.id,)
        #     if self.cleaned_data.get(field_name):
        #         pregunta.valor = self.cleaned_data.get(field_name)

        return instance
