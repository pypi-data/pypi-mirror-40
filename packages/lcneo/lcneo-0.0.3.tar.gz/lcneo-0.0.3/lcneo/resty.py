import cgi

def notfound_404(environ, start_response):
	start_response("404 Not Found", [('Content-type', 'text/plain')])
	return [b"Not Found"]

class PathDispatcher:
	def __init__(self):
		self.pathmap = { }

	def __call__(self, environ, start_response):
		path = environ["PATH_INFO"]
		params = cgi.FieldStorage(environ['wsgi.input'],
								environ=environ)
		method = environ['REQUEST_METHOD'].lower()
		environ["params"] = {key: params.getvalue(key) for key in params}
		handler = self.pathmap.get((method, path), notfound_404)
		return handler(environ, start_response)

	def register(self, method, path, function):
		self.pathmap[method.lower(), path] = function
		return function

import time

_hello_resp= """\
<html>
	<head>
		<title>Hello {name}</title>
	</head>
	<body>
		<h1>Hello {name}!</h1>
	</body>
</html>"""

def hello_world(environ, start_response):
	start_response("200 OK", [('Content-type', "text/html")])
	params = environ['params']
	resp = _hello_resp.format(name=params.get('name'))
	yield resp.encode("utf-8")

_localtime_resp="""\
<?xml version="1.0"?>
<time>
	<year>{t.tm_year}</year>
	<month>{t.tm_mon}</month>
	<day>{t.tm_mday}</day>
	<hour>{t.tm_hour}</hour>
	<minute>{t.tm_min}</minute>
	<second>{t.tm_sec}</second>
</time>"""


def localtime(environ, start_response):
	start_response("200 OK", [('Content-type', "application/xml")])
	resp = _localtime_resp.format(t=time.localtime())
	yield resp.encode("utf-8")

# Index page
_index_resp="""\
<!DOCTYPE html>
<html>
<head>
	<!-- 最新版本的 Bootstrap 核心 CSS 文件 -->
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

	<!-- 可选的 Bootstrap 主题文件（一般不用引入） -->
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

	<!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
	<title></title>
</head>
<body class="container">
    <!-- Begin page content -->
    <div class="container">

      <div class="page-header">
        <h1>Lcneo toolkit</h1>
      </div>
			<span class="label label-primary">License | MIT</span>
			<span class="label label-success">Build | passing</span>
      <p class="lead">Just a demo ...</p>
      <p>This toolkit only contains some tools or code that I use.</p>
    </div>
</body>
</html>"""
def home(environ, start_response):
	start_response("200 OK", [('Content-type', "text/html")])
	resp = _index_resp
	yield resp.encode("utf-8")

# Start service
def start(port=8080):
	from wsgiref.simple_server import make_server

	# Create the dispatcher and register functions
	dispatcher = PathDispatcher()
	dispatcher.register("GET", "/", home)
	dispatcher.register("GET", "/hello", hello_world)
	dispatcher.register("GET", "/localtime", localtime)

	# Launch a basic server
	httpd = make_server("", port, dispatcher)
	print("Serving on port {0}....".format(port))
	httpd.serve_forever()

if __name__ == '__main__':
	from wsgiref.simple_server import make_server

	# Create the dispatcher and register functions
	dispatcher = PathDispatcher()
	dispatcher.register("GET", "/", home)
	dispatcher.register("GET", "/hello", hello_world)
	dispatcher.register("GET", "/localtime", localtime)

	# Launch a basic server
	httpd = make_server("", 8080, dispatcher)
	print("Serving on port 8080....")
	httpd.serve_forever()
