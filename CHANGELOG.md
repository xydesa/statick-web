# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## Unreleased

### Added

### Fixed

### Removed

## v0.0.6 - 2021-05-28

### Changed

- Switch type hints from comment style to inline style.
- Renaming plugin directories to match Statick's directory structure.
- For testing with Actions, the installed version of Node was upgraded from v10 to v14.
  Node v10 is no longer supported.
  Node v14 is recommended by the developers as it is a long-term support (LTS) release.

### Removed

- Remove testing support for Ubuntu 16.04 and Python 3.5.
  There is no guarantee Statick will work in those environments any longer.

## v0.0.5 - 2021-05-03

This is expected to be the final release that supports Python 3.5.
Ubuntu 16.04 has reached end-of-life status.
The final release of ROS Kinetic has been made.
See <https://github.com/sscpac/statick/discussions/290> for a discussion on Python 3.5 support in Statick.

### Added

- Add support for locally installed eslint configs and plugins.
  Adding `install_dir` config option to specify where eslint's plugins and configs are installed.
  On Ubuntu, locally installed eslint configs and plugins are required for eslint versions >= 6.0.0:
  <https://eslint.org/docs/user-guide/migrating-to-6.0.0#plugins-and-shareable-configs-are-no-longer-affected-by-eslints-location>
- Add support for parsing eslint error lines.

## v0.0.4 - 2021-01-19

### Changed

- Convert use of print() and show tool output flags to the built-in Python logging module. (Thomas Denewiler, @tdenewiler)

## v0.0.3 - 2020-12-22

### Added

- Take advantange of new `DiscoveryPlugin.find_files` function that only walks a package's path once instead of
  in each discovery plugin.
  This should lead to a speed improvement in the discovery phase. (Alexander Xydes, @xydesa)

## v0.0.2 - 2020-04-06

### Added

- Installing all tool rc files with this package.
  Added new separate levels and corresponding profiles for each separate tool.
  Using installed markdownlintrc file instead of copying into this repo.
- Publishing tags to pypi.
- Formatted all code using black. Added Github Action to ensure future commits are consistent with black formatting.
- Using markdownlint statick plugin to check documentation files.

### Changed

- Switched from travis ci to github actions.

### Fixed

- Limit discovery plugins to only find files corresponding to the tools specified. (Thomas Denewiler, @tdenewiler)

## v0.0.1 - 2020-02-14

### Added

- Initial release (Alexander Xydes, @axydes)
