from django.core.management.base import BaseCommand, CommandError
import json
import pandas as pd
from aptitude_crd.models import Cuestionario, Componente, Opcion

class Command(BaseCommand):


    def add_arguments(self, parser):
        parser.add_argument('--filename')
        parser.add_argument('--database')

    def handle(self, *args, **options):
        database='default'
        filename = options['filename']
        if options['database']:
             database = options['database']
        print(f'DB: {database}')
        cuestionarios = pd.read_excel(filename)
        cuestionarios.fillna('', inplace=True)
        for index, row in cuestionarios.iterrows():
            nombre_cuestionario = row['Cuestionario'].strip()            
            bloque_cuestionario = row['Bloque'].strip()
            nombre_componente = row['Pregunta'].strip()
            desc_componente = row['Descripcion'].strip()
            try:
                nombre_respuesta = row['Respuesta'].strip()
            except:
                nombre_respuesta = ''
            try:
                puntuacion = str(row["Puntuacion"]).strip()
            except:
                puntuacion = ''
            tipo = str(row["Tipo"]).strip()

            cuestionario, created = Cuestionario.objects.using(database).get_or_create(
                nombre=nombre_cuestionario,
                defaults={'descripcion': nombre_cuestionario},
            )

            componente, created = Componente.objects.using(database).get_or_create(
                cuestionario = cuestionario,
                nombre=nombre_componente,
                tipo=tipo,
                defaults={'bloque': bloque_cuestionario, 
                          'descripcion': desc_componente},
            )

            # if tipo in ('VAL', 'LIST',):
            #     opcion, created = Opcion.objects.using(database).get_or_create(
            #         componente = componente,
            #         nombre = nombre_respuesta,
            #         valor = puntuacion,
            #         defaults={'tipo':'NUM'},
            #     )

            # tipo = models.CharField(verbose_name = _("Tipo"), max_length=10, choices= _COMP_TYPES)
            # valor_defecto = models.CharField(verbose_name = _("Valor por defecto"), max_length=100, blank= True, null = True)
            # lista = models.CharField(verbose_name = _("Lista"), max_length=100, blank= True, null = True)
            # funcion = models.CharField(verbose_name = _("Funcion"), max_length=100, blank= True, null = True)




        '''
        clip_cases = Case.objects.all()

        clips_study = Study.objects.all()[0]

        for case in clip_cases:
            new_case = ClipsCase()
            fields = case._meta.get_fields()
            for field in fields:

                #import pdb; pdb.set_trace()
                if field.name == "study":
                    new_case.study = clips_study

                elif field.name == "clips":
                    setattr(new_case, 'group', getattr(case,field.name) )

                elif field.name == "hospital":
                    continue

                else:
                    try:
                        setattr(new_case, field.name, getattr(case,field.name) )
                    except:
                        print("ERROR: " + str(new_case) )


            print("Case saved: " + str(new_case) )
            new_case.save()
            '''
