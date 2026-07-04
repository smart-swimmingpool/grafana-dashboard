# Grafana Dashboard | \ud83c\udfca Smart Swimming Pool

[![Smart Swimmingpool](https://img.shields.io/badge/%F0%9F%8F%8A%20-Smart%20Swimmingpool-blue.svg)](https://github.com/smart-swimmingpool)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## \u2728 Overview

This repository contains a **Grafana dashboard** for visualizing Smart Swimming Pool data. The dashboard provides comprehensive monitoring of your pool's vital statistics including temperatures, pump status, solar heating, and historical trends.

**Perfect for:** Users who want to visualize pool data over time, track energy usage, and analyze pool performance.

---

## \u2728 Features

### \ud83c\udf21\ufe0f Temperature Monitoring
- **Pool water temperature** \u2014 Current and historical
- **Solar collector temperature** \u2014 Current and historical
- **Temperature difference** \u2014 Pool vs Solar for efficiency analysis
- **Temperature history** \u2014 Time series graphs with customizable time ranges

### \u26a1 Pump & System Status
- **Pump status** \u2014 Real-time on/off state for pool and solar pumps
- **Operation mode** \u2014 Current mode (Auto, Manual, Boost, Timer)
- **Uptime** \u2014 Pool controller uptime monitoring
- **Pump runtime** \u2014 Daily runtime tracking

### \u2600\ufe0f Solar Heating Analysis
- **Solar heating status** \u2014 On/off state
- **Solar runtime** \u2014 Daily solar heating runtime
- **Efficiency calculation** \u2014 Based on temperature differential
- **Energy savings** \u2014 Estimated savings from solar heating

### \ud83d\udcc8 Data Visualization
- **Time series graphs** \u2014 Historical data with zoom and pan
- **Gauges** \u2014 Current values at a glance
- **Status panels** \u2014 Binary states with color coding
- **Statistics** \u2014 Aggregated data (min, max, avg)

---

## \ud83d\ude80 Quick Start

### \u26a1 Prerequisites

| Component | Version | Notes |
|-----------|---------|-------|
| Grafana | v7.0+ | v8.0+ recommended for best experience |
| MQTT Data Source Plugin | Latest | [marcusolsson-grafana-mqtt](https://grafana.com/grafana/plugins/marcusolsson-grafana-mqtt/) |
| MQTT Broker | Any | Mosquitto, EMQX, etc. |
| Pool Controller | v3.0+ | Running and publishing MQTT data |

### \u26a1 Installation

#### Option A: Direct Import (Recommended)

1. **Download dashboard JSON:**
   ```bash
   # Clone this repository
   git clone https://github.com/smart-swimmingpool/grafana-dashboard.git
   cd grafana-dashboard
   
   # Or download directly
   wget https://raw.githubusercontent.com/smart-swimmingpool/grafana-dashboard/master/dashboard-smart-swimming-pool.json
   ```

2. **Import into Grafana:**
   - Open Grafana in your browser
   - Go to **Dashboards \u2192 Import**
   - Upload the `dashboard-smart-swimming-pool.json` file
   - Select your **MQTT data source**
   - Click **Import**

#### Option B: Grafana Catalog

1. Open Grafana
2. Go to **Dashboards \u2192 Import**
3. Enter dashboard ID: **`13374`** (if published to Grafana.com)
4. Select your MQTT data source
5. Click **Load** then **Import**

---

## \ud83d\udcc1 Dashboard Configuration

### \u26a1 MQTT Data Source Setup

1. **Install MQTT plugin:**
   ```bash
   # For Grafana CLI
   grafana-cli plugins install marcusolsson-grafana-mqtt
   
   # Or via Grafana UI: Configuration \u2192 Plugins \u2192 Install
   ```

2. **Configure MQTT data source:**
   - Go to **Configuration \u2192 Data Sources \u2192 Add data source**
   - Select **MQTT**
   - Configure settings:
     - **Name:** `Smart Swimming Pool MQTT`
     - **URL:** `mqtt://your-broker-ip:1883`
     - **Client ID:** `grafana-smart-pool`
     - **Username/Password:** (if your broker requires authentication)
     - **Topic:** `smart-swimmingpool/#`
     - **QoS:** `0` or `1`
     - **Retain:** `true` (if your broker supports retained messages)

3. **Test connection:**
   - Click **Save & Test**
   - Verify connection is successful

### \u26a1 Dashboard Variables (Optional)

The dashboard supports **template variables** for easy customization:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `pool_controller_id` | Pool Controller identifier | `pool-controller` |
| `time_range` | Default time range | `24h` |

**To customize:**
1. Click **Dashboard Settings** (gear icon)
2. Go to **Variables** tab
3. Edit variable definitions as needed

---

## \ud83d\udcc1 Dashboard Structure

### \ud83c\udf21 Temperature Section

**Panels:**
1. **Pool Temperature Gauge** \u2014 Current pool water temperature
2. **Solar Temperature Gauge** \u2014 Current solar collector temperature
3. **Temperature History Graph** \u2014 Both temperatures over time
4. **Temperature Difference** \u2014 Solar - Pool (\u00b0C)

**MQTT Topics:**
```text
homeassistant/sensor/pool-controller/pool-temp/state
homeassistant/sensor/pool-controller/solar-temp/state
```

### \u26a1 Pump Status Section

**Panels:**
1. **Pool Pump Status** \u2014 On/Off with color coding
2. **Solar Pump Status** \u2014 On/Off with color coding
3. **Pump Runtime Today** \u2014 Total runtime in hours:minutes
4. **Pump Runtime History** \u2014 Daily runtime over time

**MQTT Topics:**
```text
homeassistant/switch/pool-controller/pool-pump/state
homeassistant/switch/pool-controller/solar-pump/state
smart-swimmingpool/pool-controller/pump/pool/runtime/today
smart-swimmingpool/pool-controller/pump/solar/runtime/today
```

### \u2600 Solar Heating Section

**Panels:**
1. **Solar Heating Status** \u2014 On/Off
2. **Solar Runtime Today** \u2014 Total solar heating runtime
3. **Solar Heating Efficiency** \u2014 Calculated from temperature differential
4. **Energy Savings Estimate** \u2014 Based on runtime and efficiency

**MQTT Topics:**
```text
homeassistant/switch/pool-controller/solar-pump/state
smart-swimmingpool/pool-controller/solar/runtime/today
```

### \u26a1 System Section

**Panels:**
1. **Operation Mode** \u2014 Current mode (Auto, Manual, Boost, Timer)
2. **Uptime** \u2014 Controller uptime
3. **System Health** \u2014 Memory usage, boot count
4. **Last Update** \u2014 Timestamp of last MQTT message

**MQTT Topics:**
```text
homeassistant/select/pool-controller/mode/state
smart-swimmingpool/pool-controller/uptime
smart-swimmingpool/pool-controller/system/boot-count
smart-swimmingpool/pool-controller/system/memory-free
```

---

## \ud83d\udcc1 Complete MQTT Topic Reference

### State Topics (Home Assistant Discovery)

```text
# Temperature Sensors
homeassistant/sensor/pool-controller/pool-temp/state
homeassistant/sensor/pool-controller/pool-temp/unit_of_measurement
homeassistant/sensor/pool-controller/pool-temp/device_class

homeassistant/sensor/pool-controller/solar-temp/state
homeassistant/sensor/pool-controller/solar-temp/unit_of_measurement
homeassistant/sensor/pool-controller/solar-temp/device_class

# Switches (Pumps)
homeassistant/switch/pool-controller/pool-pump/state
homeassistant/switch/pool-controller/pool-pump/command
homeassistant/switch/pool-controller/solar-pump/state
homeassistant/switch/pool-controller/solar-pump/command

# Select (Operation Mode)
homeassistant/select/pool-controller/mode/state
homeassistant/select/pool-controller/mode/command

# Number (Temperature Thresholds)
homeassistant/number/pool-controller/pool-target-temp/state
homeassistant/number/pool-controller/pool-target-temp/command
homeassistant/number/pool-controller/solar-min-delta/state
homeassistant/number/pool-controller/solar-min-delta/command
```

### Legacy Topics (Pre-v3.3.0)

```text
# State
smart-swimmingpool/pool-controller/state

# Temperatures
smart-swimmingpool/pool-controller/temperature/pool
smart-swimmingpool/pool-controller/temperature/solar

# Pump States
smart-swimmingpool/pool-controller/pump/pool/state
smart-swimmingpool/pool-controller/pump/solar/state

# Pump Runtimes
smart-swimmingpool/pool-controller/pump/pool/runtime/today
smart-swimmingpool/pool-controller/pump/solar/runtime/today

# Solar State
smart-swimmingpool/pool-controller/solar/state
smart-swimmingpool/pool-controller/solar/runtime/today

# Mode
smart-swimmingpool/pool-controller/mode

# Uptime
smart-swimmingpool/pool-controller/uptime

# System Health
smart-swimmingpool/pool-controller/system/boot-count
smart-swimmingpool/pool-controller/system/memory-free
smart-swimmingpool/pool-controller/system/heap-fragmentation
```

**Complete Reference:** [Pool Controller MQTT Configuration](https://github.com/smart-swimmingpool/pool-controller/blob/main/docs/mqtt-configuration.md)

---

## \ud83d\udee0\ufe0f Customization

### \u26a1 Adding New Panels

1. **Edit dashboard in Grafana:**
   - Click **Edit** (pencil icon) on the dashboard
   - Click **Add Panel**

2. **Configure panel:**
   - **Title:** Descriptive name for your panel
   - **Data Source:** Select your MQTT data source
   - **Query:** Enter MQTT topic (e.g., `smart-swimmingpool/pool-controller/temperature/pool`)
   - **Visualization:** Choose appropriate type (Graph, Gauge, Stat, etc.)

3. **Format data:**
   - **Unit:** \u00b0C, \u00b0F, hours, etc.
   - **Decimals:** Number of decimal places
   - **Thresholds:** Color coding for different value ranges

4. **Save panel:**
   - Click **Apply** to save the panel
   - Click **Save Dashboard** (disk icon) to save changes

5. **Export updated dashboard:**
   - Click **Save Dashboard \u2192 Export \u2192 Save to file**
   - Update the `dashboard-smart-swimming-pool.json` file
   - Submit a pull request

### \u26a1 Modifying Existing Panels

1. Click **Edit** on the panel you want to modify
2. Adjust settings as needed:
   - Change query topics
   - Modify visualization type
   - Update color schemes
   - Adjust time ranges
3. Click **Apply** to save changes
4. **Export and update** the JSON file
5. **Document changes** in CHANGELOG.md

### \u26a1 Creating Multiple Dashboards

For advanced users, you can create **multiple dashboards** for different purposes:

**Suggested dashboard organization:**

| Dashboard | Purpose | Key Panels |
|-----------|---------|------------|
| **Overview** | Quick status at a glance | Current temperatures, pump status, mode |
| **History** | Long-term trends | Temperature history, runtime statistics |
| **Efficiency** | Solar heating analysis | Efficiency calculations, energy savings |
| **System** | Controller health | Memory usage, uptime, boot count |

---

## \u26a1 Example Queries

### Temperature Query

```sql
-- MQTT Query for Pool Temperature
SELECT
  value AS temperature,
  time AS timestamp
FROM mqtt
WHERE
  topic = 'homeassistant/sensor/pool-controller/pool-temp/state'
  AND $timeFilter
ORDER BY time ASC
```

### Pump Runtime Query

```sql
-- MQTT Query for Daily Pool Pump Runtime
SELECT
  value AS runtime_minutes,
  time AS timestamp
FROM mqtt
WHERE
  topic = 'smart-swimmingpool/pool-controller/pump/pool/runtime/today'
  AND $timeFilter
ORDER BY time ASC
```

### Efficiency Calculation (Transform)

Use Grafana's **Transform** feature to calculate efficiency:

1. Add both temperature queries
2. Click **Transform** tab
3. Add **Add field from calculation**
4. Select **Binary operation: Subtraction**
5. Field A: Solar Temperature
6. Field B: Pool Temperature
7. Result: Temperature Difference (\u00b0C)

---

## \u26a1 Tips & Best Practices

### Dashboard Design

1. **Keep it simple** \u2014 Start with essential panels, add more as needed
2. **Use consistent colors** \u2014 Green for good/on, Red for bad/off, etc.
3. **Group related panels** \u2014 Temperature, Pumps, Solar, System
4. **Use appropriate time ranges** \u2014 24h for daily, 7d for weekly, 30d for monthly
5. **Add descriptions** \u2014 Explain what each panel shows

### Performance

1. **Limit data points** \u2014 Use `$__interval` for appropriate resolution
2. **Use retained messages** \u2014 Reduces MQTT traffic
3. **Avoid too many panels** \u2014 Each panel adds query load
4. **Use dashboard links** \u2014 Link between related dashboards

### MQTT Broker

1. **Enable persistence** \u2014 Store retained messages across broker restarts
2. **Set appropriate QoS** \u2014 QoS 1 for important data, QoS 0 for high-frequency
3. **Monitor broker health** \u2014 Check memory usage, connection count
4. **Secure your broker** \u2014 Use authentication and TLS for production

---

## \u26a1 Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Dashboard shows "No data" | MQTT data source not configured | Check data source settings |
| Panels show "No data" | Wrong MQTT topic | Verify topic names match Pool Controller |
| Dashboard not updating | MQTT connection lost | Check broker status, network connectivity |
| Slow dashboard loading | Too many panels or data points | Reduce panel count, limit time range |
| Authentication errors | Wrong MQTT credentials | Verify username/password in data source |
| Connection refused | Broker not running or wrong port | Check broker is running, verify port number |

### Debugging Steps

1. **Check MQTT data source:**
   - Go to **Configuration \u2192 Data Sources**
   - Click on your MQTT data source
   - Click **Test Connection**

2. **Verify MQTT topics:**
   - Use MQTT client (e.g., MQTT Explorer) to verify data is being published
   - Check topic names match those in dashboard queries

3. **Check Grafana logs:**
   - View browser console (F12) for JavaScript errors
   - Check Grafana server logs for backend errors

4. **Test with simple query:**
   - Create a test panel with a simple topic
   - Verify data appears before adding complex queries

---

## \u26a1 Advanced Configuration

### Alerts

Set up alerts for abnormal conditions:

1. **High pool temperature:**
   - Trigger when pool temp > 35\u00b0C
   - Notification: "Pool temperature is too high!"

2. **Pump runtime too long:**
   - Trigger when daily runtime > 12h
   - Notification: "Pool pump has been running too long!"

3. **Low temperature difference:**
   - Trigger when solar - pool < 5\u00b0C
   - Notification: "Solar heating may not be effective"

### Annotations

Add annotations for important events:

1. **Manual mode changes** \u2014 Annotate when mode changes to Manual
2. **Boost mode activation** \u2014 Annotate when Boost mode is activated
3. **Maintenance events** \u2014 Annotate pool cleaning, chemical additions

### Dashboard Links

Create links between dashboards:

1. **Overview \u2192 History** \u2014 Link to detailed history dashboard
2. **Overview \u2192 Efficiency** \u2014 Link to efficiency analysis
3. **History \u2192 Specific Day** \u2014 Link to day-specific dashboard

---

## \ud83e\udd1d Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch** (e.g., `feat/add-energy-panel`)
3. **Make your changes** in Grafana
4. **Export the dashboard JSON**
5. **Update the JSON file** in this repository
6. **Test your changes** thoroughly
7. **Update documentation** if applicable
8. **Submit a pull request**

### Quality Checks

Before submitting:
- \u2705 Validate JSON: `python -m json.tool dashboard-smart-swimming-pool.json > /dev/null`
- \u2705 Or use jq: `jq empty dashboard-smart-swimming-pool.json`
- \u2705 Test import in Grafana
- \u2705 Verify all panels show data
- \u2705 Check for typos and formatting issues

---

## \ud83d\udcdc License

[MIT License](LICENSE) \u2013 Free to use, modify, and share.

---

## \ud83c\udf10 Community & Support

- **Discussions:** [GitHub Discussions](https://github.com/smart-swimmingpool/smart-swimmingpool.github.io/discussions)
- **Website:** [smart-swimmingpool.com](https://smart-swimmingpool.com)
- **Grafana Community:** [community.grafana.com](https://community.grafana.com/)

**Need Help?**
1. Check this README for common issues
2. Search [GitHub Discussions](https://github.com/smart-swimmingpool/smart-swimmingpool.github.io/discussions)
3. Open a [new issue](https://github.com/smart-swimmingpool/grafana-dashboard/issues/new)

---

## \ud83d\udce2 Related Projects

| Project | Description |
|---------|-------------|
| [Pool Controller](https://github.com/smart-swimmingpool/pool-controller) | Main control unit with MQTT integration |
| [Pool Monitor](https://github.com/smart-swimmingpool/monitor) | Solar-powered wireless temperature display |
| [openHAB Config](https://github.com/smart-swimmingpool/openhab-config) | openHAB configuration files |
| [Water Quality Monitor](https://github.com/smart-swimmingpool/water-quality-monitor) | Water quality monitoring (pH, chlorine) |
| [Website](https://github.com/smart-swimmingpool/website) | Project documentation website |

---

## \ud83d\udcbb Additional Resources

### Grafana
- [Grafana Documentation](https://grafana.com/docs/) \u2014 Official Grafana docs
- [Grafana Tutorials](https://grafana.com/tutorials/) \u2014 Learning resources
- [Grafana MQTT Plugin](https://github.com/marcusolsson/grafana-mqtt) \u2014 Plugin source code

### MQTT
- [MQTT Protocol](https://mqtt.org/) \u2014 MQTT specification
- [MQTT Explorer](http://mqtt-explorer.com/) \u2014 MQTT client for testing
- [Mosquitto](https://mosquitto.org/) \u2014 Popular MQTT broker

### Smart Home
- [Home Assistant](https://www.home-assistant.io/) \u2014 Open source home automation
- [Home Assistant MQTT Discovery](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery) \u2014 Auto-discovery documentation

---

<p align="center">
  Made with \u2764\ufe0f by the Smart Swimming Pool community
</p>
