# Change Log

All notable changes to this project are documented on [Releases](https://github.com/vemel/awscliv2/releases) page.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [PEP 440](https://www.python.org/dev/peps/pep-0440/).

# [Released]

## [1.4.1] - 2020-09-03

### Fixed

- `awsv2 --assume-role` command now sets `aws_session_token` in `~/.aws/credentials`
- `awsv2 configure` sometimes did not output to `stdout` correctly

## [1.4.0] - 2020-09-02

### Added

- `aws_session_token` support to `awsv2 --configure`

### Changed

- `awsv2 --configure` no longer runs docker, changes file locally instead

## [1.3.1] - 2020-09-02

### Fixed

- Error if `$HOME/.aws` path does not exist

## [1.3.0] - 2020-09-02

### Added

- `awsv2 --assume-role <name> <source_profile> <role_arn>` command

### Fixed

- Files in `.aws` folder belonged to `root` user if they were created by `awsv2`

## [1.2.0] - 2020-08-30

### Added

- Support for interactive commands like `awsv2 configure`

### Changed

- Instructions output how to install `docker` if it was not found

### Fixed

- Error while running in non-TTY environment
- Error caused by keyboard interrupt
- `-U`/`--update` command did not return correct exit code

## [1.1.0] - 2020-08-29

### Added

- `-U`/`--update` CLI argument to pull latest `amazon/aws-cli` image

### Changed

- `-V`/`--version` command shows underlying image version
- `region_name` removed from `--configure` command

## [1.0.0] - 2020-08-29

Initial release