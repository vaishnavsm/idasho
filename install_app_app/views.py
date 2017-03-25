from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.

def dumpJsonp(request, data):
    if('sendback' in request.GET):
        data['sendback']=request.GET['sendback']
    if('callback' in request.GET):
        return "%s(%s)"%(request.GET['callback'], json.dumps(data))

def page(request):
    if('dashboard_request' in request.GET):
        request.session['dashboard_url'] = request.GET['dashboard_url']
        return HttpResponse(dumpJsonp(request, {'load_current_page':'true', 'fullscreen_on_click':'false', 'is_interactive_tile':'true', 'get_parameter':'isdash'}), content_type="application/javascript")
    if('isdash' in request.GET):
        context = {'dashboard_url':request.session['dashboard_url']}
        #context = {}
        return render(request=request, template_name="install_app_app/installapp_tile.htm", context=context)
    return HttpResponse("Boo hoo")
    