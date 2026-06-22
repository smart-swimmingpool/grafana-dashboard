# Contributing to Grafana Dashboard

Thank you for your interest in contributing to the **Smart Swimming Pool Grafana Dashboard** project!


This document provides guidelines for contributing to the project. Please read it
carefully before submitting your first pull request.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Getting Started](#getting-started)
- [Dashboard Structure](#dashboard-structure)
- [Pull Request Process](#pull-request-process)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Quality Gates](#quality-gates)

---

## Code of Conduct

This project adheres to the
[Contributor Covenant](https://www.contributor-covenant.org/version/1/4/code-of-conduct.html).
By participating, you are expected to uphold this code. Please report unacceptable
behavior to
[project maintainers](https://github.com/smart-swimmingpool/grafana-dashboard/graphs/contributors).

See also: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

---

## 🌟 How to Contribute

### Reporting Issues

- **Check existing issues**: Search
  [GitHub Issues](https://github.com/smart-swimmingpool/grafana-dashboard/issues)
  before creating a new one
- **Use the issue template**: Provide detailed information about the issue
- **Include**:
  - Grafana version
  - Screenshot of the issue
  - Expected vs. actual behavior
  - Browser/OS information (if UI-related)

### Suggesting Enhancements

- **Check the roadmap**: See [README.md](README.md) for planned features
- **Discuss first**: Open a
  [GitHub Discussion](https://github.com/smart-swimmingpool/smart-swimmingpool.github.io/discussions)
  to discuss your idea
- **Check for duplicates**: Search existing issues and PRs

### Submitting Pull Requests

- **Fork the repository**: Create your own fork
- **Create a feature branch**: Use descriptive branch names
  (e.g., `feat/add-solar-heating-panel`)
- **Test your changes**: Verify the dashboard JSON is valid
- **Update documentation**: Keep docs in sync with changes

---

## Getting Started

### Prerequisites

- Basic knowledge of Grafana dashboards
- JSON editor (VS Code, etc.)
- Understanding of Smart Swimming Pool MQTT topics

### Setting Up

```bash
# Clone the repository
git clone https://github.com/smart-swimmingpool/grafana-dashboard.git
cd grafana-dashboard

# Validate the dashboard JSON
python -m json.tool dashboard-smart-swimming-pool.json > /dev/null
```text

---

## 📁 Dashboard Structure

The main dashboard file is `dashboard-smart-swimming-pool.json` which contains:

- **Title and Description**: Dashboard metadata
- **Panels**: Individual visualization components
- **Variables**: Template variables for dynamic filtering
- **Data Sources**: MQTT data source configuration
- **Layout**: Panel positioning and sizing

### Key MQTT Topics Used

```text
smart-swimmingpool/pool-controller/state
smart-swimmingpool/pool-controller/temperature/pool
smart-swimmingpool/pool-controller/temperature/solar
smart-swimmingpool/pool-controller/pump/state
smart-swimmingpool/pool-controller/solar/state
smart-swimmingpool/pool-controller/mode
```text

---

## Dashboard Development Guidelines

### Best Practices

1. **Panel Organization**: Group related metrics together
2. **Color Schemes**: Use consistent color schemes across panels
3. **Units**: Always specify units for numeric values
4. **Descriptions**: Add descriptive tooltips for panels
5. **Variables**: Use template variables for dynamic filtering
6. **Time Ranges**: Set appropriate default time ranges

### Panel Types

- **Stat**: For single value displays (temperature, pump status)
- **Graph**: For time series data (temperature history)
- **Gauge**: For current values with thresholds
- **Bar Gauge**: For comparative displays
- **Table**: For tabular data

---

## 🔄 Pull Request Process

1. **Fork the repository** and create your branch from `master`
2. **Make your changes** following the guidelines above
3. **Validate your JSON**: Ensure the dashboard JSON is valid
4. **Test in Grafana**: Import and test your changes
5. **Update documentation** if applicable
6. **Commit your changes** with clear, descriptive messages
7. **Push to your fork** and submit a pull request

### Pull Request Requirements

- ✅ Valid JSON (test with `python -m json.tool`)
- ✅ Dashboard imports successfully in Grafana
- ✅ All panels display correctly
- ✅ Documentation is updated
- ✅ Clear commit messages

---

## Commit Message Guidelines

### Format

```text
type(scope): subject

body

footer
```text

### Types
- `feat`: New feature/panel
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting changes (no functional changes)
- `refactor`: Dashboard restructuring
- `chore`: Maintenance tasks

### Example
```text
feat(panels): add solar heating efficiency panel

- Add new panel showing solar heating efficiency over time
- Use temperature differential calculation
- Add threshold for optimal efficiency range

Closes #123
```text

---

## 🏆 Quality Gates

All contributions must pass the following quality checks:

1. **JSON Validation**: Dashboard JSON must be valid
2. **Super-Linter**: Code quality and style checks
3. **Manual Review**: Dashboard review by maintainers

### Local Quality Checks

```bash
# Validate JSON
python -m json.tool dashboard-smart-swimming-pool.json > /dev/null

# Or use jq
jq empty dashboard-smart-swimming-pool.json
```text

---

## Thank You!

Your contributions help make this dashboard better for everyone. We appreciate your
time and effort in improving the Smart Swimming Pool Grafana Dashboard!

---

## 📚 Additional Resources

- [Grafana Documentation](https://grafana.com/docs/)
- [Smart Swimming Pool Website](https://smart-swimmingpool.com)
- [GitHub Discussions](https://github.com/smart-swimmingpool/smart-swimmingpool.github.io/discussions)
- [Pool Controller MQTT Topics](https://github.com/smart-swimmingpool/pool-controller/blob/main/docs/mqtt-configuration.md)
