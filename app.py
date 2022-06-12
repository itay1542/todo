from gevent.pywsgi import WSGIServer
from gevent import monkey; monkey.patch_all()

from src.app_factory import build_app

app = build_app()

if __name__ == '__main__':
    server_bind_ip = app.config["SERVER_BIND_IP"]
    server_bind_port = app.config["SERVER_BIND_PORT"]

    print(F"listening on port {server_bind_port}")
    server = WSGIServer((server_bind_ip, server_bind_port), application=app)
    server.serve_forever()
