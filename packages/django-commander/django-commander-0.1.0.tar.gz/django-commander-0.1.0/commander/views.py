from django.http import Http404
from django.shortcuts import render

from .commands import get_filtered_commands, WebRunnableCommand
from .forms import CommandForm
from .protection import protect_with_key


@protect_with_key
def command_list(request):
    commands = get_filtered_commands()
    commands_list = [ {'command': key, 'module': value} for key, value in commands.items()]

    return render(request, 'command_list.html', {
        'commands': commands_list,
        'key': request.GET['key'],
    })


@protect_with_key
def command_run(request, name):
    commands = get_filtered_commands()
    if not name in commands:
        raise Http404(name)

    runnable = WebRunnableCommand(commands[name], name)

    response_context = {
        'command_name': runnable.name,
        'command_usage': runnable.usage,
        'key': request.GET['key'],
    }

    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            args = form.cleaned_data['args']
            auto_noinput = form.cleaned_data['automatic_noinput']
            response_context['command_results'] = runnable.run(args, auto_noinput)

    else:
        form = CommandForm()

    form.fields['args'].label = name
    response_context['form'] = form

    return render(request, 'command_details.html', response_context)
