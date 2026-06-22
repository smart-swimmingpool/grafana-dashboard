# Grafana Dashboard for Smart Swimming Pool

[![Smart Swimmingpool](https://img.shields.io/badge/%F0%9F%8F%8A%20-Smart%20Swimmingpool-blue.svg)](https://github.com/smart-swimmingpool)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Discussions: <https://github.com/smart-swimmingpool/smart-swimmingpool.github.io/discussions>

## ✨ Overview

This repository contains a **Grafana dashboard** for visualizing Smart Swimming Pool data. The dashboard provides comprehensive monitoring of your pool's vital statistics including temperatures, pump status, solar heating, and more.

## Features

- 🌡️ **Temperature Monitoring**: Pool water and solar storage temperatures
- ⚡ **Pump Status**: Real-time pump state visualization
- ☀️ **Solar Heating**: Solar heating status and efficiency
- **Time Series**: Historical data visualization
- **Customizable**: Easily adaptable to your specific setup
- 🔄 **MQTT Integration**: Works with Pool Controller MQTT topics

## Quick Start

### Prerequisites

- [Grafana](https://grafana.com/) (v7.0 or later recommended)
- [MQTT Data Source Plugin](https://grafana.com/grafana/plugins/marcusolsson-grafana-mqtt/) installed in Grafana
- MQTT broker with Pool Controller data
- Smart Swimming Pool Pool Controller running

### Installation

1. **Download the dashboard JSON:**
   ```bash
   # Clone this repository
   git clone https://github.com/smart-swimmingpool/grafana-dashboard.git
   cd grafana-dashboard
   
   # Or download directly
   wget https://raw.githubusercontent.com/smart-swimmingpool/grafana-dashboard/master/dashboard-smart-swimming-pool.json
   ```

2. **Import into Grafana:**
   - Open Grafana in your browser
   - Go to **Dashboards > Import**
   - Upload the `dashboard-smart-swimming-pool.json` file
   - Select your MQTT data source
   - Click **Import**

3. **Configure MQTT Data Source:**
   - Go to **Configuration > Data Sources**
   - Add **MQTT** data source
   - Configure with your MQTT broker settings
   - Set topic filter to: `smart-swimmingpool/#`

## 📁 Dashboard Structure

The dashboard includes the following panels:

### Temperature Section
- **Pool Temperature**: Current pool water temperature
- **Solar Temperature**: Current solar storage temperature
- **Temperature History**: Time series graph of both temperatures
- **Temperature Difference**: Difference between pool and solar

### Status Section
- **Pump Status**: Current pump state (On/Off)
- **Solar Heating Status**: Current solar heating state (On/Off)
- **Operation Mode**: Current operation mode (Auto/Manual/Boost/Timer)

### Efficiency Section
- **Solar Heating Efficiency**: Efficiency calculation based on temperature differential
- **Energy Savings**: Estimated energy savings from solar heating

### Statistics Section
- **Uptime**: Pool controller uptime
- **Pump Runtime**: Total pump runtime today
- **Solar Runtime**: Total solar heating runtime today

## MQTT Topics Reference

The dashboard expects the following MQTT topics from the Pool Controller:

```text
# State Topics
smart-swimmingpool/pool-controller/state

# Temperature Topics
smart-swimmingpool/pool-controller/temperature/pool
smart-swimmingpool/pool-controller/temperature/solar

# Pump Topics
smart-swimmingpool/pool-controller/pump/state
smart-swimmingpool/pool-controller/pump/runtime/today

# Solar Topics
smart-swimmingpool/pool-controller/solar/state
smart-swimmingpool/pool-controller/solar/runtime/today

# Mode Topic
smart-swimmingpool/pool-controller/mode

# Uptime Topic
smart-swimmingpool/pool-controller/uptime
```text

For complete MQTT topic reference, see:
[Pool Controller MQTT Configuration](https://github.com/smart-swimmingpool/pool-controller/blob/main/docs/mqtt-configuration.md)

## 🛠️ Customization

### Adding New Panels

1. Edit the dashboard in Grafana
2. Add your new panel with appropriate queries
3. Export the dashboard (Save Dashboard > Export > Save to file)
4. Update the `dashboard-smart-swimming-pool.json` file
5. Submit a pull request

### Modifying Existing Panels

- Edit panels directly in Grafana
- Test your changes
- Export and update the JSON file
- Document your changes in the CHANGELOG

## Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) before submitting pull requests.

### Development Workflow

```bash
# Clone the repository
git clone https://github.com/smart-swimmingpool/grafana-dashboard.git
cd grafana-dashboard

# Validate JSON before committing
python -m json.tool dashboard-smart-swimming-pool.json > /dev/null

# Or use jq
jq empty dashboard-smart-swimming-pool.json
```text

## 🛡️ Quality Checks

This project enforces quality standards:

- ✅ **JSON Validation**: Dashboard JSON must be valid
- ✅ **Super-Linter**: Code quality and style checking
- ✅ **Manual Review**: Dashboard review by maintainers

## 📜 License

[MIT License](LICENSE) – Free to use, modify, and share.

---

## Community

- **Discussions:** [GitHub Discussions](https://github.com/smart-swimmingpool/smart-swimmingpool.github.io/discussions)
- **Website:** [smart-swimmingpool.com](https://smart-swimmingpool.com)
- **Grafana Community:** [community.grafana.com](https://community.grafana.com/)

## Credits

- All [contributors](https://github.com/smart-swimmingpool/grafana-dashboard/graphs/contributors) for their valuable input!
- Inspired by the [Pool Controller](https://github.com/smart-swimmingpool/pool-controller) project

---

<p align="center">
  Made with ❤️ by the Smart Swimming Pool community
</p>
