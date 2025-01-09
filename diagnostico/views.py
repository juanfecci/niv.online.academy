from django.shortcuts import render

def prueba_diagnostico(request):
	return render(request, 'diagnostico1.html')

def prueba_diagnostico2(request):
	return render(request, 'diagnostico2.html')
