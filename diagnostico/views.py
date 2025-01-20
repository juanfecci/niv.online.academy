from django.shortcuts import render, redirect
from .models import Question
import random

def prueba_diagnostico(request):
	return render(request, 'diagnostico1.html')

def prueba_diagnostico2(request):
	#return render(request, 'diagnostico2.html')

    #Sección si ya esta activa la prueba:
    if request.method == 'POST':
        print("Entre al POST")
        questions_done2 = request.session['questions_done']
        number_test = (request.session['page'] - 1) * 10 + 1
        questions_ids = request.POST.getlist('questions_ids')
        print(questions_ids)
        for question_id in questions_ids:
            print(question_id)
            if int(question_id) not in questions_done2:
                question = Question.objects.get(id=question_id)
                selected_option = request.POST.getlist('selected_options_' + question_id)

                try:
                    selected_option[0]
                except IndexError:
                    is_correct = False
                else:
                    is_correct = int(selected_option[0]) == int(question.correct_option)

                request.session['answers'].append({
                    'question_id': question_id,
                    'number_test': number_test,
                    'selected_option': selected_option,
                    'is_correct': is_correct
                })
                request.session['questions_done'].append(int(question_id))
                number_test += 1
                print(request.session['questions_done'])
            else:
                print("No entre")

        request.session.modified = True

    #Sección de inicio y selección de preguntas
    if 'questions_done' not in request.session or request.method == 'GET':
        print("Entre en la limpieza")
        request.session['questions_done'] = []
        request.session['answers'] = []
        request.session['page'] = 0

    questions_done = request.session['questions_done']
    remaining_questions = Question.objects.exclude(id__in=questions_done)
    actual_page = request.session['page'] + 1
    request.session['page'] = actual_page

    if not remaining_questions.exists():

        answers = request.session.get('answers', [])

        cefr = {0:"pre-A1", 1:"A1/A1+", 2:"A2", 3:"A2+", 4:"B1", 5:"B1/B1+", 6:"B1+" ,7:"B2/C1" }
        toeic = {0:"60", 1:"60 - 180", 2:"200 - 300", 3:"300 - 500", 4:"505 - 600", 5:"605 - 700", 6:"705 - 750", 7:"750+"}

        '''
        #Verdaderas respuestas
        preguntas_nivel = {
            1:[1,2,3,4,12,17,18,19,27,28,31,33,34,42,45],
            2:[5,6,7,8,11,14,15,16,20,21,22,23,29,30,35,41,44,47,64,81,97],
            3:[9,13,24,26,32,36,37,39,43,46,47,48,50,56,65,67,73,82,84,90,98],
            4:[38,40,49,52,56,63,66,69,76,80,83,86,93,99],
            5:[51,53,54,55,61,68,70,71,72,78,85,87,88,89,95,96],
            6:[57,58,60,74,75,77,91,92,94]
        }
        '''

        #Prueba 74-99
        preguntas_nivel = {
            #1:[74,75,76,77,78,79,85,86],
            1:[74,75,76,77,78,79],
            #2:[80,81,82,83,87,88],
            2:[80,81,82,83],
            3:[89,90,91,92,93,94],
            4:[95,96,97,98,99],
        }

        resultados = {}
        for answer in answers:
            resultados[int(answer["question_id"])] = bool(answer["is_correct"])

        nivel_actual = 1
        for i in range(1,5): #cambiar a 7 en producción
            flag_nivel = True

            for q_id in preguntas_nivel[i]:
                if not resultados[q_id]:
                    flag_nivel = False
                    break

            if flag_nivel:
                nivel_actual = i + 1
            else:
                break

        print("nivel", nivel_actual)
        print(cefr[nivel_actual-1])
        print(toeic[nivel_actual-1])
        
        # Aquí puedes procesar las respuestas y calcular los resultados
        # Por ejemplo, verificar respuestas correctas o calcular puntajes

        #Cambiar numeros en producción
        return render(request, 'diagnostico3.1.html', {
                'answers1': answers[:7],
                'answers2': answers[7:14],
                'answers3': answers[14:21], 
                'answers4': answers[21:26],
                'nivel': nivel_actual, 
                'nivel_CEFR': cefr[nivel_actual-1],
                'nivel_TOEIC': toeic[nivel_actual-1]})

    list_questions = list(remaining_questions)
    if len(list_questions) >= 10:
        questions = random.sample(list_questions, 10)
        #questions = list_questions[:10]
    else:
        questions = random.sample(list_questions, len(list_questions))
        #questions = list_questions[:10]
    final_questions = []
    n_pagina = (actual_page - 1) * 10
    n_pregunta = 1
    for q in questions:
        print(q.correct_option)
        final_questions.append([q, n_pregunta + n_pagina])
        n_pregunta += 1

    return render(request, 'diagnostico2.html', {'questions': final_questions, 'actual_page': actual_page})

    