import importlib
import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ConfigLoadTest(unittest.TestCase):
    def test_missing_api_keys_do_not_crash_config(self):
        env_keys = ["LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL", "API_HOST"]
        original = {key: os.environ.get(key) for key in env_keys}
        env_file = ROOT / ".env"
        env_backup = ROOT / ".env.test_backup"
        has_env = env_file.exists()
        if has_env:
            env_file.rename(env_backup)
        for key in original:
            os.environ.pop(key, None)

        try:
            import config
            importlib.reload(config)
            self.assertEqual(config.LLM_BASE_URL, "http://localhost:11434/v1")
            self.assertEqual(config.LLM_API_KEY, "ollama")
            self.assertEqual(config.LLM_MODEL, "llama3.2:3b")
            self.assertEqual(config.API_HOST, "0.0.0.0")
            self.assertEqual(config.API_TITLE, "PaperPilot")
        finally:
            if has_env and env_backup.exists():
                env_backup.rename(env_file)
            for key, value in original.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value


if __name__ == "__main__":
    unittest.main()
