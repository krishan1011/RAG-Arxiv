import importlib
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ConfigLoadTest(unittest.TestCase):
    def test_missing_api_keys_do_not_crash_config(self):
        original = {key: os.environ.get(key) for key in ["OPENROUTER_API_KEY", "GEMINI_MODEL"]}
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
            self.assertEqual(config.OPENROUTER_API_KEY, "")
            self.assertEqual(config.GEMINI_MODEL, "")
            self.assertEqual(config.API_HOST, "0.0.0.0")
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
