from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _
from datetime import date
from django.dispatch import receiver
from django.urls import reverse

from multiselectfield import MultiSelectField

_SEX = (
    (1, _("Hombre")),
    (2, _("Mujer")),
    )

_ASA = (
    (1, _("Hombre")),
    (2, _("Mujer")),
    )

_NO_YES = (
    (0, _("No")),
    (1, _("Sí")),
    )

_NO_YES_U = (
    (0, _("No")),
    (1, _("Sí")),
    (-1, _("Desconocido")),
    )

# - Nombre
# - Apellidos
# - DNI paciente
# - Dirección
# - Identificador
# - Teléfono
# - Email
# - Consentimiento informado
# - Campos de interés:
#         ◦ Deterioro cognitivo
#         ◦ Fragilidad
#         ◦ Cáncer
#         ◦ Incontinencia de orina y/o heces
#         ◦ Caídas
#         ◦ Diabetes
#         ◦ úlceras por presión
#         ◦ problemas cardiovasculares
#         ◦ problemas respiratorios
#         ◦ problemas renales
#         ◦ problemas digestivos
#         ◦ problemas endocrinos
#         ◦ problemas alimentarios y dentales
#         ◦ problemas reumatológicos
#         ◦ problemas hematológicos
#         ◦ problemas psiquiátricos
#         ◦ problemas de movilidad
#         ◦ problemas neurológicos
#         ◦ déficits sensoriales
#         ◦ polifarmacia
#         ◦ estilos de vida saludables
#         ◦ otros

