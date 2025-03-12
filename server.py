import socket
import threading
import json
from urllib.parse import urlparse, parse_qs

class SimpleAPI:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.data = []
        self.data_lock = threading.Lock()

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            print(f'Server running on {self.host}:{self.port}')
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()

    def handle_client(self, conn, addr):
        with conn:
            request = conn.recv(4096).decode()
            if not request:
                return
            response = self.process_request(request)
            conn.sendall(response)

    def parse_request(self, request):
        lines = request.split('\r\n')
        method, full_path, version = lines[0].split()
        headers = {}
        cookies = {}
        body = ''

        i = 1
        while i < len(lines) and lines[i]:
            if ': ' in lines[i]:
                key, value = lines[i].split(': ', 1)
                headers[key.lower()] = value
            i += 1

        if 'cookie' in headers:
            cookie_pairs = headers['cookie'].split('; ')
            for pair in cookie_pairs:
                if '=' in pair:
                    k, v = pair.split('=', 1)
                    cookies[k] = v

        if '\r\n\r\n' in request:
            body = request.split('\r\n\r\n', 1)[1]

        parsed_url = urlparse(full_path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        return method, path, query_params, headers, cookies, body

    def build_response(self, status_code, body, headers=None):
        status_messages = {
            200: 'OK',
            201: 'Created',
            204: 'No Content',
            404: 'Not Found',
            400: 'Bad Request',
            500: 'Internal Server Error'
        }
        status_message = status_messages.get(status_code, 'Unknown')
        response = f'HTTP/1.1 {status_code} {status_message}\r\n'
        headers = headers or {}
        headers['Content-Type'] = 'application/json'
        headers['Content-Length'] = str(len(body.encode()))
        for key, value in headers.items():
            response += f'{key}: {value}\r\n'
        response += '\r\n'
        response += body
        return response.encode()

    def process_request(self, request):
        try:
            method, path, query_params, headers, cookies, body = self.parse_request(request)

            if path == '/items' and method == 'GET':
                with self.data_lock:
                    return self.build_response(200, json.dumps({'status': 'success', 'data': self.data}))

            elif path == '/items' and method == 'POST':
                try:
                    item = json.loads(body)
                    with self.data_lock:
                        self.data.append(item)
                    return self.build_response(201, json.dumps({'status': 'created', 'data': item}))
                except json.JSONDecodeError:
                    return self.build_response(400, json.dumps({'status': 'error', 'message': 'Invalid JSON'}))

            elif path.startswith('/items/') and method == 'PUT':
                try:
                    item_id = int(path.split('/')[-1])
                    updated_item = json.loads(body)
                    with self.data_lock:
                        for i, item in enumerate(self.data):
                            if item.get('id') == item_id:
                                self.data[i] = updated_item
                                return self.build_response(200, json.dumps({'status': 'updated', 'data': updated_item}))
                    return self.build_response(404, json.dumps({'status': 'not found'}))
                except (ValueError, json.JSONDecodeError):
                    return self.build_response(400, json.dumps({'status': 'error', 'message': 'Invalid input'}))

            elif path.startswith('/items/') and method == 'DELETE':
                try:
                    item_id = int(path.split('/')[-1])
                    with self.data_lock:
                        for i, item in enumerate(self.data):
                            if item.get('id') == item_id:
                                del self.data[i]
                                return self.build_response(204, '')
                    return self.build_response(404, json.dumps({'status': 'not found'}))
                except ValueError:
                    return self.build_response(400, json.dumps({'status': 'error', 'message': 'Invalid ID'}))

            else:
                return self.build_response(404, json.dumps({'status': 'error', 'message': 'Invalid endpoint or method'}))

        except Exception as e:
            return self.build_response(500, json.dumps({'status': 'error', 'message': str(e)}))

if __name__ == '__main__':
    api = SimpleAPI()
    api.start_server()
