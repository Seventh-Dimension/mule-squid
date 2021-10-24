from django.shortcuts import render
from .services import *
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        qr = data.get('queryResult')
        level = qr.get('action')
        outputContexts = qr.get('outputContexts')
        print(outputContexts)
        repo = [ctx['parameters']['repoName'] for ctx in outputContexts if ctx['name'].endswith('playsquidgame-level1-followup')][0]
        game = game_play(level)
        game.code_base_git(repo,'main')
        game.code_validations()
        game.folder_validations()
        game.getBugs()
        game.getStatus()
        if game.status == 'Qualified':
            textresponse = {"fulfillmentMessages": [{"text": {"text": [
            "Congrats for passing the "+ level + ". Please proceed to play further rounds by mentioning the rounds"
            ]}}]}
        else:
            textresponse = {"fulfillmentMessages": [{"text": {"text": [
                "Oops. You haven't cleared this level. Do you want to play again? or Exit the game?"
            ]}}]}
        response = {'Status': game.status}
    return JsonResponse(textresponse,content_type='application/json')



