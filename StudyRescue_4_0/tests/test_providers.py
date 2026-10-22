"""Unit tests for key selection and AI provider request translation (no paid calls)."""
import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('sr_server_providers', Path(__file__).resolve().parents[1] / 'server.py')
s = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(s)

class ProviderTests(unittest.TestCase):
    def test_no_key(self):
        with patch.dict(os.environ, {'GEMINI_API_KEY':'', 'OPENAI_API_KEY':'','AI_PROVIDER':'auto'}):
            self.assertIsNone(s.get_provider())
    def test_provider_gemini(self):
        with patch.dict(os.environ, {'GEMINI_API_KEY':'test-key','OPENAI_API_KEY':'', 'AI_PROVIDER':'auto','GEMINI_MODEL':'gemini-2.5-flash'}):
            with patch.object(s, 'call_json',return_value={'candidates':[{'content':{'parts':[{'text':'OK'}]}}]}) as request:
                self.assertEqual(s.ai([{'role':'system','content':'Help students'},{'role':'user','content':'Hi'}]),'OK')
                args=request.call_args.args
                self.assertTrue(args[0].startswith('https://generativelanguage.googleapis.com/'))
                self.assertEqual(args[2]['x-goog-api-key'],'test-key')
                self.assertIn('systemInstruction',args[1])
    def test_gemini_vision(self):
        msg=[{'role':'user','content':[{'type':'text','text':'What is this?'},{'type':'image_url','image_url':{'url':'data:image/png;base64,YQ=='}}]}]
        with patch.dict(os.environ, {'GEMINI_API_KEY':'test-key', 'AI_PROVIDER':'gemini'}):
            with patch.object(s,'call_json',return_value={'candidates':[{'content':{'parts':[{'text':'{"title":"HW"}'}]}}]}) as request:
                self.assertEqual(s.ai(msg,json_mode=True),'{"title":"HW"}')
                self.assertEqual(request.call_args.args[1]['contents'][0]['parts'][1]['inlineData']['mimeType'],'image/png')
    def test_provider_openai(self):
        with patch.dict(os.environ, {'OPENAI_API_KEY':'test-openai', 'GEMINI_API_KEY':'','AI_PROVIDER':'auto','OPENAI_MODEL':'gpt-4.1-mini'}):
            with patch.object(s,'call_json',return_value={'choices':[{'message':{'content':'Done'}}]}) as request:
                self.assertEqual(s.ai([{'role':'user','content':'Hello'}],json_mode=True),'Done')
                self.assertEqual(request.call_args.args[0],'https://api.openai.com/v1/chat/completions')
                self.assertEqual(request.call_args.args[2]['Authorization'],'Bearer test-openai')
                self.assertEqual(request.call_args.args[1]['response_format'],{'type':'json_object'})

if __name__=='__main__':
    unittest.main()
