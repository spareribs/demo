from django.http import HttpResponse


class CheckSoureMiddware(object):
    def process_request(self, request):
        from_source = request.META['HTTP_USER_AGENT']
        print('from_source ', from_source)
        if 'MSIE 6.0' in from_source:
            request.session['from_source'] = 'MSIE 6.0'
            return HttpResponse('''<div align="center"><img src="../static/img/old.png" class="alignleft" alt="升级浏览器"/></div>''')
        if 'Trident/7.0' in from_source:
            request.session['from_source'] = 'MSIE 7.0'
            return HttpResponse('''<div align="center"><img src="../static/img/old.png" class="alignleft" alt="升级浏览器"/></div>''')
        if 'Trident/7.0' in from_source:
            request.session['from_source'] = 'MSIE 8.0'
            return HttpResponse('''<div align="center"><img src="../static/img/old.png" class="alignleft" alt="升级浏览器"/></div>''')
        else:
            request.session['from_source'] = 'pc'