class Tema(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = "aptitude_tema"

class Registro(models.Model):

    nombre = models.CharField(verbose_name = _("Nombre"), max_length=64)
    apellidos = models.CharField(verbose_name = _("Apellidos"), max_length=64)
    email = models.EmailField(verbose_name = _("Correo electrónico"), max_length=50, blank= True, null = True)

    dni = models.CharField(verbose_name = _("DNI"), max_length=10, blank= True, null = True)
    direccion = models.CharField(verbose_name = _("Dirección"), max_length=255, blank= True, null = True)
    ciudad = models.CharField(verbose_name = _("Ciudad"), max_length=255, blank= True, null = True)
    pais = models.CharField(verbose_name = _("País"), max_length=255, blank= True, null = True)
    fecha_nacimiento = models.DateField(verbose_name = _("Fecha de nacimiento"), blank= True, null = True)
    sexo = models.IntegerField(verbose_name = _("Sexo"), choices = _SEX, blank= True, null = True)
    telefono = models.CharField(verbose_name = _("Teléfono"), max_length=9, blank= True, null = True)
    consentimiento = models.FileField(verbose_name = _("Consentimiento informado"), blank= True, null = True)

    temas = models.ManyToManyField(Tema, verbose_name = _("Campos de interés"), blank= True)

    @property
    def edad(self):
        today = date.today()
        age = 45 # today.year - self.fecha_nacimiento.year - ((today.month, today.day) <  (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

        return age

    @property
    def rango_edad(self):

        rangos = { '0-15': (0,15),
                   '16-35': (16,35),
                   '36-50':(36, 50),
                   '51-65': (51,65),
                   '66-80': (66,80),
                   '80+':(80,120)
                }

        edad = self.edad
        for rango, valores in rangos.items():
            if edad >= valores[0] and edad <= valores[1]:
                return rango

    class Meta:
        db_table = "aptitude_registro"

    def __str__(self):
        return "{} {}".format(self.nombre, self.apellidos)

# Código del paciente (numérica).
# Fecha de nacimiento (día/mes/año).
# Sexo (categórica)
# Acceso a Internet (sí/no).
# Nivel de estudios: No escolarizado/ estudios primarios/estudios de secundaria/bachillerato/ universitario/ desconocido.

# Captación del paciente: médico general/especialista/farmacéutico/médico de la mutua/ familiar/ ayuntamiento/investigador/estación termal/convocatoria anual/otro.
# Frecuencia de visitas médicas: < 3meses/ 3-12 meses/ >12 meses/ sin seguimiento/ desconocido.

# Convivencia: solo/ con familia/ con pareja/ otro/ desconocido.
# Ayuda domiciliaria: ninguna/ comida/ tareas domésticas/ enfermero

# Evaluador: enfermera especialista en geriatria/ enfermera otros/ médico general/equipo multidisciplinar/médico residente/médico general/otros.
# Motivo de evaluación: impresión de fragilidad/ queja cognitiva/ desconocido

_VIVIENDA = (
    (1, _("En su casa")),
    (2, _("En casa de un hijo/hija")),
    (3, _("En casa de otro familiar")),
    (4, _("En un piso para personas mayores")),
)
_NIVEL_ESTUDIOS  = (
    (0, _("No escolarizado")),
    (1, _("Estudios primarios")),
    (2, _("Estudios de secundaria")),
    (3, _("Bachillerato")),
    (4, _("Estudios universitarios")),
    (-1, _("Desconocido")),
    )

_CAPTACION  = (
    (0, _("médico general")),
    (1, _("especialista")),
    (2, _("farmacéutico")),
    (3, _("médico de la mutua")),
    (4, _("familiar")),
    (5, _("Ayuntamiento")),
    (6, _("investigador")),
    (7, _("estación termal")),
    (8, _("convocatoria anual")),
    (9, _("otro")),
    )

_MOTIVO = (
    (0, _("Sospecha de situación de fragilidad")),
    (1, _("Sospecha de deterioro cognitiva")),
    (2, _("Seguimiento")),
    (-1, _("Motivo desconocido")),
    )

_INTERVENCION = (
    ('social', _("Intervención social")),
    ('fisica', _("Intervención física")),
    ('cognitiva', _("Intervención cognitiva")),
    ('nutricional', _("Intervención nutricional")),
    ('psicologica', _("Intervención psicológica")),
    ('otra', _("Otras intervenciones")),
    )

_PROFESIONAL = (
    (0, _("enfermera especialista en geriatria")),
    (1, _("enfermera otros")),
    (2, _("médico general")),
    (3, _("equipo multidisciplinar")),
    (4, _("médico residente")),
    (5, _("otros")),
    )

_COMP_TYPES = (
    ('TEXT', _("Texto")),
    ('NUM', _("Numérico")),
    ('VAL', _("Lista_Valor")),
    ('CHECK', _("Chequeo simple")),
    ('MULTIPLE', _("Chequeo multiple")),
    ('LIST', _("Lista")),
    ('CALC', _("Calculado")),
    )

_OP_TYPES = (
    ('TEXT', _("Texto")),
    ('NUM', _("Numérico")),
    )

_DOMINIO = (
    ('ANTROPOMETRICO', _("Antropométrico")),
    ('SCREENING', _("Screening")),
    ('COGNITIVO', _("Cognitivo")),
    ('FUNCIONAL', _("Funcional")),
    ('VITALIDAD', _("Vitalidad")),
    ('VISION', _("Sensorial (Visión)")),
    ('AUDICION', _("Sensorial (Audición)")),
    ('PSICOLOGICO', _("Psicológico")),
    ('COMPLEMENTARIOS', _("Complementarios")),
    )

_SALUD = (
    (1, _("Muy buena")),
    (2, _("Buena")),
    (3, _("Regular")),
    (4, _("Mala")),
    (5, _("Muy mala")),
    )

_HEALTH_PROBLEMS = (
    (1, _('Hipertensión')),
    (2, _('Cardiopatía isquémica sin antecedentes de infarto.')),
    (3, _('Infarto de miocardio')),
    (4, _('Insuficiencia cardiaca')),
    (5, _('Arritmias cardíacas')),
    (6, _('Otros problemas del corazón')),
    (7, _('Varices o insuficiencia venosa extremidades inferiores')),
    (8, _('Enfermedad arterial periférica')),
    (9, _('Otros problemas neurológicos')),
    (10, _('Alergias')),
    (11, _('Enfermedad respiratoria crónica')),
    (12, _('Enfermedad del tejido conectivo')),
    (13, _('Inflamación crónica del intestino')),
    (14, _('Ulcera gastroduodenal')),
    (15, _('Hepatopatía crónica leve')),
    (16, _('Hepatopatía crónica moderada/severa')),
    (17, _('Dislipemia')),
    (18, _('Problemas de tiroides')),
    (19, _('Insuficiencia renal crónica moderada/severa')),
    (20, _('Enfermedad Cerebrovascular')),
    (21, _('Hemiplejia')),
    (22, _('Demencia')),
    (23, _('Depresión')),
    (24, _('Nerviosismo')),
    (25, _('Dolores de cabeza o migraña')),
    (26, _('Enfermedad de Párkinson')),
    (27, _('Tumor o neoplasia sólida sin metástasis')),
    (28, _('Tumor o neoplasia sólida con metástasis')),
    (29, _('Leucemia')),
    (30, _('Linfoma')),
    (31, _('Sida definido')),
    (32, _('Antecedentes de fractura en el último año')),
    (33, _('Osteoporosis')),
    (34, _('Artrosis')),
    (35, _('Problemas de audición')),
    (36, _('Cataratas no operadas')),
    (37, _('Otros problemas de visión')),
    (38, _('Dolor crónico')),
    (39, _('Diabetes no complicada')),
    (40, _('Diabetes con lesión en órganos diana')),
    (41, _('Problemas de espalda (incluye columna y discos intervertebrales)')),
    (42, _('Otros problemas de visión (degeneración macular senil, problemas de refracción no resueltos con gafas o lentillas)')),
)

_TERRITORIO = (
    (0, _('Navarra')),
    (1, _('Alt Urgell')),
    (2, _('Badalona')),
    (3, _('Baix Ebre')),
    (4, _('Reus')),
    (5, _('Ripollès')),
)

_DISPONIBILIDAD = (
    (0, _('Todos')),
    (1, _('Solo Navarra')),
    (2, _('Solo Cataluña')),
)

_STEPS = (
    (0, _('Prueba')),
    (1, _('Step 1')),
    (2, _('Step 2')),
)

class Intervencion(models.Model):
    tipo = models.CharField(max_length=50, choices=_INTERVENCION)
    detalle = models.CharField(max_length=100)

    def __str__(self):
        return '{} - {}'.format(self.tipo, self.detalle)


    class Meta:
        verbose_name_plural = "Intervenciones"
        db_table = 'aptitude_intervencion'

class Cuestionario(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    dominio = models.CharField(verbose_name = _("Dominio"), max_length=15, choices= _DOMINIO, default='COGNITIVO')
    order = models.IntegerField(default=1)
    activo = models.BooleanField(default=False)


    url = models.URLField(blank=True, null=True)
    guia = models.FileField(blank=True, null = True, upload_to='docs/')
    calculo_valor =  models.CharField(max_length=100, default='puntuacion_total')
    limite =  models.IntegerField(default=0, blank= True, null = True)
    disponibilidad = models.IntegerField(default=0, choices=_DISPONIBILIDAD, blank= True, null = True)

    class Meta:
        ordering = ['order',]
        db_table='aptitude_cuestionario'

    def __str__(self):
        return self.nombre

class Componente(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE, related_name="componentes")
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank= True, null = True)
    bloque = models.CharField(max_length=100, blank= True, null = True)
    tipo = models.CharField(verbose_name = _("Tipo"), max_length=10, choices= _COMP_TYPES)
    required = models.BooleanField(default=True)
    valor_defecto = models.CharField(verbose_name = _("Valor por defecto"), max_length=100, blank= True, null = True)
    lista = models.CharField(verbose_name = _("Lista"), max_length=100, blank= True, null = True)
    funcion = models.CharField(verbose_name = _("Funcion"), max_length=100, blank= True, null = True)
    order =  models.IntegerField(default=0, blank= True, null = True)

    @property
    def titulo(self):
        if self.nombre.__contains__('_'):
            return self.descripcion
        else:
            return self.nombre
    
    @property
    def help_text(self):
        if self.descripcion != self.titulo:
            return self.descripcion
        else:
            return ''

    def get_choices(self):
        if self.tipo == 'VAL':
            if self.lista == 'SI_NO':
                return [('SI', 'Sí'), ('NO', 'No')]
            else:
                return [(o.valor, o.nombre) for o in self.opciones.all()]
        elif self.tipo in  ('CHECK','MULTIPLE'):
             return [(o.valor, o.nombre) for o in self.opciones.all()]
        elif self.tipo == 'LIST':
             return [(o.valor, o.nombre) for o in self.opciones.all()]
        else:
             return [('SI', 'Sí'), ('NO', 'No')]

        return [('SI', 'Sí'), ('NO', 'No')]

    def __str__(self):
        return self.nombre

    class Meta:
        db_table='aptitude_componente'

class Opcion(models.Model):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name="opciones")
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(verbose_name = _("Tipo"), max_length=10, choices= _OP_TYPES)
    valor = models.CharField(verbose_name = _("Valor"), max_length=10)

    class Meta:
        verbose_name_plural = "Opciones"
        db_table='aptitude_opcion'

    def __str__(self):
        return self.nombre

    def value(self):
        return eval(self.valor)

