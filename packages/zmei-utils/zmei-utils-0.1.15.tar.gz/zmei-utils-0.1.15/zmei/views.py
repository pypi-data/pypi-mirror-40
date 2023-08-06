import json
from pprint import pprint

from django.http import HttpResponse
from django.utils.decorators import classonlymethod
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.generic.base import View, ContextMixin, TemplateResponseMixin
from zmei.json import ZmeiReactJsonEncoder


class ImproperlyConfigured(Exception):
    pass


class _Data(object):
    def __init__(self, data=None):
        self.__dict__.update(data or {})

    def __add__(self, data):
        return _Data({**self.__dict__, **data})


class ZmeiDataViewMixin(ContextMixin, View):
    _data = None

    def get_data(self, url, request, inherited=False):
        return {}

    def _get_data(self):
        if not self._data:
            url = type('url', (object,), self.kwargs)
            self._data = self.get_data(
                url=url,
                request=self.request,
                inherited=False
            )
            self._data['url'] = url

        return self._data

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        return {**context_data, **self._get_data()}


class ZmeiRemoteInvocationViewMixin(ZmeiDataViewMixin):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        accept = self.request.META.get('HTTP_ACCEPT')
        if accept and 'application/json' in accept:
            return HttpResponse(ZmeiReactJsonEncoder(view=self).encode(self._get_data()), content_type='application/json')

        return self.render_to_response(context)

    @classonlymethod
    def as_view(cls, **initkwargs):
        return ensure_csrf_cookie(super().as_view(**initkwargs))

    def _remote_response(self, data):
        return HttpResponse(ZmeiReactJsonEncoder(view=self).encode(data), content_type='application/json')

    def state(self, data):
        return {'__state__': data}

    def error(self, data):
        return {'__error__': data}

    def post(self, request, *args, **kwargs):
        if 'application/json' not in self.request.META['HTTP_ACCEPT']:
            raise ValueError('Only json is available as a response type.')

        call = json.loads(request.body)
        method_name = f"_remote__{call.get('method')}"

        if not hasattr(self, method_name):
            raise ValueError('Unknown method')

        method = getattr(self, method_name)

        try:
            result = method(
                type('url', (object,), self.kwargs),
                request,
                *(call.get('args') or [])
            )
        except Exception as e:
            return self._remote_response(self.error(str(e)))

        if not result:
            return self._remote_response(self.state(self._get_data()))

        return self._remote_response(result)


class CrudView(TemplateResponseMixin):
    def render_to_response(self, context, **response_kwargs):
        return context


class CrudMultiplexerView(TemplateResponseMixin, ContextMixin, View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.crud_views = {}
        for cls in self.get_crud_views():
            crud = cls(*args, **kwargs)
            self.crud_views[crud.name] = crud

    def get_crud_views(self):
        return ()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context['crud'] = {}
        for crud in self.crud_views.values():
            self.populate_crud(args, crud, kwargs, request)

            context['crud'][crud.name] = crud.get(request, *args, **kwargs)

        return self.render_to_response(context)

    def populate_crud(self, args, crud, kwargs, request):
        crud.request = request
        crud.args = args
        crud.kwargs = kwargs

    def post(self, request, *args, **kwargs):
        form_name = request.POST.get('_form')
        crud = self.crud_views.get(form_name)

        self.populate_crud(args, crud, kwargs, request)

        if not crud:
            return self.http_method_not_allowed(request, *args, **kwargs)

        return crud.post(request, *args, **kwargs)
