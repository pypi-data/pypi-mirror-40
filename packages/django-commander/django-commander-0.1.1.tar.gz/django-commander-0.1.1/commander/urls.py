from django.urls import path

from commander import views as cmdr


commander_urls = ([
    path('', cmdr.command_list, name='list'),
    path('<str:name>/', cmdr.command_run, name='run'),
], 'commander', 'commander')