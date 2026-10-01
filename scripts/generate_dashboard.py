#!/usr/bin/env python3
"""Generate the Grafana dashboard for Pool Controller v5 (Home Assistant + InfluxDB).

Home Assistant's InfluxDB integration stores every entity with the tag
"entity_id". Entities with a unit are written to a measurement named after
the unit (e.g. "°C", "s", "dBm"); entities without a unit (switches, selects)
are written to a measurement named after the full entity id
(e.g. "switch.pool_controller_pool_pump"). Numeric states are stored in the
field "value" (on/off as 1/0), text states in the field "state".

The entity ids are the defaults Home Assistant derives from the Pool Controller
MQTT discovery (device "Pool Controller"). They are exposed as dashboard
variables so renamed entities can be adjusted without editing panels.

Run: python3 scripts/generate_dashboard.py > dashboard-smart-swimming-pool.json
"""

import json

DS = {"type": "influxdb", "uid": "${DS_INFLUXDB}"}

_next_id = 0


def _id():
    global _next_id
    _next_id += 1
    return _next_id


def target(query, ref="A", alias=None):
    t = {"datasource": DS, "query": query, "rawQuery": True, "refId": ref, "resultFormat": "time_series"}
    if alias:
        t["alias"] = alias
    return t


def unit_query(unit, var, agg="mean", fill="null"):
    return (f'SELECT {agg}("value") FROM "{unit}" WHERE "entity_id" = \'${var}\' '
            f'AND $timeFilter GROUP BY time($__interval) fill({fill})')


def entity_query(domain, var, field="value", agg="last", fill="previous"):
    return (f'SELECT {agg}("{field}") FROM "{domain}.${var}" '
            f'WHERE $timeFilter GROUP BY time($__interval) fill({fill})')


def last_query(unit, var):
    return f'SELECT last("value") FROM "{unit}" WHERE "entity_id" = \'${var}\' AND $timeFilter'


def row(title, y, collapsed=False, panels=None):
    return {"type": "row", "id": _id(), "title": title, "collapsed": collapsed,
            "gridPos": {"h": 1, "w": 24, "x": 0, "y": y}, "panels": panels or []}


def timeseries(title, targets, pos, unit, overrides=None, description=None):
    return {
        "type": "timeseries", "id": _id(), "title": title, "datasource": DS,
        "description": description or "", "gridPos": pos, "targets": targets,
        "fieldConfig": {
            "defaults": {"unit": unit, "decimals": 1, "color": {"mode": "palette-classic"},
                         "custom": {"lineWidth": 2, "fillOpacity": 10, "spanNulls": 3600000,
                                    "showPoints": "never"}},
            "overrides": overrides or []},
        "options": {"legend": {"displayMode": "list", "placement": "bottom", "calcs": ["lastNotNull", "min", "max"]},
                    "tooltip": {"mode": "multi", "sort": "none"}},
    }


def color_override(name, color):
    return {"matcher": {"id": "byName", "options": name},
            "properties": [{"id": "color", "value": {"mode": "fixed", "fixedColor": color}}]}


def gauge(title, query, pos, unit, mn, mx, steps, decimals=1):
    return {
        "type": "gauge", "id": _id(), "title": title, "datasource": DS, "gridPos": pos,
        "targets": [target(query)],
        "fieldConfig": {"defaults": {"unit": unit, "min": mn, "max": mx, "decimals": decimals,
                                     "thresholds": {"mode": "absolute", "steps": steps}},
                        "overrides": []},
        "options": {"reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False},
                    "showThresholdLabels": False, "showThresholdMarkers": True},
    }


def stat(title, query, pos, unit, steps=None, decimals=None, mappings=None, description=None, graph="area"):
    defaults = {"unit": unit, "thresholds": {"mode": "absolute",
                                             "steps": steps or [{"color": "blue", "value": None}]}}
    if decimals is not None:
        defaults["decimals"] = decimals
    if mappings:
        defaults["mappings"] = mappings
    return {
        "type": "stat", "id": _id(), "title": title, "datasource": DS, "gridPos": pos,
        "description": description or "", "targets": [target(query)],
        "fieldConfig": {"defaults": defaults, "overrides": []},
        "options": {"reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False},
                    "colorMode": "background", "graphMode": graph, "textMode": "value", "justifyMode": "center"},
    }


