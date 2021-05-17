from django.shortcuts import render
from . import forms, program_execution
from django.http import HttpResponse


def get_program_input(request):
    sdout = ""
    sderr = ""
    if request.method == 'POST':
        form = forms.CodeInputForm(request.POST)
        if form.is_valid():
             sdout, sderr = program_execution.execution(form)
    else:
        form = forms.CodeInputForm()
    return render(request, 'executor/executor_page.html', {'form': form, 'output': sdout, 'error': sderr})
