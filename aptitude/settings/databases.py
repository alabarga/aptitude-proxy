from  django.utils.deprecation import MiddlewareMixin

import threading
request_cfg = threading.local()

class RouterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        url_host = request.META.get("HTTP_HOST")
        request_cfg.db = 'default'
        if url_host.startswith("cat."):
            request_cfg.db = "cat"

        return None

    def process_response(self, request, response ):
        return response


class DatabaseRouter:
    def _default_db(self):
        if hasattr( request_cfg, 'db' ):
            database_config=request_cfg.db
        else:
            database_config='default'

        return database_config

    def db_for_read(self, model, **hints):
        return self._default_db()


    def db_for_write(self, model, **hints):
        return self._default_db()
