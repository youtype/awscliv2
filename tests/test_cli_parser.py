from awscliv2.cli_parser import parse_args, get_version

class TestCliParser:
    def test_parse_args(self):
        assert parse_args(["--install"]).install
        
    def test_get_version(self):
        assert get_version()