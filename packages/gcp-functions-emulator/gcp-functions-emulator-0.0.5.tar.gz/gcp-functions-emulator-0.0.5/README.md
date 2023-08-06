This module tries to emulate the environment in Google Cloud Functions for
Python. It serves the given function on the given module.

For example. lets imagine we have the following cloud function
```python
# mycloudfunction.py
def api(request):
  return 'important data'
```
To emulate we have to call it like so
```
$ python -m gcp-functions-emulator.http mycloudfunction.py api
```
And to access the data we can use for example curl
```
$ curl localhost:5000/api
important data
```

If you run the server from a terminal, you have to disable the debug. It is
disabled by default thoug. Flask looks for file changes, but in interactive
terminal there's no file.
```python
from serve import http
port = 5000
module_path = 'mycloudfunction.py'
function_name = 'api'
debug = False
http(module_path, function_name, port, debug)
```