def state_timeline(title, targets, pos, mappings, description=None, steps=None):
    return {
        "type": "state-timeline", "id": _id(), "title": title, "datasource": DS, "gridPos": pos,
        "description": description or "", "targets": targets,
        "fieldConfig": {"defaults": {"mappings": mappings, "color": {"mode": "thresholds"},
                                     "thresholds": {"mode": "absolute",
                                                    "steps": steps or [{"color": "text", "value": None}]},
                                     "custom": {"fillOpacity": 80, "lineWidth": 0}},
                        "overrides": []},
        "options": {"showValue": "auto", "mergeValues": True, "rowHeight": 0.8, "alignValue": "center",
                    "legend": {"showLegend": False}, "tooltip": {"mode": "single", "sort": "none"}},
    }


def textbox_var(name, label, default):
    return {"type": "textbox", "name": name, "label": label, "hide": 2,
            "query": default, "current": {"text": default, "value": default},
            "options": [{"selected": True, "text": default, "value": default}]}


# Range mappings: InfluxQL returns floats (0.0 / 1.0), aggregated values may lie in between.
ON_OFF = [
    {"type": "range", "options": {"from": -0.5, "to": 0.5, "result": {"text": "OFF", "color": "#7f7f7f", "index": 0}}},
    {"type": "range", "options": {"from": 0.5, "to": 1.5, "result": {"text": "ON", "color": "green", "index": 1}}},
]
# Text mappings for the "state" field ("on"/"off") used by the state timeline.
ON_OFF_TEXT = [{"type": "value", "options": {
    "off": {"text": "OFF", "color": "#7f7f7f", "index": 0},
    "on": {"text": "ON", "color": "green", "index": 1}}}]
ON_OFF_STEPS = [{"color": "#7f7f7f", "value": None}, {"color": "green", "value": 0.5}]

MODES = [{"type": "value", "options": {
    "auto": {"text": "Auto", "color": "green", "index": 0},
    "manu": {"text": "Manual", "color": "yellow", "index": 1},
    "boost": {"text": "Boost", "color": "orange", "index": 2},
    "timer": {"text": "Timer", "color": "blue", "index": 3}}}]

TEMP_STEPS = [{"color": "blue", "value": None}, {"color": "green", "value": 20},
              {"color": "orange", "value": 28}, {"color": "red", "value": 32}]
SOLAR_STEPS = [{"color": "blue", "value": None}, {"color": "green", "value": 25},
               {"color": "orange", "value": 45}, {"color": "red", "value": 70}]

panels = [
    row("Temperatures", 0),
    gauge("Pool", last_query("°C", "pool_temp"), {"h": 8, "w": 4, "x": 0, "y": 1}, "celsius", 0, 40, TEMP_STEPS),
    gauge("Solar", last_query("°C", "solar_temp"), {"h": 8, "w": 4, "x": 4, "y": 1}, "celsius", 0, 80, SOLAR_STEPS),
    timeseries("Temperature history", [
        target(unit_query("°C", "pool_temp"), "A", "Pool"),
        target(unit_query("°C", "solar_temp"), "B", "Solar"),
        target(unit_query("°C", "controller_temp"), "C", "Controller"),
    ], {"h": 8, "w": 16, "x": 8, "y": 1}, "celsius",
        [color_override("Pool", "blue"), color_override("Solar", "orange"),
         {"matcher": {"id": "byName", "options": "Controller"},
          "properties": [{"id": "color", "value": {"mode": "fixed", "fixedColor": "purple"}},
                         {"id": "custom.lineStyle", "value": {"fill": "dash", "dash": [10, 10]}},
                         {"id": "custom.fillOpacity", "value": 0}]}]),

    row("Pumps & Operation", 9),
    state_timeline("Pumps", [
        target(entity_query("switch", "pool_pump", field="state"), "A", "Pool Pump"),
        target(entity_query("switch", "solar_pump", field="state"), "B", "Solar Pump"),
    ], {"h": 6, "w": 16, "x": 0, "y": 10}, ON_OFF_TEXT,
        "Switching times of the filter (pool) pump and the solar pump."),
    stat("Pool Pump", entity_query("switch", "pool_pump", fill="none"),
         {"h": 3, "w": 4, "x": 16, "y": 10}, "none", ON_OFF_STEPS, mappings=ON_OFF, graph="none"),
    stat("Solar Pump", entity_query("switch", "solar_pump", fill="none"),
         {"h": 3, "w": 4, "x": 20, "y": 10}, "none", ON_OFF_STEPS, mappings=ON_OFF, graph="none"),
    stat("Effective Runtime", last_query("s", "effective_runtime"),
         {"h": 3, "w": 4, "x": 16, "y": 13}, "dthms", graph="none",
         description="Filter runtime for today including the temperature-based circulation extension."),
    stat("Circulation Extension", last_query("s", "circulation_extension"),
         {"h": 3, "w": 4, "x": 20, "y": 13}, "dthms", graph="none",
         description="Additional runtime added by the temperature-based circulation."),
    state_timeline("Operation Mode", [
        target(entity_query("select", "operation_mode", field="state"), "A", "Mode"),
    ], {"h": 4, "w": 24, "x": 0, "y": 16}, MODES, "Operation mode: auto, manual, boost or timer."),

    row("Diagnostics", 20, collapsed=True, panels=[
        stat("WiFi Signal", last_query("dBm", "rssi"), {"h": 4, "w": 6, "x": 0, "y": 21}, "dBm",
             [{"color": "red", "value": None}, {"color": "orange", "value": -80},
              {"color": "green", "value": -67}], 0),
        stat("Uptime", last_query("s", "uptime"), {"h": 4, "w": 6, "x": 6, "y": 21}, "dtdurations", decimals=1),
        stat("Free Heap", last_query("B", "heap"), {"h": 4, "w": 6, "x": 12, "y": 21}, "bytes",
             [{"color": "red", "value": None}, {"color": "orange", "value": 20000},
              {"color": "green", "value": 40000}], 0),
        stat("Controller Temperature", last_query("°C", "controller_temp"),
             {"h": 4, "w": 6, "x": 18, "y": 21}, "celsius",
             [{"color": "green", "value": None}, {"color": "orange", "value": 60},
              {"color": "red", "value": 75}], 1),
        timeseries("WiFi signal history", [target(unit_query("dBm", "rssi"), "A", "RSSI")],
                   {"h": 7, "w": 12, "x": 0, "y": 25}, "dBm"),
        timeseries("Free heap history", [target(unit_query("B", "heap"), "A", "Free Heap")],
                   {"h": 7, "w": 12, "x": 12, "y": 25}, "bytes"),
    ]),
]

