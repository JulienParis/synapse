import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, socketio


# CONFIG = {
#     # 'mode': 'wsgi',
#     'working_dir': '/apps/synapse',
#     # 'python': '/usr/bin/python',
#     'args': (
#         '--bind=0.0.0.0:5000',
#         '--workers=3',
#         '--timeout=120',
#         'app.run_pesticides_prod',
#     ),
# }


if __name__ == "__main__":
    app.run_synapse_prod()



### start gunicorn from terminal :
### from : /apps/synapse/
### run command                 : gunicorn --bind 0.0.0.0:5000 wsgi:app
### run command in background   : gunicorn --bind 0.0.0.0:5000 wsgi:app &
### run command in background   : gunicorn --bind 0.0.0.0:5000 --timeout=120 --workers=1 --worker-class=eventlet wsgi:app &
