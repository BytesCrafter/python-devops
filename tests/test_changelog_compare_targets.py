# pyright: reportAttributeAccessIssue=false, reportArgumentType=false

import os
import runpy
import sys
import tempfile
import types
from pathlib import Path
import unittest


class DummyResponse:
    def __init__(self, payload):
        self.status_code = 200
        self._payload = payload

    def json(self):
        return self._payload


class RequestsStub:
    def __init__(self):
        self.calls = []

    def get(self, url, headers=None):
        self.calls.append(url)
        if len(self.calls) == 1:
            return DummyResponse(
                [
                    {
                        "title": "Add compare target verification",
                        "number": 99,
                        "user": {"login": "bob"},
                        "closed_at": "2026-06-05T12:00:00Z",
                        "html_url": "https://github.com/BytesCrafter/python-devops/pull/99",
                    }
                ]
            )
        return DummyResponse([])


class ChangelogCompareTargetTests(unittest.TestCase):
    def test_pull_query_uses_configured_compare_branches(self):
        requests_stub = RequestsStub()
        openai_stub = types.ModuleType("openai")

        class DummyOpenAI:
            def __init__(self, api_key=None):
                self.api_key = api_key

        openai_stub.OpenAI = DummyOpenAI

        dotenv_stub = types.ModuleType("dotenv")
        dotenv_stub.load_dotenv = lambda *args, **kwargs: None

        original_modules = {
            name: sys.modules.get(name)
            for name in ("requests", "openai", "dotenv")
        }

        try:
            sys.modules["requests"] = requests_stub
            sys.modules["openai"] = openai_stub
            sys.modules["dotenv"] = dotenv_stub

            with tempfile.TemporaryDirectory() as tmpdir:
                env_updates = {
                    "ASSISTANT_NAME": "TEST",
                    "PROJECT_PATH": tmpdir,
                    "RELEASE_NAME": "DevOps Automation Script by BytesCrafter",
                    "RELEASE_VERSION": "1.0.0",
                    "RELEASE_DATE": "June 5, 2026",
                    "GITHUB_OWNER": "BytesCrafter",
                    "GITHUB_REPO": "python-devops",
                    "GITHUB_TOKEN": "dummy-token",
                    "GITHUB_TARGET": "pulls",
                    "GITHUB_COMPARED_BASE": "mainline",
                    "GITHUB_COMPARED_HEAD": "release-candidate",
                    "CHANGELOG_SANITIZATION_PATTERN": "^$",
                    "CHANGELOG_SPECIAL_NOTE": "None",
                    "CHANGELOG_OPENAI_SUMMARIZE": "False",
                    "CHANGELOG_ITEM_OPENAI_TITLE": "False",
                    "CHANGELOG_NOTE_OPENAI_GENERATE": "False",
                    "CHANGELOG_ITEM_WITH_TIME": "False",
                }

                previous_env = {key: os.environ.get(key) for key in env_updates}
                os.environ.update(env_updates)
                try:
                    runpy.run_path("changelog.py", run_name="__main__")
                finally:
                    for key, value in previous_env.items():
                        if value is None:
                            os.environ.pop(key, None)
                        else:
                            os.environ[key] = value

                changelog_path = Path(tmpdir) / "CHANGELOG.md"
                self.assertTrue(changelog_path.exists(), "CHANGELOG.md should be generated")
                changelog_content = changelog_path.read_text(encoding="utf-8")
                self.assertIn("Add compare target verification", changelog_content)
                self.assertEqual(len(requests_stub.calls), 2)
                self.assertIn("base=mainline", requests_stub.calls[0])
                self.assertIn("head=release-candidate", requests_stub.calls[0])
                self.assertNotIn("base=release", requests_stub.calls[0])
                self.assertNotIn("head=develop", requests_stub.calls[0])
        finally:
            for name, module in original_modules.items():
                if module is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = module

    def test_missing_optional_boolean_flags_do_not_crash(self):
        requests_stub = RequestsStub()
        openai_stub = types.ModuleType("openai")

        class DummyOpenAI:
            def __init__(self, api_key=None):
                self.api_key = api_key

        openai_stub.OpenAI = DummyOpenAI

        dotenv_stub = types.ModuleType("dotenv")
        dotenv_stub.load_dotenv = lambda *args, **kwargs: None

        original_modules = {
            name: sys.modules.get(name)
            for name in ("requests", "openai", "dotenv")
        }

        try:
            sys.modules["requests"] = requests_stub
            sys.modules["openai"] = openai_stub
            sys.modules["dotenv"] = dotenv_stub

            with tempfile.TemporaryDirectory() as tmpdir:
                env_updates = {
                    "ASSISTANT_NAME": "TEST",
                    "PROJECT_PATH": tmpdir,
                    "RELEASE_NAME": "DevOps Automation Script by BytesCrafter",
                    "RELEASE_VERSION": "1.0.0",
                    "RELEASE_DATE": "June 5, 2026",
                    "GITHUB_OWNER": "BytesCrafter",
                    "GITHUB_REPO": "python-devops",
                    "GITHUB_TOKEN": "dummy-token",
                    "GITHUB_TARGET": "pulls",
                    "GITHUB_COMPARED_BASE": "mainline",
                    "GITHUB_COMPARED_HEAD": "release-candidate",
                    "CHANGELOG_SANITIZATION_PATTERN": "^$",
                }

                previous_env = {key: os.environ.get(key) for key in env_updates}
                os.environ.update(env_updates)
                try:
                    runpy.run_path("changelog.py", run_name="__main__")
                finally:
                    for key, value in previous_env.items():
                        if value is None:
                            os.environ.pop(key, None)
                        else:
                            os.environ[key] = value

                changelog_path = Path(tmpdir) / "CHANGELOG.md"
                self.assertTrue(changelog_path.exists(), "CHANGELOG.md should be generated")
                changelog_content = changelog_path.read_text(encoding="utf-8")
                self.assertIn("Add compare target verification", changelog_content)
                self.assertEqual(len(requests_stub.calls), 2)
                self.assertIn("base=mainline", requests_stub.calls[0])
                self.assertIn("head=release-candidate", requests_stub.calls[0])
        finally:
            for name, module in original_modules.items():
                if module is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = module


if __name__ == "__main__":
    unittest.main()
