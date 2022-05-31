from django.http import HttpResponse
from django.utils.decorators import method_decorator
# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt


def show(request):
    return HttpResponse('this is dingdanlist')


@method_decorator(csrf_exempt, name='dispatch')
class Show1(View):
    # @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        res = super(Show1, self).dispatch(request, *args, **kwargs)
        return res

    def get(self, request, *args, **kwargs):
        return HttpResponse('get')

    def post(self, request, *args, **kwargs):
        return HttpResponse('post')

    def put(self, request, *args, **kwargs):
        return HttpResponse('put')

    def delete(self, request, *args, **kwargs):
        return HttpResponse('delete')


'''rest framework '''
from rest_framework.views import APIView


class Show2(APIView):
    def get(self, request, *args, **kwargs):
        super().dispatch()
        return HttpResponse('get')

    def post(self, request, *args, **kwargs):
        return HttpResponse('post')

    def put(self, request, *args, **kwargs):
        return HttpResponse('put')

    def delete(self, request, *args, **kwargs):
        return HttpResponse('delete')
