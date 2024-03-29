from unittest.mock import Mock

from awscliv2.api import AWSAPI


class TestAWSAPI:
    def test_get_awscli_v2_cmd(self):
        assert AWSAPI().get_awscli_v2_cmd()[0]

    def test_execute(self):
        awsapi = AWSAPI()
        awsapi._run_subprocess = Mock()
        awsapi._run_subprocess.return_value = 0
        assert awsapi.execute(["--version"]) == ""
