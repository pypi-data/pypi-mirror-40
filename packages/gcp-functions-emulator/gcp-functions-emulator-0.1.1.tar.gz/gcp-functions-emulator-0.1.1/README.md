# Google Cloud Functions Python Emulator

![downloads](https://img.shields.io/pypi/dm/gcp-functions-emulator.svg?style=flat-square)
![build](https://gitlab.com/divisadero/cloud-functions-python-emulator/badges/master/pipeline.svg?style=flat-square)

This module tries to emulate the environment in Google Cloud Functions for
Python. It serves the given function on the given module.

For example. lets imagine we have the following cloud function
```python
# mycloudfunction.py
def api(request):
  return 'important data'
```
To emulate we have to call it like so:
```
$ gcpfemu <path/to/file.py> <function_name>
```
For example, with the code above we will call it:
```
$ gcpfemu mycloudfunction.py api
```
And to access the data we can use for example curl:
```
$ curl localhost:5000/api
important data
```

If you want to run the emulator programatically you can do drun the server 
from a terminal, you have to disable the debug. It is
disabled by default thoug. Flask looks for file changes, but in interactive
terminal there's no file.
```python
from gcpfemu import http 
port = 1234 # use a different port
module_path = 'mycloudfunction.py' # set the path to the code itself
function_name = 'api' # set the function name
http(module_path, function_name, port, debug) # load and serve the function
```
