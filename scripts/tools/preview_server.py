#!/usr/bin/env python3
import http.server
import socketserver
import os
from urllib.parse import unquote

ROOT = os.path.join(os.path.dirname(__file__), '..')

def render_markdown(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # strip YAML frontmatter
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            body = parts[2]
        else:
            body = text
    else:
        body = text
    try:
        import markdown
        html = markdown.markdown(body, extensions=['tables','fenced_code'])
    except Exception:
        # fallback minimal conversion
        html = '<pre>' + body.replace('<','&lt;') + '</pre>'
    return f"<html><head><meta charset=\"utf-8\"><title>Preview</title></head><body>{html}</body></html>"

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = unquote(self.path.lstrip('/'))
        if path.endswith('.html'):
            name = path[:-5]
            md = os.path.join(ROOT, '_policies', name + '.md')
            if os.path.exists(md):
                self.send_response(200)
                self.send_header('Content-type','text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(render_markdown(md).encode('utf-8'))
                return
        return super().do_GET()

if __name__ == '__main__':
    port = 8000
    with socketserver.TCPServer(('127.0.0.1', port), Handler) as httpd:
        print(f'Serving preview at http://127.0.0.1:{port}/virtual-power-plant.html')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('Stopping')