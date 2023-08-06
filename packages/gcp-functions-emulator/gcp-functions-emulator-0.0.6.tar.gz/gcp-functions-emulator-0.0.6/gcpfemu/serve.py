import os
import sys
import importlib.util
from flask import Flask, request

def http(module_path, function_name, port=5000, debug=False):
    # dinamically import the module and the function to run
    spec = importlib.util.spec_from_file_location('cloud_function', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    dir(module)
    function = getattr(module, function_name)
    # serve the code in the specified route
    app = Flask(__name__)
    @app.route('/' + function_name)
    def index():
        return function(request)
    # listen for connections
    app.run('127.0.0.1', port, debug=debug)

def main():
    # get config variables
    module_path = sys.argv[1]
    function_name = sys.argv[2]
    port = sys.argv[3] or sys.getenv('port') or 5000
    if port is None or module_path is None or function_name is None:
        raise Exception('You have to call the function with params: <modulefile.py> <function_name> [port]')
    http(module_path, function_name, port, debug)

if __name__ == "__main__":
    main()
