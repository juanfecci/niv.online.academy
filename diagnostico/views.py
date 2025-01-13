from django.shortcuts import render, redirect
from .models import Question
import random

def prueba_diagnostico(request):
	return render(request, 'diagnostico1.html')

def prueba_diagnostico2(request):
	#return render(request, 'diagnostico2.html')

    #Sección si ya esta activa la prueba:
    if request.method == 'POST':
        print("Entre al Post")
        questions_ids = request.POST.getlist('questions_ids')
        #selected_options = request.POST.getlist('selected_options')
        selected_options_aux = request.POST.getlist('selected_options_74')
        print(questions_ids)
        #print(selected_options)
        print(selected_options_aux)

        for question_id in questions_ids:
            print("Entre al for")
            question = Question.objects.get(id=question_id)
            selected_option = request.POST.getlist('selected_options_' + question_id)

            try:
                selected_option[0]
            except IndexError:
                is_correct = False
            else:
                is_correct = int(selected_option[0]) == int(question.correct_option)
            
            print(int(selected_option[0]))
            print(question.correct_option)
            print(is_correct)

            request.session['answers'].append({
                'question_id': question_id,
                'selected_option': selected_option,
                'is_correct': is_correct
            })
            request.session['questions_done'].append(int(question_id))

        print("Sali del for")
        request.session.modified = True

    #Sección de inicio y selección de preguntas
    if 'questions_done' not in request.session or request.method == 'GET':
        print("Entre en la limpieza")
        request.session['questions_done'] = []
        request.session['answers'] = []
        request.session['page'] = 0

    questions_done = request.session['questions_done']
    print(questions_done)
    remaining_questions = Question.objects.exclude(id__in=questions_done)
    actual_page = request.session['page'] + 1
    request.session['page'] = actual_page

    if not remaining_questions.exists():
        answers = request.session.get('answers', [])
        # Aquí puedes procesar las respuestas y calcular los resultados
        # Por ejemplo, verificar respuestas correctas o calcular puntajes

        return render(request, 'resultados.html', {'answers': answers})

    list_questions = list(remaining_questions)
    if len(list_questions) >= 10:
        questions = random.sample(list_questions, 10)
    else:
        questions = random.sample(list_questions, len(list_questions))
    final_questions = []
    n_pagina = (actual_page - 1) * 10
    n_pregunta = 1
    for q in questions:
        final_questions.append([q, n_pregunta + n_pagina])
        n_pregunta += 1

    print("Terminando")
    return render(request, 'diagnostico2.html', {'questions': final_questions, 'actual_page': actual_page})

    