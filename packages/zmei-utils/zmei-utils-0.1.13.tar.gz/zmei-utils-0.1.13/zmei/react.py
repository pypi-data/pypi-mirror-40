import json
import os

from django.conf import settings
from django.http import HttpResponse
from py_mini_racer import py_mini_racer
from py_mini_racer.py_mini_racer import MiniRacerBaseException
from zmei.json import ZmeiReactJsonEncoder

from .views import ZmeiDataViewMixin, ImproperlyConfigured


class ZmeiReactServer(object):
    def __init__(self):
        super().__init__()

        self.loaded_files = []
        self.loaded_files_mtime = {}

        self.jsi = None

        self.checksum = None

    def reload_interpreter(self):
        self.jsi = py_mini_racer.MiniRacer()

        code = """
        var global = this;
        var module = {exports: {}};
        var setTimeout = function(){};
        var clearTimeout = function(){};var console = {
            error: function() {},
            log: function() {},
            warn: function() {}
        };
        """

        self.jsi.eval(code)

        for filename in self.loaded_files:
            self.loaded_files_mtime[filename] = os.path.getmtime(filename)
            self.eval_file(filename)

    def autreload(self):
        if len(self.loaded_files_mtime) == 0:
            return

        for filename in self.loaded_files:
            if self.loaded_files_mtime[filename] != os.path.getmtime(filename):
                print('Reloading ZmeiReactServer')
                self.reload_interpreter()
                break

    def evaljs(self, code):
        if not self.jsi:
            self.reload_interpreter()

        return self.jsi.eval(code)

        # except JSRuntimeError as e:
        #     message = str(e)
        #
        #     message = '\n' + colored('Error:', 'white', 'on_red') + ' ' + message
        #
        #     print(message)
        #     m = re.search('\(line\s+([0-9]+)\)', message)
        #     if m:
        #         print('-' * 100)
        #         print('Source code:')
        #         print('-' * 100)
        #         row = int(m.group(1)) - 1
        #         source = code.splitlines()
        #
        #         line = colored(source[row], 'white', 'on_red')
        #         print('\n'.join([f'{x+1}:\t{source[x]}' for x in range(max(0, row - 10), row)]))
        #         print(f'{row+1}:\t{line}')
        #         print('\n'.join([f'{x+1}:\t{source[x]}' for x in range(row + 1, min(row + 10, len(source) - 1))]))
        #         print('-' * 100)

    def load(self, filename):
        self.loaded_files.append(filename)

    def eval_file(self, filename):
        with open(filename) as f:
            self.evaljs(f.read())


class ZmeiReactViewMixin(ZmeiDataViewMixin):
    react_server = None
    react_components = None
    server_render = True

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if 'application/json' in self.request.META['HTTP_ACCEPT']:
            return HttpResponse(context['react_state'], content_type='application/json')

        return self.render_to_response(context)

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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if not isinstance(self.react_server, ZmeiReactServer):
            raise ImproperlyConfigured('ZmeiReactViewMixin requires react_server property')

        if not isinstance(self.react_components, list):
            raise ImproperlyConfigured('ZmeiReactViewMixin requires react_component property')

        data['react_state'] = ZmeiReactJsonEncoder(view=self).encode(self._get_data())

        if settings.DEBUG:
            self.react_server.autreload()

        if self.server_render:
            for cmp in self.react_components:
                try:
                    data[f'react_page_{cmp}'] = self.react_server.evaljs(f"R.renderServer(R.{cmp}Reducer, R.{cmp}, {data['react_state']});")

                    # print('WARN! Server-side rendering disabled!')
                except MiniRacerBaseException as e:
                    data[f'react_page_{cmp}'] = f'<script>var err = {json.dumps({"msg": str(e)})}; ' \
                                                f'document.body.innerHTML = ' \
                                                "'<h2>Error rendering React component. See console for details.</h2>' + " \
                                                f'"<pre>" + err.msg + "</pre>" + document.body.innerHTML;</script>'

        return data
