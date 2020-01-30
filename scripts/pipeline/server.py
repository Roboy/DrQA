from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from drqa import pipeline
import json
import logging

global DrQA

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.send_header('x-dino', 'dinos are great')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        query_components = parse_qs(urlparse(self.path).query)
        print(query_components)
        question = ''.join(query_components["question"])
        answers = DrQA.process(question, top_n=3)
        print(answers)
        json_payload = json.dumps({"answers": answers})
        self.wfile.write(bytes(json_payload, encoding="utf-8"))

    def do_HEAD(self):
        self._set_headers()

def run(server_class=HTTPServer, handler_class=S, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    #instance of DrQA
    print("Welcome to DrQA office, please take a seat. The Doc will be ready for you soon!")
    DrQA = pipeline.DrQA(
        cuda=False,
        tokenizer='spacy'
    )
    print("DrQA instantiated!")

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
