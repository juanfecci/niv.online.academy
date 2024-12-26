import csv
from django.core.management.base import BaseCommand
from diagnostico.models import Question  # Cambia 'your_app' por el nombre de tu aplicación

class Command(BaseCommand):
    help = 'Importa preguntas desde un archivo CSV al modelo Question'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Ruta al archivo CSV que contiene las preguntas')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')  # Usamos ';' como delimitador
            for row in reader:
                # Crear una nueva pregunta en la base de datos
                question = Question(
                    id_question=row['id'],
                    text=row['text'],
                    option_1=row['option_1'],
                    option_2=row['option_2'],
                    option_3=row['option_3'],
                    option_4=row['option_4'],
                    correct_option=row['correct_option'],
                )
                question.save()
                self.stdout.write(f'Pregunta "{row["text"]}" importada correctamente.')

        self.stdout.write(self.style.SUCCESS('Todas las preguntas han sido importadas correctamente.'))