variables = [
    textbox_var("pool_temp", "Pool temperature entity", "pool_controller_pool_temperature"),
    textbox_var("solar_temp", "Solar temperature entity", "pool_controller_solar_temperature"),
    textbox_var("controller_temp", "Controller temperature entity", "pool_controller_controller_temperature"),
    textbox_var("pool_pump", "Pool pump entity", "pool_controller_pool_pump"),
    textbox_var("solar_pump", "Solar pump entity", "pool_controller_solar_pump"),
    textbox_var("operation_mode", "Operation mode entity", "pool_controller_operation_mode"),
    textbox_var("effective_runtime", "Effective runtime entity", "pool_controller_effective_runtime"),
    textbox_var("circulation_extension", "Circulation extension entity", "pool_controller_circulation_extension"),
    textbox_var("rssi", "WiFi signal entity", "pool_controller_wifi_signal_strength"),
    textbox_var("uptime", "Uptime entity", "pool_controller_system_uptime"),
    textbox_var("heap", "Free heap entity", "pool_controller_free_heap_space"),
]

dashboard = {
    "__inputs": [{"name": "DS_INFLUXDB", "label": "InfluxDB", "description":
                  "InfluxDB (InfluxQL) database written by the Home Assistant InfluxDB integration",
                  "type": "datasource", "pluginId": "influxdb", "pluginName": "InfluxDB"}],
    "__requires": [
        {"type": "grafana", "id": "grafana", "name": "Grafana", "version": "10.0.0"},
        {"type": "datasource", "id": "influxdb", "name": "InfluxDB", "version": "1.0.0"},
        {"type": "panel", "id": "gauge", "name": "Gauge", "version": ""},
        {"type": "panel", "id": "stat", "name": "Stat", "version": ""},
        {"type": "panel", "id": "state-timeline", "name": "State timeline", "version": ""},
        {"type": "panel", "id": "timeseries", "name": "Time series", "version": ""},
    ],
    "title": "Smart Swimming Pool",
    "uid": "smart-swimming-pool",
    "description": "Pool Controller v5 (Home Assistant MQTT discovery) - data from the Home Assistant InfluxDB integration",
    "tags": ["smart-swimming-pool", "pool-controller", "home-assistant"],
    "editable": True,
    "graphTooltip": 1,
    "schemaVersion": 39,
    "version": 1,
    "time": {"from": "now-24h", "to": "now"},
    "refresh": "1m",
    "timepicker": {},
    "timezone": "browser",
    "annotations": {"list": []},
    "links": [{"title": "Smart Swimming Pool", "type": "link", "url": "https://smart-swimmingpool.com/",
               "targetBlank": True, "icon": "info"}],
    "templating": {"list": variables},
    "panels": panels,
}

print(json.dumps(dashboard, indent=2, ensure_ascii=False))
