from django.core.management.base import BaseCommand
from django.db import connection
from aptitude_crd.models import Paciente

class Command(BaseCommand):
    help = 'Resets the AUTOINCREMENT sequences for specific tables in SQLite'

    def handle(self, *args, **kwargs):

        # Step 1: Delete all Paciente instances (this will cascade to other models)
        deleted_count, _ = Paciente.objects.all().delete()  # Cascades delete to related models
        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {deleted_count} Paciente instances and related models"))

        # List of tables for which you want to reset the sequences
        tables = [
            'aptitude_evaluacion',
            'aptitude_pregunta',
            'aptitude_intervencion',
            'aptitude_visita',
            'aptitude_paciente'
        ]

        # Reset AUTOINCREMENT sequence for each table
        with connection.cursor() as cursor:
            for table in tables:
                cursor.execute(f"UPDATE sqlite_sequence SET seq = 0 WHERE name = '{table}';")
                self.stdout.write(self.style.SUCCESS(f"Reset AUTOINCREMENT for table: {table}"))

        self.stdout.write(self.style.SUCCESS("Successfully reset sequences for all tables"))
