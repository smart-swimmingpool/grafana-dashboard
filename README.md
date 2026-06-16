# Grafana Dashboard for Smart Swimming Pool

[![Smart Swimmingpool](https://img.shields.io/badge/%F0%9F%8F%8A%20-Smart%20Swimmingpool-blue.svg)](https://github.com/smart-swimmingpool)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Discussions: [https://github.com/smart-swimmingpool/smart-swimmingpool.github.io/discussions](https://github.com/smart-swimmingpool/smart-swimmingpool.github.io/discussions)

JSON exported dashboard of Smart Swimming Pool for **Grafana** visualization.

---

## 📌 Overview

This repository provides a **pre-configured Grafana dashboard** for visualizing **Smart Swimming Pool** data. 
Use this dashboard to **track temperature trends, monitor system status, and analyze historical data** from your pool controller.

---

## ✅ Prerequisites

Before you begin, ensure you have the following:

| **Component**       | **Purpose**                          | **Installation Guide** |
|--------------------|--------------------------------------|------------------------|
| **Grafana**         | Visualization platform               | [Official Guide](https://grafana.com/docs/grafana/latest/setup-grafana/installation/) |
| **InfluxDB**        | Time-series database                 | [Official Guide](https://docs.influxdata.com/influxdb/latest/install/) |
| **Telegraf**        | Data collection agent                | [Official Guide](https://docs.influxdata.com/telegraf/latest/introduction/install/) |
| **MQTT Broker**     | Message broker (e.g., Mosquitto)     | [Mosquitto Setup](#mqtt-broker-setup) |
| **Pool Controller** | Smart Swimming Pool device           | [Pool Controller Docs](https://github.com/smart-swimmingpool/pool-controller) |

---

## 🚀 Quick Start

### 1️⃣ **Set Up InfluxDB**

InfluxDB is a **time-series database** that stores your pool data for visualization.

#### **Install InfluxDB on Raspberry Pi**
```bash
# Add InfluxDB repository
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
sudo echo "deb https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

# Install InfluxDB
sudo apt-get update
sudo apt-get install influxdb

# Start InfluxDB
sudo systemctl start influxdb
sudo systemctl enable influxdb
```

#### **Create Database**
```bash
influx
```
In the InfluxDB CLI:
```sql
CREATE DATABASE pool_data
quit
```

---

### 2️⃣ **Set Up Telegraf**

Telegraf collects MQTT data and writes it to InfluxDB.

#### **Install Telegraf**
```bash
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
sudo echo "deb https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt-get update
sudo apt-get install telegraf
sudo systemctl start telegraf
sudo systemctl enable telegraf
```

#### **Configure Telegraf**
Edit `/etc/telegraf/telegraf.conf`:
```ini
[[inputs.mqtt_consumer]]
  servers = ["tcp://<broker-ip>:1883"]
  topics = ["homeassistant/sensor/pool-controller/#"]
  data_format = "value"
  data_type = "float"

[[outputs.influxdb]]
  urls = ["http://localhost:8086"]
  database = "pool_data"
```
Restart Telegraf:
```bash
sudo systemctl restart telegraf
```

---

### 3️⃣ **Set Up Grafana**

#### **Install Grafana**
```bash
sudo apt-get install -y apt-transport-https software-properties-common wget
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt-get update
sudo apt-get install grafana
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

#### **Access Grafana**
- Open `http://<raspberry-pi-ip>:3000` (default: `admin/admin`)

#### **Add InfluxDB Data Source**
1. Go to **Configuration > Data Sources > Add data source > InfluxDB**
2. Set:
   - **URL**: `http://localhost:8086`
   - **Database**: `pool_data`
3. Click **Save & Test**

#### **Import Dashboard**
1. Download [dashboard.json](dashboard.json)
2. Go to **Dashboards > Import**
3. Upload the JSON file
4. Select the InfluxDB data source

---

## 📊 Dashboard Features

| **Panel** | **Description** | **Data** |
|-----------|-----------------|----------|
| Pool Temperature | Current pool water temperature | `pool_temp` |
| Solar Temperature | Current solar collector temperature | `solar_temp` |
| Temperature Trends | Historical data (last 24h) | All temp sensors |
| Pump Status | Current pump states | `pool_pump`, `solar_pump` |
| System Health | Heap, uptime, RSSI | `heap`, `uptime`, `rssi` |

---

## 🔧 MQTT Broker Setup

### **Install Mosquitto**
```bash
sudo apt-get install mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

### **Secure Mosquitto**
```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd username
sudo nano /etc/mosquitto/mosquitto.conf
```
Add:
```ini
allow_anonymous false
password_file /etc/mosquitto/passwd
```
Restart:
```bash
sudo systemctl restart mosquitto
```

---

## 🛠️ Customization

### **Modify Panels**
1. Open dashboard > Edit panel
2. Adjust queries/visualizations
3. Click **Apply**

### **Add New Panels**
1. Click **Add panel**
2. Select InfluxDB data source
3. Write query (e.g., `SELECT "value" FROM "pool_temp" WHERE $timeFilter GROUP BY time($__interval)`)
4. Choose visualization type

---

## 🔍 Troubleshooting

### ❌ **Grafana can't connect to InfluxDB**
- Check InfluxDB: `sudo systemctl status influxdb`
- Test CLI: `influx -execute "SHOW DATABASES"`
- Check Grafana logs: `sudo journalctl -u grafana-server -f`

### ❌ **Telegraf isn't collecting data**
- Check Telegraf: `sudo systemctl status telegraf`
- View logs: `sudo journalctl -u telegraf -f`
- Test MQTT: `mosquitto_sub -h <broker-ip> -t "homeassistant/sensor/pool-controller/#" -v`

---

## 📚 Resources
- [Pool Controller Docs](https://github.com/smart-swimmingpool/pool-controller)
- [MQTT Configuration Guide](https://github.com/smart-swimmingpool/pool-controller/blob/main/docs/mqtt-configuration.md)
- [InfluxDB Docs](https://docs.influxdata.com/influxdb/latest/)
- [Grafana Docs](https://grafana.com/docs/)

---

## 📜 License
MIT License – see [LICENSE](../LICENSE) for details.