# Change Log

All notable changes to this project are documented on [Releases](https://github.com/vemel/awscliv2/releases) page.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [PEP 440](https://www.python.org/dev/peps/pep-0440/).

# [Released]

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