class Paciente(models.Model):

    codigo = models.CharField(verbose_name = _("Codigo"), max_length=7, blank= True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null = False)

    nombre = models.CharField(verbose_name = _("Nombre"), max_length=64)
    apellidos = models.CharField(verbose_name = _("Apellidos"), max_length=64)
    dni = models.CharField(verbose_name = _("DNI"), max_length=10, blank=True, null = True)
    
    ciudad = models.CharField(verbose_name = _("Ciudad"), max_length=255, blank= False, null = False)
    telefono = models.CharField(verbose_name = _("Teléfono"), max_length=9, blank=False, null = False)

    fecha_nacimiento = models.DateField(verbose_name = _("Fecha de nacimiento"), blank= False, null = False)
    sexo = models.IntegerField(verbose_name = _("Sexo"), choices = _SEX, blank= False, null = False)
    
    territorio = models.IntegerField(verbose_name = _("Territorio"), choices = _TERRITORIO, blank= True, null = False, default=0)
    pais = models.CharField(verbose_name = _("País"), max_length=255, blank= True, null = False, default='España')

    nivel_estudios = models.IntegerField(verbose_name = _("Nivel de estudios"), choices = _NIVEL_ESTUDIOS, blank= True, null = True)
    vivienda = models.IntegerField(verbose_name = _("Vivienda"), choices = _VIVIENDA, blank= True, null = True)
    convivientes = models.IntegerField(verbose_name = _("Convivientes"), blank= True, null = True)

    consentimiento = models.FileField(verbose_name = _("Consentimiento informado"), blank= True, null = True)
    consentimiento_informado = models.BooleanField(blank=False, null=False)

    email = models.EmailField(verbose_name = _("Correo electrónico"), max_length=50, blank= True, null = True)
    cp = models.CharField(verbose_name = _("Código postal"), max_length=6, blank= True, null = True)
    direccion = models.CharField(verbose_name = _("Dirección"), max_length=255, blank= True, null = True)
    internet = models.IntegerField(verbose_name = _("Acceso a internet"), choices = _NO_YES_U, blank= True, null = True, default=0)
    captacion = models.IntegerField(verbose_name = _("Captación del paciente"), choices = _CAPTACION, blank= True, null = True)

    salud = models.IntegerField(verbose_name = _("Salud general"), choices=_SALUD, blank= True, null = True)
    problemas_num = models.IntegerField(verbose_name = _("Número de problemas"), blank= True, null = True)
    problemas = MultiSelectField(verbose_name = _("Problemas de salud"), choices=_HEALTH_PROBLEMS, blank= True, null = True)

    def save(self, *args, **kwargs):
        # First, call the parent class's save() method
        super(Paciente, self).save(*args, **kwargs)

        # Only update `codigo` if it's not already set (typically, on creation)
        if not self.codigo:
            self.codigo = "NAV{:04d}".format(self.pk)
            # Call save again only if `codigo` was updated
            Paciente.objects.filter(pk=self.pk).update(codigo=self.codigo)

    def nombre_masked(self):

        return ' '.join([part[:2] + 'X' * len(part[2:]) for part in "{} {}".format(self.nombre, self.apellidos).split()])

    def __str__(self):
        return self.codigo

    class Meta:
        db_table='aptitude_paciente'


