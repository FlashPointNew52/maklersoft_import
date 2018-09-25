#!/usr/bin/env python3
import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
from pprint import pprint
from time import sleep
from present_parser_V2 import PresentParser as PP
from avito_parser_V2 import AvitoParser as AV
from farpost_parser_V2 import FarpostParser as FP


class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        message = None
        data = None

        if self.path == '/favicon.ico':
            pass

        else:
            path = self.path.split('?')[0]
            if path == '/get_media_data':

                params_size = len(self.path.split('?'))

                if params_size == 2 and self.path.split('?')[1] != '':

                    try:
                        query_path = self.path
                        query_url = parse.parse_qs(parse.urlparse(query_path).query)['url'][0]
                        query_ip = parse.parse_qs(parse.urlparse(query_path).query)['ip'][0]
                        query_source = query_url.split('/')[2].replace('www', '').replace('.ru', '').replace('.', '')

                        if requests.get(query_url).status_code != requests.codes.ok:
                            message = "Invalid url!\r\n"

                        else:
                            params = {
                                'source': query_source,
                                'url': query_url,
                                'ip': query_ip
                            }

                            if params['source'] == 'present-dv':
                                try:
                                    data = PP().get_data(params['url'])
                                except SystemExit:
                                    message = "Present-script error!\r\n"

                            elif params['source'] == 'avito':
                                try:
                                    data = AV().get_data(params['url'])
                                except SystemExit:
                                    message = "Avito-script error!\r\n"

                            elif params['source'] == 'farpost':
                                try:
                                    data = FP().get_data(params['url'])
                                except SystemExit:
                                    message = "Farpost-script error!\r\n"

                            else:
                                message = "Params not found!\r\n"

                    except KeyError:
                        message = "Params is not full!\r\n"

                else:
                    message = "Params is null!\r\n"

            else:
                message = "Path not found!\r\n"

            if data:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                # pprint(data)
                self.wfile.write(json.dumps(data, ensure_ascii=False).encode())


            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                # self.wfile.write(bytes(message, "utf8"))


if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 8080
    print('Run server: http://{0}:{1}'.format(HOST, PORT))
    httpd = HTTPServer((HOST, PORT), Serv)
    httpd.serve_forever()
