from django.shortcuts import render
from .services import *
from django.http import HttpResponse,JsonResponse

def webhook(request):
    if request.method == 'POST':
        data = request.POST.copy()
        level = data.get('action')
        outputContexts = data.get('outputContexts')
        repo = [ctx['parameters']['repoName'] for ctx in outputContexts if ctx['name'].endswith('playsquidgame-level1-followup')][0]
        game = game_play(level)
        game.code_base_git(repo,'main')
        game.code_validations()
        game.folder_validations()
        game.getBugs()
        game.getStatus()
        response = {'Status': game.status}
    return JsonResponse(response,content_type='application/json')



