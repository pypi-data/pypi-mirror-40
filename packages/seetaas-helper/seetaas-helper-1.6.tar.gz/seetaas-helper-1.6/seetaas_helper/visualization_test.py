from __future__ import unicode_literals
import json
import sys
import multiprocessing

import gunicorn.app.base
from gunicorn.six import iteritems

from cgi import parse_qs, escape

class Mapper:
    __mapper_relation = {}

    @staticmethod
    def register(cls, value):
        Mapper.__mapper_relation[cls] = value

    @staticmethod
    def exist(cls):
        if cls in Mapper.__mapper_relation:
            return True
        return False

    @staticmethod
    def get_value(cls):
        return Mapper.__mapper_relation[cls]


class AutoFill(type):
    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls, *args, **kwargs)
        arg_list = list(args)
        if Mapper.exist(cls):
            value = Mapper.get_value(cls)
            arg_list.append(value)
        obj.__init__(*arg_list, **kwargs)
        return obj


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

def response_404(environ, start_response):
   status = '404'

   response_json = json.dumps(dict(code=404, err_msg='Not found'))
   response_bytes = bytes(response_json, encoding = 'utf-8') 

   response_headers = [('Content-Type', 'text/html'),
                  ('Content-Length', str(len(response_json)))]
   
   start_response(status, response_headers)

   return [response_bytes]

def handle_get(environ, start_response):
   status = '200 OK'
   response_json = json.dumps(dict(code=200, data='OK'))
 
   response_bytes = bytes(response_json, encoding = 'utf-8')
 
   data_len = str(len(response_json))
   response_headers = [('Content-Type', 'text/html'),
                  ('Content-Length', data_len)]
   
   start_response(status, response_headers)
   return [response_bytes] 

def handle_post(environ, start_response):
    # the environment variable CONTENT_LENGTH may be empty or missing
   try:
      request_body_size = int(environ.get('CONTENT_LENGTH', 0))
   except (ValueError):
      request_body_size = 0

   request_body = bytes.decode(environ['wsgi.input'].read(request_body_size))
   post_data = parse_qs(request_body)
   
   image_numpy = post_data.get('image_numpy', [''])[0]
   image_numpy = escape(image_numpy)
 
   if len(image_numpy) < 1:
      return response_404(environ, start_response)

   status = '200 OK'
 
   d = Deploy()
 
   response_json = json.dumps(dict(code=200, data=d.f(image_numpy)))
 
   response_bytes = bytes(response_json, encoding = 'utf-8') 
   response_headers = [('Content-Type', 'text/html'),
                  ('Content-Length', str(len(response_json)))]

   start_response(status, response_headers)

   return [response_bytes]
   

def application(environ, start_response):
   method = environ['REQUEST_METHOD']
   path = environ['PATH_INFO']
   if method=='GET' and path == '/_health':
      return handle_get(environ, start_response)
   elif method=='POST' and path == "/":
      return handle_post(environ, start_response)
   else:
      return response_404(environ, start_response)


 
 
class Deploy(metaclass=AutoFill):

    def __init__(self, f=None):
        self.f = f

    @staticmethod
    def register(func):
        Mapper.register(Deploy, func)

    @classmethod
    def run(cls, numworkers=1):
        options = {
            'bind': '%s:%s' % ('0.0.0.0', '2222'),
            'workers': cls.num_of_workers(numworkers),
        }
        StandaloneApplication(application, options).run()

    @classmethod
    def num_of_workers(cls, numworkers=1):
        workers = int(numworkers)
        assert workers > 0, ValueError
        return workers if workers < multiprocessing.cpu_count() * 2 else multiprocessing.cpu_count() * 2



