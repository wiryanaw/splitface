"""Serve the built site (out/) for a local preview, telling the browser never to cache it, so a
plain reload always shows the latest build.
Usage: python3 tools/serve.py [port]  (from the project folder; port 8792 by default)"""
import functools
import http.server
import os
import sys


class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8792
http.server.ThreadingHTTPServer(("", port), functools.partial(NoCache, directory=root)).serve_forever()
