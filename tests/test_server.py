"""Smoke tests for the local server and JSON/vision request contracts (AI is mocked)."""
import importlib.util
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('studyrescue_server', ROOT / 'server.py')
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


class HttpSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        cls.base = f'http://127.0.0.1:{cls.http.server_port}'
        cls.worker = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.worker.start()

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.http.server_close()

    def request(self, path, body=None):
        if body is None:
            req = Request(self.base + path)
        else:
            req = Request(self.base + path, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
        try:
            with urlopen(req, timeout=3) as res:
                return res.status, res.read()
        except HTTPError as e:
            return e.code, e.read()

    def test_static_site_and_status(self):
        for lang in ('en', 'de', 'fr'):
            for page in ('overview', 'tasks', 'planner', 'coach', 'insights', 'settings'):
                code, body = self.request(f'/{lang}/{page}.html')
                self.assertEqual(code, 200)
                self.assertIn(f'data-lang="{lang}"'.encode(), body)
        code, body = self.request('/api/status')
        self.assertEqual(code, 200)
        self.assertIn(b'"languages"', body)

    def test_key_not_in_project(self):
        self.assertEqual(self.request('/server.py')[0], 404)
        self.assertEqual(self.request('/.env')[0], 404)

    def test_no_key_returns_offline_status(self):
        with patch.dict(server.os.environ, {'OPENAI_API_KEY': ''}):
            code, body = self.request('/api/coach', {'lang': 'en', 'today': '2026-10-22'})
            self.assertEqual(code, 503)

    def test_mock_ai_parse(self):
        response = '{"title":"Study chemistry","subject":"science","due":"2026-10-23","minutes":40,"difficulty":2,"importance":2}'
        with patch.dict(server.os.environ, {'OPENAI_API_KEY': 'mock-for-tests'}), patch.object(server, 'ai', return_value=response):
            code, body = self.request('/api/parse', {'lang':'de','today':'2026-10-22','text':'Chemie morgen 40 Minuten'})
            self.assertEqual(code, 200)
            task = json.loads(body)['task']
            self.assertEqual(task['due'], '2026-10-23')
            self.assertEqual(task['subject'], 'science')

    def test_mock_ai_coach(self):
        with patch.dict(server.os.environ, {'OPENAI_API_KEY': 'mock-for-tests'}), patch.object(server, 'ai', return_value='Beginne mit Mathematik.'):
            code, body = self.request('/api/coach', {'lang':'de','today':'2026-10-22','tasks':[], 'availability':[120]*7,'unscheduled':[], 'plannedMinutes':0})
            self.assertEqual(code, 200)
            self.assertEqual(json.loads(body)['analysis'], 'Beginne mit Mathematik.')

    def test_mock_photo(self):
        # Small 1x1 JPEG fixture. The mock tests format handling, not actual vision quality.
        with patch.dict(server.os.environ, {'OPENAI_API_KEY': 'mock-for-tests'}), patch.object(server, 'ai', return_value='{"title":"Math worksheet","subject":"math","due":"2026-10-24","minutes":45,"difficulty":2,"importance":2}'):
            code, body = self.request('/api/photo', {'lang':'fr','today':'2026-10-22','image':'data:image/jpeg;base64,/9j/2Q=='})
            self.assertEqual(code, 200)
            self.assertEqual(json.loads(body)['task']['title'], 'Math worksheet')


if __name__ == '__main__':
    unittest.main()
