#!coding:utf-8
from django.shortcuts import render
import subprocess
from django.conf import settings
import os

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from dwebsocket.decorators import accept_websocket,require_websocket

# Create your views here.

workdir = settings.BASE_DIR

def index(request):
    """主页面"""
    #return HttpResponse('xxx')
    print dir(request)
    return render(request, 'index.html',locals())

def websocket(request):
    """主页面"""
    #return HttpResponse('xxx')
    print dir(request)
    return render(request, 'websocket.html',locals())

def start_task(request):
    #return HttpResponse('ok')
    if request.method == 'POST':
        interpreter = request.POST['interpreter']
        script = os.path.join(settings.BASE_DIR,request.POST['script'])
        log = request.POST['log']
        cmd = '''%s %s > %s''' % (interpreter,script,log)
        os.system('''echo %s > %s/task.state''' % (1, workdir))
        p = subprocess.Popen(
            cmd,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
        outdata, errdata = p.communicate()
        retcode  = p.wait()
        if retcode:
            os.system('''echo %s > %s/task.state''' % (retcode,workdir) )
            return HttpResponse('error')
        else:
            os.system('''echo %s > %s/task.state''' % (0, workdir))
            return HttpResponse('ok')
    else:
        return HttpResponse('GET')

# @accept_websocket
# def testwebsocket(request):
#     if request.is_websocket():
#         print   dir(request)
#         print request.websocket
#         for logtype in request.websocket:
#             print logtype
#             if logtype == 'a':
#                 request.websocket.send('aaa')
#             elif logtype == 'b':
#                 request.websocket.send('bbb')
#     else:
#         print 'request is not websocket'
#         return HttpResponse('request is not websocket')

@accept_websocket
def testwebsocket(request):
    if request.is_websocket():
        print   dir(request)
        print request.websocket
        for logtype in request.websocket:
            print logtype
            status = 1
            loglen = 0
            while status:
                status = int(os.popen('''cat %s/task.state | head -1''' % workdir).read().strip())
                f = open('%s/a.log' % workdir, 'r')
                content = f.read()
                now_loglen = len(content)
                if now_loglen > loglen:
                    request.websocket.send(content)
                    loglen = now_loglen
            if logtype == 'a':
                request.websocket.send('aaa')
            elif logtype == 'b':
                request.websocket.send('bbb')
            break
    else:
        print 'request is not websocket'
        return HttpResponse('request is not websocket')

def getprocess(request):
    f = open('%s/%s' % (workdir,request.POST['log']),'r')
    content = f.read()
    status = int(os.popen('''cat %s/task.state | head -1''' % workdir).read().strip())
    data = {'data':content,'status':status}
    return JsonResponse(data)
