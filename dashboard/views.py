from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader

from .models import User, InstalledApp

import json
# Create your views here.

VALID_REQUESTS = ['get_username']

def dumpJsonp(request, data):
    if('sendback' in request.GET):
        data['sendback']=request.GET['sendback']
    if('callback' in request.GET):
        return "%s(%s)"%(request.GET['callback'], json.dumps(data))
    else:
        data['meta']='MALFORMED_JSONP'
        return json.dumps(data)

def login(request):
    context = {'failed':False}
    if('logout' in request.GET and request.GET['logout']=='true'):
        request.session.clear()
    if('username' in request.session):
        return redirect('/dash/')
    if('username' in request.POST and 'password' in request.POST):    
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        try:
            user = User.objects.get(username=username)
        except:
            user = None
        context['failed'] = True
        if(user != None):
            if(user.password == password):
                context = {'failed':False}
                request.session['username']=username
                return redirect('/dash/')
    return render(request, 'dashboard/login.htm', context)
    
    
def dash(request):
    if('username' not in request.session):
        return redirect('/')
    template = loader.get_template("dashboard/index.htm")
    context = {'app_list':None}
    username = request.session.get('username','')
    if(username != ''):
        user = get_object_or_404(User, username=username)
        context['app_list'] = user.installedapp_set.all()
        context['username'] = username
    return HttpResponse(template.render(context, request))

def req(request):
    if(request.method == 'GET'):
        if('REQUEST' in request.GET):
            data = json.loads(request.GET['REQUEST'])
            response = {'error':'false'}
            for r in list(data['REQUEST']):
                if(r=="get_username"):
                    response['username'] = request.session['username']
            return HttpResponse(dumpJsonp(request,response), content_type='application/javascript')
        else:
            return HttpResponse(dumpJsonp(request,{'error':'true', 'error_message':'no_request'}), content_type="application/javascript")
    return HttpResponse(dumpJsonp(request,{'error':'true', 'error_message':'faulty_request'}), content_type="application/json")

def install_app(request):
    if('page_url' in request.GET and 'tile_url' in request.GET):
        user = None
        try:
            user = User.objects.get(username=request.session['username'])
        except:
            return HttpResponse(dumpJsonp(request,{'error':'true', 'error_message':'invalid_user'}), content_type="application/json")
        newApp = InstalledApp(app_page_id=request.GET['page_url'], app_tile_id=request.GET['page_url'], user=user, app_id = user.maxapp+1)
        newApp.save()
        user.maxapp = user.maxapp + 1
        user.save()
        return HttpResponse(dumpJsonp(request,{'error':'false'}), content_type="application/json")
    return HttpResponse(dumpJsonp(request,{'error':'true', 'error_message':'faulty_request'}), content_type="application/json")