class Visita(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null = True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='visitas')
    fecha = models.DateField(verbose_name = _("Fecha de la visita"), auto_now_add=True)

    motivo = models.IntegerField(verbose_name = _("Motivo de evaluación"), choices = _STEPS, blank= True, null = True)
    muestra = models.BooleanField(verbose_name = _("Recoge muestra"), default=False)
    codigo_muestra = models.CharField(verbose_name = _("Codigo muestra"), max_length=5, blank= True, null = True)

    cuestionarios = models.ManyToManyField(Cuestionario)

    dominios = models.CharField(verbose_name = _("Dominios"), max_length=255, blank= True, null = True)
    informe_medico = models.CharField(verbose_name = _("Informe"), max_length=5, blank= True, null = True)
    seguimiento = models.CharField(verbose_name = _("Seguimiento"), max_length=5, blank= True, null = True)
    nivel_seguimiento = models.CharField(verbose_name = _("Nivel de seguimiento"), max_length=5, blank= True, null = True)

    intervencion = models.ManyToManyField(Intervencion, blank=True)

    notas = models.TextField(blank= True, null = True)

    def is_cat(self):
        return self.paciente.territorio > 0

    def lista_dominios(self):
        return ['COGNITIVO', 'FUNCIONAL', 'VITALIDAD', 'VISION', 'AUDICION', 'PSICOLOGICO', 'COMPLEMENTARIOS']

    def dominios_afectados(self):
        icope = self.evaluaciones.get(cuestionario__dominio='SCREENING')
        if icope:
            return icope.preguntas.filter(componente__nombre__endswith='_alert').filter(valor='SI').count() > 0 
        else:
            return False
        
    def tiene_dominios_afectados(self):
        icope = self.evaluaciones.get(cuestionario__dominio='SCREENING')
        if icope:
            return icope.preguntas.filter(componente__nombre__endswith='_alert').filter(valor='SI').count() > 0 
        else:
            return False
        # return set([ p.componente.nombre.replace('-1','') for p in icope.preguntas.all() if p.valor == 'SI' ]) - {'TODO_OK'}

    def solo_sensorial(self):
        dominios = self.dominios_afectados()

        if dominios == {'VISION'} or dominios == {'VISION', 'AUDICION'} or  dominios == {'AUDICION'}:
            return True
        else:
            return False

    def add_cuestionarios(self):
        if self.is_cat():
            self.add_all_cuestionarios()
        elif len(self.dominios_afectados()):
            if self.solo_sensorial():
                for d in self.dominios_afectados():
                    self.add_cuestionarios_dominio(d)
            else:
                self.add_all_cuestionarios()

    def add_all_cuestionarios(self):
        cuestionarios = Cuestionario.objects.filter(order__gte=1).exclude(activo=0)

        if self.is_cat():
            cuestionarios = cuestionarios.exclude(disponibilidad=1)

        if not self.is_cat():
            cuestionarios = cuestionarios.exclude(disponibilidad=2)

        for cuestionario in cuestionarios: #self.cuestionarios.all()
            self.cuestionarios.add(cuestionario)
            evaluacion = Evaluacion.objects.get_or_create(
                visita=self,
                cuestionario=cuestionario
            )

    def add_cuestionarios_dominio(self, dominio):
        cuestionarios = Cuestionario.objects.filter(dominio=dominio).exclude(activo=0)

        for cuestionario in cuestionarios: #self.cuestionarios.all()
            self.cuestionarios.add(cuestionario)
            evaluacion = Evaluacion.objects.get_or_create(
                visita=self,
                cuestionario=cuestionario
            )

    @property
    def cuestionarios_completos(self):
        return self.evaluaciones.all().filter(completada=False).count() == 0

    @property
    def motivo_evaluacion(self):
        if self.motivo is not None:
            return _MOTIVO[self.motivo][1]
        else:
            return 'Desconocido'

    def __str__(self):
        return "{} ({})".format(_STEPS[self.motivo or 0][1], self.fecha)

    def get_absolute_url(self):
        return reverse('visita-eval', args=[self.id,])

    class Meta:
        db_table='aptitude_visita'

