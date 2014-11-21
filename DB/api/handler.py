import http.server

import url_parser
import db

USAGE = "/(device id)?[start_time=(start time as UTC unix timestamp), end_time=(end time as UTC unix timestamp), type=(Sensor type code)].join('&')"


class ApiHandler(http.server.SimpleHTTPRequestHandler):

	def __init__(self, req, client_addr,server):
		http.server.SimpleHTTPRequestHandler.__init__(self, req, client_addr, server)

	def do_GET(self):
		try:
			parsed = url_parser.parse(self.path)
		except:
			print(self.path)
			if self.path == '/':
				self.send_response(200)
				self.send_header("Content-type", "text/plain")
				self.end_headers()
				self.wfile.write((self.address_string() + USAGE).encode("utf-8"))
				self.wfile.flush()
			else:
				self.send_error(404)
			return

		try:
			r = db.query(parsed)

			self.send_response(200)
			self.send_header("Content-type", "application/json;charset=utf-8")

			self.end_headers()
			self.wfile.write('[\n'.encode("utf-8"))
			for line in r:
				self.wfile.write(line.encode("utf-8"))
			self.wfile.write(']\n'.encode("utf-8"))
		except:
			self.send_error(500)
			return

		self.wfile.flush()
