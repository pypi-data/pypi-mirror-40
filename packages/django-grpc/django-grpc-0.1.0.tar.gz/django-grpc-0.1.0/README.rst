# django-grpc
Easy way to launch gRPC server with access to Django ORM and other handy staff.  
gRPC request are much faster that traditional HTTP requests because are not
passed through standard middlewares.

## Installation

```bash
pip install django-grpc
``` 

Update settings.py
```python
INSTALLED_APPS = [
    # ...
    'django_grpc',
]

GRPC_SERVICERS = ['dotted.path.to.callback']
```

The callback must look like following:
```python
import my_pb2
import my_pb2_grpc

def grpc_hook(server):
    my_pb2_grpc.add_MYServicer_to_server(MYServicer(), server)

...
class MYServicer(my_pb2_grpc.MYServicer):

    def GetPage(self, request, context):
        response = my_pb2.PageResponse(title="Demo object")
        return response
```

## Usage
```bash
python manage.py grpcserver
```

For development convenience add `--autoreload` flag