@receiver(models.signals.post_save, sender=Visita)
def execute_after_visit_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.add_cuestionarios_dominio('ANTROPOMETRICO')
        instance.add_cuestionarios_dominio('SCREENING')

class Evaluacion(models.Model):
    visita = models.ForeignKey(Visita, on_delete=models.CASCADE, related_name='evaluaciones')
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)
    completada = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.cuestionario.nombre)
        #return '{} - {}'.format(self.id, self.cuestionario.nombre)

    @property
    def paciente(self):

        return self.visita.paciente
    
    @property
    def resultado(self):

        return self.puntuacion > self.cuestionario.limite

    @property
    def puntuacion(self):
        return sum([p.valor_num for p in self.preguntas.all() if p.componente.tipo == 'VAL'])

    def get_absolute_url(self):
        return reverse('evaluacion', args=[self.id,])

    def add_preguntas(self):
        for componente in self.cuestionario.componentes.filter(order__gte=0).order_by('order','pk'):
            pregunta = Pregunta.objects.get_or_create(
                evaluacion=self,
                componente=componente,
            )

    class Meta:
        verbose_name_plural = "evaluaciones"
        db_table = 'aptitude_evaluacion'

@receiver(models.signals.post_save, sender=Evaluacion)
def execute_after_eval_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.add_preguntas()

    # if not created and instance.cuestionario.dominio == 'SCREENING':
    #    instance.visita.add_cuestionarios()

    #     for p in instance.preguntas.all():
    #         if p.valor == 'SI':
    #             instance.visita.add_cuestionarios_dominio(p.componente.nombre)


