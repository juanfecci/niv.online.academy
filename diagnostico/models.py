from django.db import models

class Question(models.Model):
    text = models.TextField()  # Texto de la pregunta
    id_question = models.IntegerField(default=0)
    option_1 = models.CharField(max_length=255)  # Primera opción
    option_2 = models.CharField(max_length=255)  # Segunda opción
    option_3 = models.CharField(max_length=255)  # Tercera opción
    option_4 = models.CharField(max_length=255)  # Cuarta opción
    correct_option = models.CharField(max_length=1)  # Número de la opción correcta

    def __str__(self):
        return self.text

'''
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_option = models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)

    #user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Si necesitas vincularlo a un usuario
    #answer_text = models.TextField(blank=True, null=True)  # Para respuestas abiertas, o cambialo si son de opción múltiple
    #correct = models.BooleanField(default=False)  # Si aplica, para marcar si es correcta
''' 