from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from json import dumps
import sys
from cowpy import cow

ADDRESS = ('127.0.0.1', 3000)

INDEX = b'''<!DOCTYPE html>
<html>
<head>
    <title> cowsay </title>
</head>
<body>
    <header>
        <nav>
        <ul>
            <li><a href="/cowsay">cowsay</a></li>
        </ul>
        </nav>
    <header>
    <main>
        <p>This website provides an api linked above.  It /
        can be used to generate cowsay messages in raw test or JSON</p>
    </main>
</body>
</html>
'''
COWSAY = b'''<!DOCTYPE html>
<html>
<head>
    <title> cowsay api docs </title>
</head>
<body>
    <header>
        <nav>
        <ul>
            <li><a href="..">home</a></li>
        </ul>
        </nav>
    <header>
    <main>
        <div>
            <p>An iendpoint is provided at the following path:
            /cow[?msg=message]. If the message is not provided a default/
             message will be inserted.  A POST at the endpoint will respond/
              with a json document of the following form:</p>
            <code>{"content: string response from GET}</code>
        <div>
        <div>
        examples below:
        </div>
        <ul>
            <li>
                <a href="/cow?msg=Hello user!"></iframe></a>
            </li>
            <li>
                <a href="/cow">cow
                <iframe src="/cow></iframe>
                </a>
            </li>
        </ul>
    </main>
</body>
</html>
'''


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    COW = cow.get_cow()()

    def get_index(self, parsed_path):
        """ handle '/' path get request """
        self.send_response(200)
        self.end_headers()
        self.wfile.write(INDEX)

    def get_cow(self, parsed_path):
        """handles /cow[?msg=message>] path get request """
        parsed_qs = parse_qs(parsed_path.query)
        msg_option = parsed_qs.get('msg')
        if msg_option is None:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'')
            return
        msg = msg_option[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(self.COW.milk(msg).encode())

    def post_cow(self, parsed_path):
        """handles /cow[?msg=message>] path post request """
        parsed_qs = parse_qs(parsed_path.query)
        msg = parsed_qs.get('msg')[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(dumps({"content": self.COW.milk(msg)}).encode())

    def do_GET(self):
        """ runs generic get.  handles 404 status """
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/':
            return self.get_index(parsed_path)

        if parsed_path.path == '/cowsay':
            return self.get_cowsay(parsed_path)

        if parsed_path.path == '/cow':
            return self.get_cow(parsed_path)

        print(parsed_path.path)
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Not found')

    def do_POST(self):
        """ Dispatch post to known pathsw or handle 404 status """
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/cow':
            return self.post.cow(parsed_path)

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Not Found')


def create_server():
    """ initialize server for cowsay """
    return HTTPServer(ADDRESS, SimpleHTTPRequestHandler)


def main():
    """ Entry point for server app """
    with create_server() as server:
        print(f'Starting server on port { ADDRESS[1] }')
        server.serve_forever()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print(f'Stopping server on port { ADDRESS[1] }')