class Pregunta(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='preguntas')
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, related_name='respuestas')
    valor = models.CharField(max_length=100)

    @property
    def respuesta(self):
        if self.componente.tipo == 'VAL':
            try:
                return self.componente.opciones.get(valor=self.valor)
            except:
                return ''
        else:
            return self.valor

    @property
    def valor_num(self):
        try:
            if self.componente.tipo == 'VAL':
                return eval(self.valor) or 0 # componente.opciones.get(id=self.valor).valor
            elif self.componente.tipo == 'NUM':
                return eval(self.valor)
            else:
                0
        except:
            return 0

    def __str__(self):
        return str(self.componente)

    class Meta:
        db_table='aptitude_pregunta'

# nombre = models.CharField(verbose_name = _("Nombre"), max_length=64)
    # apellidos = models.CharField(verbose_name = _("Apellidos"), max_length=64)
    # email = models.EmailField(verbose_name = _("Correo electrónico"), max_length=9, blank= True, null = True)

    # dni = models.CharField(verbose_name = _("DNI"), max_length=9, blank= True, null = True)
    # direccion = models.CharField(verbose_name = _("Dirección"), max_length=255, blank= True, null = True)
    # fecha_nacimiento = models.DateField(verbose_name = _("Fecha de nacimiento"), blank= True, null = True)
    # sexo = models.IntegerField(verbose_name = _("Sexo"), choices = _SEX, blank= True, null = True)
    # telefono = models.CharField(verbose_name = _("Teléfono"), max_length=9, blank= True, null = True)
    # consentimiento = models.FileField(verbose_name = _("Consentimiento informado"), blank= True, null = True)
    #intereses =

# Captación del paciente: médico general/especialista/farmacéutico/médico de la mutua/ familiar/ ayuntamiento/investigador/estación termal/convocatoria anual/otro.
# Evaluador: enfermera especialista en geriatria/ enfermera otros/ médico general/equipo multidisciplinar/médico residente/médico general/otros.
# Motivo de evaluación: impresión de fragilidad/ queja cognitiva/ desconocido
# Frecuencia de visitas médicas: < 3meses/ 3-12 meses/ >12 meses/ sin seguimiento/ desconocido.
# Nivel de estudios: No escolarizado/ estudios primarios/estudios de secundaria/bachillerato/ universitario/ desconocido.
# Convivencia: solo/ con familia/ con pareja/ otro/ desconocido.
# Ayuda domiciliaria: ninguna/ comida/ tareas domésticas/ enfermeros/ quiropráctico/teleasistencia/ desconocido.
# Prestación económica por situación de dependencia: Si/No/desconocido.
# Medidas de protección jurídica: Sí/No/desconocido.
# No de patologías crónicas
# No de tratamientos habituales
# Cáncer en tratamiento actual: Sí/No/Desconocido

# class Patient(models.Model):

#     asa = models.IntegerField(verbose_name = "ASA", choices = _ASA , blank= True, null = True)
#     hypertension = models.IntegerField(verbose_name = "Hypertension", choices = _NO_YES, blank= True, null = True)
#     hb = models.FloatField(verbose_name = "HB (g/dL)", blank= True, null = True)
#     platelets = models.IntegerField(verbose_name = "Platelets (x10⁹/L)", blank= True, null = True)
#     """
#         Glucoses
#     """
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     moment = models.IntegerField(null=True)
#     glucose = models.DecimalField(max_digits=5, decimal_places=2)
#     insulin = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#     comment = models.TextField()
#     date_glucoses = models.DateField()
#     hour_glucoses = models.TimeField()
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = 'Glucose'
#         verbose_name_plural = 'Glucoses'

#     def __str__(self):
#         return "Glucose: %s Insulin: %s (date: %s)" % (
#                                                 self.glucose,
#                                                 self.insulin,
#                                                 self.date_glucoses)
