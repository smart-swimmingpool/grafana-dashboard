# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- New dashboard for Pool Controller v5.x (Home Assistant MQTT discovery + InfluxDB integration):
  temperatures, pump state timeline, operation mode, effective runtime, circulation extension
  and diagnostics (WiFi, uptime, free heap, controller temperature)
- `scripts/generate_dashboard.py` to generate the dashboard JSON
- Dashboard screenshot (example data) in `docs/`
- Added Super-Linter v8.7.0 workflow for code quality checks
- Added CODE_OF_CONDUCT.md (Contributor Covenant v1.4)
- Added CONTRIBUTING.md with development guidelines
- Added comprehensive documentation

### Changed

- Renamed the openHAB based dashboard for Pool Controller v1/v2 to
  `dashboard-smart-swimming-pool-openhab-legacy.json`
- Rewrote README to match the actual dashboards
- Updated GitHub Actions to use actions/checkout@v7 (was v2)
- Updated actions/cache to v3 (was v2)
- Updated actions/setup-python to v5 (was v2)

### Fixed

- Fixed outdated GitHub Actions versions

## [1.0.0] - 2024-01-01

### Features

- Initial release of Smart Swimming Pool Grafana Dashboard
- Temperature monitoring panels
- Pump and solar heating status panels
- MQTT data source configuration
- Time series visualizations

[Unreleased]: https://github.com/smart-swimmingpool/grafana-dashboard/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/smart-swimmingpool/grafana-dashboard/releases/tag/v1.0.0
