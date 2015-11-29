import http.server

import url_parser
import db

USAGE = "Usage: http://db.sead.systems:8080/(device id)['?' + '&'.join(.[[start_time=(start time as UTC unix timestamp)]\n" \
		", [end_time=(end time as UTC unix timestamp)], [type=(Sensor type code),[device=(seadplug for SEAD plug,\n" \
		"egauge or channel name for eGauge), granularity=(interval between data points in seconds of an energy list\n" \
		"query, must also include list_format=energy and type=P), diff=(1 get the data differences instead of the data)]]],\n" \
		" [subset=(subsample result down to this many rows)], [list_format=(string representing what the json list entries\n" \
		"will look like)], [limit=(truncate result to this many rows)], [json=(1 get the result in pseudo JSON format)]]\n"


class ApiHandler(http.server.SimpleHTTPRequestHandler):

	def __init__(self, req, client_addr,server):
		http.server.SimpleHTTPRequestHandler.__init__(self, req, client_addr, server)

	def do_GET(self):
		try:
			parsed = url_parser.parse(self.path)
		except Exception as inst:
			if self.path == '/':
				self.send_response(200)
				self.send_header("Content-type", "text/plain")
				self.end_headers()
				self.wfile.write(USAGE.encode("utf-8"))
				self.wfile.flush()
			else:
				print(type(inst))
				print(inst.args)
				print(inst)

				self.send_error(404)
			return

		try:
			r = db.query(parsed)

			self.send_response(200)
			self.send_header("Content-type", "application/json;charset=utf-8")  # Not actually using JSON format. Causes errors in Chrome when it tries to validate
			self.send_header("Access-Control-Allow-Origin", "*")
			self.end_headers()
			for line in r:
				self.wfile.write(line.encode("utf-8"))
		except Exception as inst:
			self.send_error(500)
			print(type(inst))
			print(inst.args)
			print(inst)

			return

		self.wfile.flush()
