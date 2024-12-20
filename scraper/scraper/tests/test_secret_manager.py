from unittest.mock import MagicMock, patch

import pytest

from scraper.config.secret_manager import build_env_json

sample_yaml_content = """
secrets:
  TEST: YWdlLWVuY3J5cHRpb24ub3JnL3YxCi0+IFgyNTUxOSBTa1RkTEVZZWdEbnI1Rmgyb2RzdEc3L1hkWXozYWk5RkZmMlk5TUpFSWljCm9ldTJBN2xEYXlFaFdiNmJsUXR4eklxTllBV2JjTi9Yb2czTUxrRElnWmsKLS0tIDNYbWNvNnFUeDFrb2VZZ3FCcGsyOWNtZ25hQXMrWi91cGY5endYeGo2UlEK61yW+mYcM0my9NH6B2X3o2L3CfCNveVXm9PtV5V/0R7w2Ue2aWUrrEUL3SXEwSNIMAQ=
"""
sample_decrypted_value = "my-secret-value"


@pytest.fixture
def mock_subprocess_run():
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = sample_decrypted_value.encode("utf-8")
        mock_run.return_value = mock_result
        yield mock_run


def test_load_and_decrypt_secrets(mock_subprocess_run, tmp_path):
    yaml_file_path = tmp_path / "dev.yaml"
    yaml_file_path.write_text(sample_yaml_content)
    temp_output = tmp_path / "env.json"
    private_key_path = "/workspaces/AustinRent/secrets/austin-rent-key.txt"
    decrypted_secrets = build_env_json(yaml_file_path, private_key_path, temp_output)
    assert decrypted_secrets == {"TEST": sample_decrypted_value}
    mock_subprocess_run.assert_called_once()


def test_load_and_decrypt_env_vars(mock_subprocess_run, tmp_path):
    sample_yaml_content = """
    secrets:
      TEST: YWdlLWVuY3J5cHRpb24ub3JnL3YxCi0+IFgyNTUxOSBTa1RkTEVZZWdEbnI1Rmgyb2RzdEc3L1hkWXozYWk5RkZmMlk5TUpFSWljCm9ldTJBN2xEYXlFaFdiNmJsUXR4eklxTllBV2JjTi9Yb2czTUxrRElnWmsKLS0tIDNYbWNvNnFUeDFrb2VZZ3FCcGsyOWNtZ25hQXMrWi91cGY5endYeGo2UlEK61yW+mYcM0my9NH6B2X3o2L3CfCNveVXm9PtV5V/0R7w2Ue2aWUrrEUL3SXEwSNIMAQ=
    env_vars:
      MY_ENV_VAR: my-env-var-value
    """
    yaml_file_path = tmp_path / "dev.yaml"
    yaml_file_path.write_text(sample_yaml_content)
    temp_output = tmp_path / "env.json"
    private_key_path = "/workspaces/AustinRent/secrets/austin-rent-key.txt"
    decrypted_secrets = build_env_json(yaml_file_path, private_key_path, temp_output)
    assert decrypted_secrets == {"TEST": sample_decrypted_value}
    mock_subprocess_run.assert_called_once()


def test_load_and_decrypt_secrets_invalid_yaml(tmp_path):
    invalid_yaml_content = """
    secrets:
        TEST: pass
        INVALID
    """
    yaml_file_path = tmp_path / "invalid_dev.yaml"
    yaml_file_path.write_text(invalid_yaml_content)
    temp_output = tmp_path / "env.json"
    private_key_path = "/workspaces/AustinRent/secrets/austin-rent-key.txt"

    with pytest.raises(Exception, match="Error loading YAML file:"):
        build_env_json(yaml_file_path, private_key_path, temp_output)
