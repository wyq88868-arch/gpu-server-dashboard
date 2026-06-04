# -*- coding: utf-8 -*-
import os
import json
import time
import threading
import subprocess

def hidden_subprocess_kwargs():
    """Hide child console windows on Windows, especially ssh.exe console popup."""
    kwargs = {}
    try:
        if os.name == "nt":
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = 0
            kwargs["startupinfo"] = si
            kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    except Exception:
        pass
    return kwargs

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

APP_HOST = "127.0.0.1"
APP_PORT = 8766
CONFIG_FILE = "dashboard_config.json"

STATE_LOCK = threading.Lock()
STATE = {
    "connected": False,
    "status": "未连接",
    "last_update": None,
    "host": "wyqserver",
    "port": "22",
    "interval": "0.6",
    "meta": {},
    "memory": {},
    "gpus": [],
    "top_processes": [],
    "raw": "",
    "error": ""
}

MONITOR_PROC = None
MONITOR_THREAD = None
STOP_EVENT = threading.Event()

REMOTE_SCRIPT = r"""
import os
import time
import subprocess

INTERVAL = float("__INTERVAL__")

def run_cmd(args):
    try:
        p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        return p.stdout.strip()
    except Exception:
        return ""

def run_shell(cmd):
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
        return p.stdout.strip()
    except Exception:
        return ""

def has_cmd(name):
    return subprocess.call("command -v %s >/dev/null 2>&1" % name, shell=True) == 0

while True:
    print("__BEGIN__", flush=True)

    print("__META__", flush=True)
    print("time|" + time.strftime("%Y-%m-%d %H:%M:%S"), flush=True)
    print("host|" + run_cmd(["hostname"]), flush=True)
    print("uptime|" + (run_cmd(["uptime", "-p"]) or run_cmd(["uptime"])), flush=True)

    try:
        with open("/proc/loadavg", "r") as f:
            parts = f.read().strip().split()
        load = ",".join(parts[:3])
    except Exception:
        load = ""
    print("load|" + load, flush=True)
    print("cpu_cores|" + str(os.cpu_count() or ""), flush=True)

    print("__MEM__", flush=True)
    try:
        meminfo = {}
        with open("/proc/meminfo", "r") as f:
            for line in f:
                k, v = line.split(":", 1)
                meminfo[k] = int(v.strip().split()[0]) * 1024
        total = meminfo.get("MemTotal", 0)
        available = meminfo.get("MemAvailable", 0)
        cache = meminfo.get("Cached", 0) + meminfo.get("SReclaimable", 0)
        used = max(0, total - available)
        print("total|%s" % total, flush=True)
        print("used|%s" % used, flush=True)
        print("available|%s" % available, flush=True)
        print("cache|%s" % cache, flush=True)
    except Exception:
        pass

    print("__DISK__", flush=True)
    try:
        st = os.statvfs("/")
        total = st.f_blocks * st.f_frsize
        avail = st.f_bavail * st.f_frsize
        used = total - avail
        percent = int(used * 100 / total) if total else 0
        print("root_total|%s" % total, flush=True)
        print("root_used|%s" % used, flush=True)
        print("root_avail|%s" % avail, flush=True)
        print("root_percent|%s%%" % percent, flush=True)
    except Exception:
        pass

    print("__GPU_INFO__", flush=True)
    gpu_info = ""
    if has_cmd("nvidia-smi"):
        gpu_info = run_cmd([
            "nvidia-smi",
            "--query-gpu=index,uuid,name,temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw,power.limit",
            "--format=csv,noheader,nounits"
        ])
        if gpu_info:
            print(gpu_info, flush=True)
    else:
        print("NO_NVIDIA_SMI", flush=True)

    print("__GPU_PROCS__", flush=True)
    if has_cmd("nvidia-smi"):
        procs = run_cmd([
            "nvidia-smi",
            "--query-compute-apps=gpu_uuid,pid,process_name,used_memory",
            "--format=csv,noheader,nounits"
        ])
        if procs:
            print(procs, flush=True)

    print("__PS_DETAIL__", flush=True)
    if has_cmd("nvidia-smi"):
        pid_text = run_cmd([
            "nvidia-smi",
            "--query-compute-apps=pid",
            "--format=csv,noheader,nounits"
        ])
        pids = []
        for x in pid_text.splitlines():
            x = x.strip()
            if x.isdigit() and x not in pids:
                pids.append(x)
        if pids:
            out = run_cmd(["ps", "-p", ",".join(pids), "-o", "pid=,user=,etime=,args="])
            if out:
                print(out, flush=True)

    print("__TOP_PROC__", flush=True)
    top_proc = run_cmd(["ps", "-eo", "pid,user,pcpu,pmem,comm", "--sort=-pcpu"])
    if top_proc:
        print("\n".join(top_proc.splitlines()[:12]), flush=True)

    print("__END__", flush=True)
    time.sleep(INTERVAL)
"""

HTML = r'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Server Resource Dashboard V2.4</title>
  <style>
    :root {
      --bg1: #eef7ff;
      --bg2: #f7f2ff;
      --card: rgba(255,255,255,0.74);
      --line: rgba(15, 23, 42, 0.08);
      --text: #111827;
      --muted: #64748b;
      --blue: #1683f7;
      --green: #36c66c;
      --orange: #ff970e;
      --purple: #a855f7;
      --red: #ef4444;
      --shadow: 0 24px 70px rgba(15, 23, 42, .10);
      --softshadow: 0 12px 35px rgba(15, 23, 42, .07);
      --radius: 28px;
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", Arial, sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at 0% 0%, rgba(22,131,247,.18), transparent 28%),
        radial-gradient(circle at 100% 5%, rgba(168,85,247,.16), transparent 28%),
        linear-gradient(120deg, var(--bg1), #f8fbff 48%, var(--bg2));
      min-height: 100vh;
      overflow-x: hidden;
    }

    .app { width: min(1840px, calc(100vw - 52px)); margin: 28px auto 60px; }
    .topbar { display: flex; align-items: center; justify-content: space-between; gap: 18px; margin-bottom: 20px; }
    .brand { display: flex; align-items: center; gap: 14px; }
    .logo {
      width: 48px; height: 48px; border-radius: 16px;
      background: linear-gradient(135deg, #1683f7, #7c3aed);
      box-shadow: 0 14px 35px rgba(22, 131, 247, .30);
      display: grid; place-items: center; color: white; font-weight: 950; letter-spacing: -1px;
    }
    h1 { margin: 0; font-size: 28px; letter-spacing: -0.04em; line-height: 1.08; }
    .subtitle { margin-top: 4px; color: var(--muted); font-size: 13px; font-weight: 650; }

    .controls {
      display: flex; align-items: center; flex-wrap: wrap; justify-content: flex-end; gap: 10px;
      padding: 12px; border: 1px solid var(--line); border-radius: 22px;
      background: rgba(255,255,255,.62); box-shadow: var(--softshadow); backdrop-filter: blur(18px);
    }

    input {
      width: 180px; height: 42px; border: 1px solid var(--line); border-radius: 14px;
      padding: 0 12px; outline: none; background: rgba(255,255,255,.82); font-weight: 750; color: #0f172a;
    }
    input.port { width: 76px; }
    input.interval { width: 90px; }

    button {
      height: 42px; border: none; border-radius: 14px; padding: 0 16px;
      font-weight: 900; cursor: pointer; transition: .18s ease; color: white;
      background: linear-gradient(135deg, #1683f7, #4f46e5);
      box-shadow: 0 12px 28px rgba(22,131,247,.22);
    }
    button:hover { transform: translateY(-1px); filter: brightness(1.02); }
    button.secondary { color: #334155; background: rgba(255,255,255,.86); border: 1px solid var(--line); box-shadow: none; }
    button.danger { background: linear-gradient(135deg, #ef4444, #f97316); box-shadow: 0 12px 28px rgba(239,68,68,.18); }

    .status-pill {
      display: inline-flex; align-items: center; gap: 8px; padding: 10px 14px; border-radius: 999px;
      background: rgba(255,255,255,.86); border: 1px solid var(--line);
      font-size: 13px; font-weight: 900; color: #334155;
    }
    .dot { width: 10px; height: 10px; border-radius: 999px; background: var(--red); box-shadow: 0 0 0 5px rgba(239,68,68,.12); }
    .dot.on { background: #22c55e; box-shadow: 0 0 0 5px rgba(34,197,94,.13); }

    .section-label { margin: 22px 0 5px; font-size: 13px; letter-spacing: .12em; text-transform: uppercase; font-weight: 1000; color: #64748b; }
    .section-title-row { display: flex; align-items: end; justify-content: space-between; gap: 16px; margin-bottom: 14px; }
    .memory-card .section-title-row { padding-right: 150px; }
    .memory-card .hint { max-width: 620px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-align: right; }
    h2 { margin: 0; font-size: 30px; letter-spacing: -0.055em; }
    .hint { color: var(--muted); font-size: 14px; font-weight: 700; }

    .memory-card {
      border: 1px solid var(--line); border-radius: var(--radius);
      background: linear-gradient(120deg, rgba(255,255,255,.78), rgba(255,255,255,.54));
      box-shadow: var(--shadow); backdrop-filter: blur(22px); padding: 22px; position: relative; overflow: hidden;
    }
    .memory-card::after {
      content: ""; position: absolute; right: -110px; top: -130px; width: 330px; height: 330px; border-radius: 999px;
      background: radial-gradient(circle, rgba(168,85,247,.16), transparent 70%); pointer-events: none;
    }
    .memory-main { display: grid; grid-template-columns: 150px 1fr; gap: 28px; align-items: center; }

    .ring {
      --p: 0; width: 150px; height: 150px; border-radius: 50%;
      background: conic-gradient(var(--blue) calc(var(--p) * 1%), #e9eef5 0);
      display: grid; place-items: center; box-shadow: inset 0 0 0 1px rgba(15,23,42,.04); position: relative;
    }
    .ring::before { content: ""; position: absolute; width: 92px; height: 92px; border-radius: 50%; background: rgba(255,255,255,.94); }
    .ring-inner { position: relative; text-align: center; z-index: 1; }
    .ring-value { font-size: 28px; font-weight: 1000; letter-spacing: -0.06em; }
    .ring-label { color: #64748b; text-transform: uppercase; font-weight: 1000; font-size: 11px; margin-top: 3px; }

    .metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
    .mini-card { border: 1px solid var(--line); border-radius: 18px; background: rgba(255,255,255,.62); padding: 18px 16px; min-height: 78px; }
    .mini-label { color: #64748b; font-size: 12px; font-weight: 1000; text-transform: uppercase; letter-spacing: .04em; }
    .mini-value { margin-top: 8px; font-size: 20px; font-weight: 1000; letter-spacing: -0.04em; }
    .loadbar { margin-top: 18px; border: 1px solid var(--line); border-radius: 16px; padding: 12px 14px; background: rgba(255,255,255,.56); color: #334155; font-size: 13px; font-weight: 650; }
    .badge { position: absolute; right: 22px; top: 20px; padding: 10px 14px; border-radius: 999px; background: rgba(22,131,247,.12); color: #0b6bdb; font-weight: 1000; }

    .gpu-grid { display: grid; grid-template-columns: repeat(4, minmax(280px, 1fr)); gap: 18px; }
    .gpu-card {
      border: 1px solid var(--line); border-radius: 26px; background: var(--card);
      box-shadow: var(--softshadow); backdrop-filter: blur(20px); padding: 18px; min-height: 440px; overflow: hidden; position: relative;
    }
    .gpu-card::before { content: ""; position: absolute; inset: 0 0 auto 0; height: 118px; background: linear-gradient(90deg, rgba(22,131,247,.12), transparent); pointer-events: none; }
    .gpu-card.green::before { background: linear-gradient(90deg, rgba(54,198,108,.14), transparent); }
    .gpu-card.orange::before { background: linear-gradient(90deg, rgba(255,151,14,.16), transparent); }
    .gpu-card.purple::before { background: linear-gradient(90deg, rgba(168,85,247,.16), transparent); }

    .gpu-head { position: relative; display: grid; grid-template-columns: 56px 1fr auto; gap: 10px; align-items: center; z-index: 1; }
    .gpu-icon {
      width: 56px; height: 56px; border-radius: 16px; background: var(--blue); color: white;
      display: grid; place-items: center; font-size: 12px; font-weight: 1000; line-height: 1.0; text-align: center;
      box-shadow: 0 12px 26px rgba(22,131,247,.22);
    }
    .green .gpu-icon { background: var(--green); box-shadow: 0 12px 26px rgba(54,198,108,.22); }
    .orange .gpu-icon { background: var(--orange); box-shadow: 0 12px 26px rgba(255,151,14,.22); }
    .purple .gpu-icon { background: var(--purple); box-shadow: 0 12px 26px rgba(168,85,247,.22); }

    .gpu-name { font-weight: 1000; letter-spacing: -0.025em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .temp { padding: 8px 11px; border: 1px solid var(--line); border-radius: 999px; background: rgba(255,255,255,.78); font-weight: 1000; font-size: 13px; }

    .vram-box { position: relative; margin-top: 16px; border: 1px solid var(--line); border-radius: 22px; background: rgba(255,255,255,.66); padding: 22px 16px 16px; z-index: 1; }
    .vram-value { font-size: 28px; line-height: 1; font-weight: 1000; letter-spacing: -0.06em; }
    .vram-sub { margin-top: 8px; color: var(--muted); font-size: 13px; font-weight: 700; }
    .progress { margin-top: 14px; width: 100%; height: 18px; border-radius: 999px; background: #e5e7eb; overflow: hidden; }
    .bar { height: 100%; width: 0%; border-radius: inherit; background: linear-gradient(90deg, #4aa3ff, var(--blue)); transition: width .25s ease; }
    .green .bar { background: linear-gradient(90deg, #86efac, var(--green)); }
    .orange .bar { background: linear-gradient(90deg, #fbbf24, var(--orange)); }
    .purple .bar { background: linear-gradient(90deg, #d8b4fe, var(--purple)); }

    .stat-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 14px; }
    .stat { border: 1px solid var(--line); border-radius: 18px; background: rgba(255,255,255,.60); padding: 14px 12px; }
    .stat-label { color: var(--muted); font-size: 11px; font-weight: 1000; text-transform: uppercase; letter-spacing: .08em; }
    .stat-value { margin-top: 8px; font-size: 19px; font-weight: 1000; letter-spacing: -0.04em; }

    .proc-title { margin-top: 16px; color: var(--muted); font-size: 12px; font-weight: 1000; text-transform: uppercase; letter-spacing: .08em; }
    .proc-list { margin-top: 8px; max-height: 190px; overflow-y: auto; padding-right: 4px; overscroll-behavior: contain; }
    .proc-item { border: 1px solid var(--line); border-radius: 16px; background: rgba(255,255,255,.62); padding: 12px; margin-bottom: 8px; font-size: 12px; }
    .proc-line1 { display: flex; justify-content: space-between; gap: 10px; font-weight: 1000; font-size: 13px; }
    .proc-meta { margin-top: 5px; color: var(--muted); font-weight: 700; }
    .proc-cmd { margin-top: 6px; color: #334155; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-family: Consolas, monospace; font-size: 11px; }

    .bottom-grid { display: grid; grid-template-columns: 1.15fr .85fr; gap: 18px; margin-top: 18px; align-items: start; }
    .panel { border: 1px solid var(--line); border-radius: 24px; background: rgba(255,255,255,.66); box-shadow: var(--softshadow); padding: 18px; backdrop-filter: blur(20px); }
    .panel h3 { margin: 0 0 12px; font-size: 20px; letter-spacing: -0.04em; }
    pre { margin: 0; white-space: pre-wrap; font-family: Consolas, "Courier New", monospace; font-size: 12px; line-height: 1.45; color: #334155; max-height: 250px; overflow: auto; }
    .summary-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
    .summary-item { border: 1px solid var(--line); border-radius: 16px; background: rgba(255,255,255,.62); padding: 12px; }
    .summary-key { color: var(--muted); font-size: 11px; font-weight: 1000; text-transform: uppercase; letter-spacing: .08em; }
    .summary-val { margin-top: 6px; font-weight: 900; color: #0f172a; word-break: break-all; }
    .panel-subtitle { margin: -6px 0 12px; color: var(--muted); font-size: 12px; font-weight: 750; line-height: 1.45; }
    .top-table { display: grid; gap: 8px; max-height: 430px; overflow: auto; padding-right: 4px; overscroll-behavior: contain; }
    .top-row { display: grid; grid-template-columns: 82px minmax(90px, 1fr) 82px 82px 72px minmax(160px, 1.6fr); gap: 8px; align-items: center; border: 1px solid var(--line); border-radius: 14px; background: rgba(255,255,255,.62); padding: 10px; font-family: Consolas, monospace; font-size: 12px; }
    .top-row.header { position: sticky; top: 0; z-index: 2; background: rgba(255,255,255,.96); color: var(--muted); font-weight: 1000; text-transform: uppercase; font-family: inherit; box-shadow: 0 8px 20px rgba(15,23,42,.04); }
    .top-cell-ellipsis { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .cpu-panel { min-height: 520px; }
    .error-box { border: 1px solid rgba(239,68,68,.2); background: rgba(239,68,68,.06); color: #991b1b; border-radius: 16px; padding: 12px; font-family: Consolas, monospace; font-size: 12px; white-space: pre-wrap; }
    .ok-box { border: 1px solid rgba(34,197,94,.2); background: rgba(34,197,94,.07); color: #166534; border-radius: 16px; padding: 12px; font-weight: 850; }

    .empty { min-height: 300px; border: 1px dashed rgba(100,116,139,.28); border-radius: 26px; display: grid; place-items: center; color: var(--muted); font-weight: 850; background: rgba(255,255,255,.42); }

    @media (max-width: 1450px) { .gpu-grid { grid-template-columns: repeat(2, minmax(280px, 1fr)); } }
    @media (max-width: 900px) {
      .topbar { align-items: stretch; flex-direction: column; }
      .controls { justify-content: flex-start; }
      .memory-main { grid-template-columns: 1fr; }
      .metric-grid { grid-template-columns: repeat(2, 1fr); }
      .gpu-grid { grid-template-columns: 1fr; }
      .bottom-grid { grid-template-columns: 1fr; }
      input { width: 100%; }
    }
  </style>
</head>
<body>
  <main class="app">
    <div class="topbar">
      <div class="brand">
        <div class="logo">GPU</div>
        <div>
          <h1>Server Resource Dashboard V2.4</h1>
          <div class="subtitle">V2.4 · Hidden SSH subprocess · no console popup</div>
        </div>
      </div>
      <div class="controls">
        <span class="status-pill"><span id="dot" class="dot"></span><span id="status">未连接</span></span>
        <input id="host" placeholder="wyqserver 或 user@ip" />
        <input id="port" class="port" placeholder="22" />
        <input id="interval" class="interval" placeholder="0.6" />
        <button onclick="connect()">连接</button>
        <button class="danger" onclick="disconnect()">断开</button>
        <button class="secondary" onclick="saveConfig()">保存</button>
      </div>
    </div>

    <div class="section-label">System RAM</div>
    <section class="memory-card">
      <div id="memBadge" class="badge">0% used</div>
      <div class="section-title-row">
        <h2>Memory</h2>
        <div class="hint" id="metaHint">等待连接</div>
      </div>

      <div class="memory-main">
        <div class="ring" id="memRing" style="--p:0">
          <div class="ring-inner">
            <div class="ring-value" id="memPercent">0%</div>
            <div class="ring-label">Used</div>
          </div>
        </div>
        <div>
          <div class="metric-grid">
            <div class="mini-card"><div class="mini-label">Used</div><div class="mini-value" id="memUsed">-</div></div>
            <div class="mini-card"><div class="mini-label">Total</div><div class="mini-value" id="memTotal">-</div></div>
            <div class="mini-card"><div class="mini-label">Available</div><div class="mini-value" id="memAvailable">-</div></div>
            <div class="mini-card"><div class="mini-label">Cache</div><div class="mini-value" id="memCache">-</div></div>
          </div>
          <div class="loadbar" id="loadText">Load: -</div>
        </div>
      </div>
    </section>

    <div class="section-label">GPU Memory</div>
    <div class="section-title-row">
      <h2>GPU Resources</h2>
      <div class="hint">Per-GPU memory, power, utilization, temperature, and processes</div>
    </div>
    <section id="gpuGrid" class="gpu-grid">
      <div class="empty">连接服务器后显示 GPU 资源</div>
    </section>

    <section class="bottom-grid">
      <div class="panel cpu-panel"><h3>CPU Processes</h3><div class="panel-subtitle">Top 60 by CPU. Core % can exceed 100% for multi-threaded jobs; Total % is normalized by CPU cores.</div><div id="topProc" class="top-table">-</div></div>
      <div class="panel"><h3>Server Summary</h3><div id="raw">-</div></div>
    </section>
  </main>

<script>
if (!window.CSS) window.CSS = {};
if (!CSS.escape) CSS.escape = s => String(s).replace(/"/g, '\\"').replace(/\\/g, "\\\\");
const colors = ["blue", "green", "orange", "purple"];
const hostEl = document.getElementById("host");
const portEl = document.getElementById("port");
const intervalEl = document.getElementById("interval");

function bytesToGiB(v) {
  if (!v || isNaN(v)) return "-";
  return (Number(v) / 1024 / 1024 / 1024).toFixed(2) + " GiB";
}
function mibToGiB(v) {
  if (v === null || v === undefined || v === "" || isNaN(v)) return "-";
  return (Number(v) / 1024).toFixed(2);
}
function pct(a, b) {
  a = Number(a); b = Number(b);
  if (!b || isNaN(a) || isNaN(b)) return 0;
  return Math.max(0, Math.min(100, Math.round(a * 100 / b)));
}
function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, m => ({"&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"}[m]));
}
async function api(path, opts={}) {
  const res = await fetch(path, opts);
  return await res.json();
}
async function saveConfig() {
  await api("/api/config", {
    method: "POST",
    body: JSON.stringify({ host: hostEl.value, port: portEl.value, interval: intervalEl.value })
  });
}
async function connect() {
  await saveConfig();
  await api("/api/start", { method: "POST" });
  setTimeout(refresh, 300);
}
async function disconnect() {
  await api("/api/stop", { method: "POST" });
  setTimeout(refresh, 300);
}
async function loadConfig() {
  const data = await api("/api/status");
  hostEl.value = data.host || "wyqserver";
  portEl.value = data.port || "22";
  intervalEl.value = data.interval || "0.6";
  render(data);
}
let gpuStructureSignature = "";

function render(data) {
  document.getElementById("status").textContent = data.status || "未知";
  document.getElementById("dot").className = "dot" + (data.connected ? " on" : "");

  const m = data.memory || {};
  const used = Number(m.used || 0);
  const total = Number(m.total || 0);
  const available = Number(m.available || 0);
  const cache = Number(m.cache || 0);
  const memP = pct(used, total);

  document.getElementById("memRing").style.setProperty("--p", memP);
  document.getElementById("memPercent").textContent = memP + "%";
  document.getElementById("memBadge").textContent = memP + "% used";
  document.getElementById("memUsed").textContent = bytesToGiB(used);
  document.getElementById("memTotal").textContent = bytesToGiB(total);
  document.getElementById("memAvailable").textContent = bytesToGiB(available);
  document.getElementById("memCache").textContent = bytesToGiB(cache);

  const meta = data.meta || {};
  document.getElementById("metaHint").textContent =
    [meta.host, meta.time, data.last_update ? "local " + data.last_update : ""].filter(Boolean).join(" · ");
  document.getElementById("loadText").textContent = `Load: ${meta.load || "-"}    Uptime: ${meta.uptime || "-"}`;

  renderGpuGridIncremental(data.gpus || [], !!data.connected);
  renderTopProcesses(data.top_processes || [], Number(meta.cpu_cores || 1));
  renderSummary(data);
}

function gpuSig(gpus) {
  return gpus.map(g => {
    const procs = (g.processes || []).map(p => p.pid).join(",");
    return `${g.index}:${g.uuid}:${procs}`;
  }).join(";");
}

function renderGpuGridIncremental(gpus, connected) {
  const grid = document.getElementById("gpuGrid");
  if (!gpus.length) {
    const msg = connected ? "未检测到 GPU 或 nvidia-smi 无输出" : "连接服务器后显示 GPU 资源";
    if (grid.dataset.emptyMsg !== msg) {
      grid.innerHTML = `<div class="empty">${msg}</div>`;
      grid.dataset.emptyMsg = msg;
    }
    gpuStructureSignature = "";
    return;
  }

  const sig = gpuSig(gpus);
  if (sig !== gpuStructureSignature) {
    const procScroll = {};
    document.querySelectorAll(".proc-list").forEach(el => {
      procScroll[el.dataset.gpuIndex] = el.scrollTop;
    });

    grid.innerHTML = gpus.map((g, idx) => createGpuCardHtml(g, idx)).join("");
    gpuStructureSignature = sig;

    document.querySelectorAll(".proc-list").forEach(el => {
      const key = el.dataset.gpuIndex;
      if (procScroll[key] !== undefined) el.scrollTop = procScroll[key];
    });
  }

  gpus.forEach((g, idx) => updateGpuCard(g, idx));
}

function createGpuCardHtml(g, idx) {
  const cls = colors[idx % colors.length];
  const gi = esc(g.index);
  const procs = g.processes || [];
  const procHtml = procs.length ? procs.map(p => `
    <div class="proc-item" data-pid="${esc(p.pid)}">
      <div class="proc-line1">
        <span class="proc-title-main">PID ${esc(p.pid)} · ${esc(shortName(p.process_name || p.cmd || ""))}</span>
        <span class="proc-mem">${esc(p.used_memory || "-")} MiB</span>
      </div>
      <div class="proc-meta">user: <span class="proc-user">${esc(p.user || "-")}</span> · time: <span class="proc-time">${esc(p.etime || "-")}</span></div>
      <div class="proc-cmd">${esc(p.cmd || p.process_name || "-")}</div>
    </div>`).join("") : `<div class="proc-item">当前 GPU 上没有计算进程</div>`;

  return `
    <article class="gpu-card ${cls}" data-gpu-card="${gi}">
      <div class="gpu-head">
        <div class="gpu-icon">GPU<br>${gi}</div>
        <div class="gpu-name" data-field="name" title="${esc(g.name)}">${esc(g.name || "NVIDIA GPU")}</div>
        <div class="temp" data-field="temp">-°C</div>
      </div>
      <div class="vram-box">
        <div class="vram-value" data-field="vram">- / - GiB</div>
        <div class="vram-sub" data-field="vramSub">VRAM used · -%</div>
        <div class="progress"><div class="bar" data-field="bar" style="width:0%"></div></div>
      </div>
      <div class="stat-row">
        <div class="stat"><div class="stat-label">Util</div><div class="stat-value" data-field="util">-%</div></div>
        <div class="stat"><div class="stat-label">Power</div><div class="stat-value" data-field="power">-</div></div>
        <div class="stat"><div class="stat-label">Limit</div><div class="stat-value" data-field="limit">-</div></div>
      </div>
      <div class="proc-title">Running on this GPU</div>
      <div class="proc-list" data-gpu-index="${gi}">${procHtml}</div>
    </article>
  `;
}

function updateGpuCard(g, idx) {
  const card = document.querySelector(`[data-gpu-card="${CSS.escape(String(g.index))}"]`);
  if (!card) return;

  const usedM = Number(g.memory_used || 0);
  const totalM = Number(g.memory_total || 0);
  const p = pct(usedM, totalM);

  setText(card, '[data-field="name"]', g.name || "NVIDIA GPU");
  const nameEl = card.querySelector('[data-field="name"]');
  if (nameEl) nameEl.title = g.name || "NVIDIA GPU";

  setText(card, '[data-field="temp"]', `${g.temperature || "-"}°C`);
  setText(card, '[data-field="vram"]', `${mibToGiB(usedM)} / ${mibToGiB(totalM)} GiB`);
  setText(card, '[data-field="vramSub"]', `VRAM used · ${p}%`);
  const bar = card.querySelector('[data-field="bar"]');
  if (bar) bar.style.width = p + "%";
  setText(card, '[data-field="util"]', `${g.utilization || "-"}%`);
  setText(card, '[data-field="power"]', fmtPower(g.power_draw));
  setText(card, '[data-field="limit"]', fmtPower(g.power_limit));

  (g.processes || []).forEach(proc => {
    const row = card.querySelector(`.proc-item[data-pid="${CSS.escape(String(proc.pid))}"]`);
    if (!row) return;
    setText(row, ".proc-title-main", `PID ${proc.pid} · ${shortName(proc.process_name || proc.cmd || "")}`);
    setText(row, ".proc-mem", `${proc.used_memory || "-"} MiB`);
    setText(row, ".proc-user", proc.user || "-");
    setText(row, ".proc-time", proc.etime || "-");
    setText(row, ".proc-cmd", proc.cmd || proc.process_name || "-");
  });
}

function setText(root, selector, value) {
  const el = root.querySelector(selector);
  if (el && el.textContent !== String(value)) el.textContent = String(value);
}

function renderTopProcesses(lines, cpuCores=1) {
  const box = document.getElementById("topProc");
  const currentScroll = box.scrollTop;

  if (!lines || !lines.length) {
    if (box.dataset.empty !== "1") {
      box.innerHTML = `<div class="proc-item">暂无进程数据</div>`;
      box.dataset.empty = "1";
    }
    return;
  }

  const rows = lines.slice(1, 61).map(line => {
    const p = String(line).trim().split(/\s+/);
    if (p.length < 5) return "";
    const pid = p[0], user = p[1], coreCpu = Number(p[2] || 0), mem = p[3], cmd = p.slice(4).join(" ");
    const totalCpu = cpuCores ? (coreCpu / cpuCores).toFixed(1) : "-";
    return `<div class="top-row">
      <div>${esc(pid)}</div>
      <div class="top-cell-ellipsis" title="${esc(user)}">${esc(user)}</div>
      <div title="Raw Linux ps CPU%. Multi-threaded jobs can exceed 100%.">${esc(coreCpu)}%</div>
      <div title="CPU share normalized by ${esc(cpuCores)} CPU cores.">${esc(totalCpu)}%</div>
      <div>${esc(mem)}%</div>
      <div class="top-cell-ellipsis" title="${esc(cmd)}">${esc(cmd)}</div>
    </div>`;
  }).join("");

  const html = `<div class="top-row header">
      <div>PID</div><div>User</div><div>Core %</div><div>Total %</div><div>MEM</div><div>Command</div>
    </div>` + rows;

  if (box.dataset.lastHtml !== html) {
    box.innerHTML = html;
    box.dataset.lastHtml = html;
    box.scrollTop = currentScroll;
  }
}

function renderSummary(data) {
  const box = document.getElementById("raw");
  const meta = data.meta || {};
  const gpus = data.gpus || [];
  const totalVram = gpus.reduce((s, g) => s + Number(g.memory_total || 0), 0);
  const usedVram = gpus.reduce((s, g) => s + Number(g.memory_used || 0), 0);
  const gpuAvgUtil = gpus.length ? Math.round(gpus.reduce((s, g) => s + Number(g.utilization || 0), 0) / gpus.length) : 0;
  const gpuProcCount = gpus.reduce((s, g) => s + ((g.processes || []).length), 0);

  const err = data.error ? `<div class="error-box">${esc(data.error)}</div>` : `<div class="ok-box">Running normally. No active error.</div>`;

  const html = `
    <div class="summary-grid">
      <div class="summary-item"><div class="summary-key">Host</div><div class="summary-val">${esc(meta.host || "-")}</div></div>
      <div class="summary-item"><div class="summary-key">Remote Time</div><div class="summary-val">${esc(meta.time || "-")}</div></div>
      <div class="summary-item"><div class="summary-key">CPU Cores</div><div class="summary-val">${esc(meta.cpu_cores || "-")}</div></div>
      <div class="summary-item"><div class="summary-key">Load Avg</div><div class="summary-val">${esc(meta.load || "-")}</div></div>
      <div class="summary-item"><div class="summary-key">GPU Count</div><div class="summary-val">${gpus.length}</div></div>
      <div class="summary-item"><div class="summary-key">GPU Avg Util</div><div class="summary-val">${gpuAvgUtil}%</div></div>
      <div class="summary-item"><div class="summary-key">Total VRAM Used</div><div class="summary-val">${mibToGiB(usedVram)} / ${mibToGiB(totalVram)} GiB</div></div>
      <div class="summary-item"><div class="summary-key">GPU Processes</div><div class="summary-val">${gpuProcCount}</div></div>
    </div>
    <div style="height:10px"></div>
    ${err}
    <div style="height:10px"></div>
    <div class="summary-item">
      <div class="summary-key">CPU Process Table Note</div>
      <div class="summary-val" style="font-size:13px; line-height:1.5; font-weight:750;">
        Core % is the raw Linux process CPU usage. A multi-threaded Python job can show 600% because it is using roughly six CPU cores.
        Total % divides Core % by total CPU cores, so it is easier to understand whole-machine CPU share.
      </div>
    </div>
  `;

  if (box.dataset.lastHtml !== html) {
    box.innerHTML = html;
    box.dataset.lastHtml = html;
  }
}

function shortName(s) {
  s = String(s || "");
  return s.split(/[\\/]/).pop().split(/\s+/)[0].slice(0, 26);
}
function fmtPower(v) {
  if (v === null || v === undefined || v === "" || isNaN(v)) return "-";
  return Number(v).toFixed(1).replace(".0", "") + "W";
}
async function refresh() {
  try {
    const data = await api("/api/status");
    render(data);
  } catch (e) {
    document.getElementById("raw").textContent = String(e);
  }
}
loadConfig();
setInterval(refresh, 600);
</script>
</body>
</html>'''

def load_config():
    cfg = {"host": "wyqserver", "port": "22", "interval": "0.6"}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                old = json.load(f)
            cfg.update({k: str(v) for k, v in old.items() if k in cfg})
        except Exception:
            pass
    with STATE_LOCK:
        STATE["host"] = cfg["host"]
        STATE["port"] = cfg["port"]
        STATE["interval"] = cfg["interval"]
    return cfg

def save_config(cfg):
    clean = {
        "host": str(cfg.get("host") or "wyqserver").strip(),
        "port": str(cfg.get("port") or "22").strip(),
        "interval": str(cfg.get("interval") or "0.6").strip()
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(clean, f, ensure_ascii=False, indent=2)
    with STATE_LOCK:
        STATE.update(clean)
    return clean

def split_csv(line):
    return [x.strip() for x in line.split(",")]

def parse_key_values(lines):
    d = {}
    for line in lines:
        if "|" in line:
            k, v = line.split("|", 1)
            d[k.strip()] = v.strip()
    return d

def parse_block(raw):
    sections = {}
    current = None
    for line in raw.splitlines():
        if line.startswith("__") and line.endswith("__"):
            current = line
            sections[current] = []
        elif current:
            sections[current].append(line)

    meta = parse_key_values(sections.get("__META__", []))
    memory = parse_key_values(sections.get("__MEM__", []))
    disk = parse_key_values(sections.get("__DISK__", []))
    memory.update(disk)

    gpu_lines = sections.get("__GPU_INFO__", [])
    proc_lines = sections.get("__GPU_PROCS__", [])
    ps_lines = sections.get("__PS_DETAIL__", [])
    top_lines = sections.get("__TOP_PROC__", [])

    ps_map = {}
    for line in ps_lines:
        parts = line.split(None, 3)
        if len(parts) >= 3:
            pid = parts[0]
            ps_map[pid] = {
                "user": parts[1] if len(parts) > 1 else "",
                "etime": parts[2] if len(parts) > 2 else "",
                "cmd": parts[3] if len(parts) > 3 else ""
            }

    gpus = []
    uuid_to_gpu = {}
    for line in gpu_lines:
        if not line.strip() or line.strip() == "NO_NVIDIA_SMI":
            continue
        parts = split_csv(line)
        if len(parts) < 9:
            continue
        g = {
            "index": parts[0],
            "uuid": parts[1],
            "name": parts[2],
            "temperature": parts[3],
            "utilization": parts[4],
            "memory_used": parts[5],
            "memory_total": parts[6],
            "power_draw": parts[7],
            "power_limit": parts[8],
            "processes": []
        }
        uuid_to_gpu[g["uuid"]] = g
        gpus.append(g)

    for line in proc_lines:
        if not line.strip():
            continue
        parts = split_csv(line)
        if len(parts) < 4:
            continue
        gpu_uuid, pid, pname, used_mem = parts[:4]
        proc = {
            "gpu_uuid": gpu_uuid,
            "pid": pid,
            "process_name": pname,
            "used_memory": used_mem,
            "user": ps_map.get(pid, {}).get("user", ""),
            "etime": ps_map.get(pid, {}).get("etime", ""),
            "cmd": ps_map.get(pid, {}).get("cmd", pname),
        }
        if gpu_uuid in uuid_to_gpu:
            uuid_to_gpu[gpu_uuid]["processes"].append(proc)

    return {
        "meta": meta,
        "memory": memory,
        "gpus": gpus,
        "top_processes": top_lines,
        "raw": raw
    }

def set_state(**kwargs):
    with STATE_LOCK:
        STATE.update(kwargs)

def get_state():
    with STATE_LOCK:
        return json.loads(json.dumps(STATE, ensure_ascii=False))

def stop_monitor():
    global MONITOR_PROC
    STOP_EVENT.set()
    if MONITOR_PROC is not None:
        try:
            MONITOR_PROC.terminate()
        except Exception:
            pass
        MONITOR_PROC = None
    set_state(connected=False, status="已断开")

def monitor_loop(host, port, interval):
    global MONITOR_PROC
    STOP_EVENT.clear()
    script = REMOTE_SCRIPT.replace("__INTERVAL__", interval)

    cmd = [
        "ssh", "-p", str(port),
        "-o", "BatchMode=no",
        "-o", "ServerAliveInterval=15",
        "-o", "ServerAliveCountMax=3",
        host, "python3", "-u", "-"
    ]

    try:
        popen_kwargs = hidden_subprocess_kwargs()
        MONITOR_PROC = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            **popen_kwargs
        )
        MONITOR_PROC.stdin.write(script)
        MONITOR_PROC.stdin.close()
        set_state(connected=True, status="已连接：" + host, error="")
    except FileNotFoundError:
        set_state(connected=False, status="连接失败", error="未找到 ssh 命令。请安装/启用 Windows OpenSSH 客户端。")
        return
    except Exception as e:
        set_state(connected=False, status="连接失败", error=str(e))
        return

    block = []
    in_block = False

    try:
        for line in MONITOR_PROC.stdout:
            if STOP_EVENT.is_set():
                break
            line = line.rstrip("\n")
            if line == "__BEGIN__":
                block = ["__BEGIN__"]
                in_block = True
            elif line == "__END__":
                block.append("__END__")
                raw = "\n".join(block)
                parsed = parse_block(raw)
                parsed["last_update"] = time.strftime("%Y-%m-%d %H:%M:%S")
                parsed["connected"] = True
                parsed["status"] = "已连接：" + host
                parsed["error"] = ""
                set_state(**parsed)
                block = []
                in_block = False
            else:
                if in_block:
                    block.append(line)
                else:
                    if line.strip():
                        set_state(error=line)
    except Exception as e:
        set_state(error=str(e))

    try:
        if MONITOR_PROC is not None:
            MONITOR_PROC.terminate()
    except Exception:
        pass

    if not STOP_EVENT.is_set():
        set_state(connected=False, status="连接中断")
    MONITOR_PROC = None

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _html(self):
        body = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/" or path == "/index.html":
            self._html()
        elif path == "/api/status":
            self._json(get_state())
        else:
            self.send_error(404)

    def do_POST(self):
        global MONITOR_THREAD
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode("utf-8")) if raw else {}
        except Exception:
            data = {}

        if path == "/api/config":
            cfg = save_config(data)
            self._json({"ok": True, **cfg})
        elif path == "/api/start":
            cfg = load_config()
            stop_monitor()
            time.sleep(0.1)
            set_state(status="正在连接：" + cfg["host"], error="")
            MONITOR_THREAD = threading.Thread(
                target=monitor_loop,
                args=(cfg["host"], cfg["port"], cfg["interval"]),
                daemon=True
            )
            MONITOR_THREAD.start()
            self._json({"ok": True})
        elif path == "/api/stop":
            stop_monitor()
            self._json({"ok": True})
        else:
            self.send_error(404)

def open_app_window():
    try:
        import webview
    except Exception:
        print("缺少 pywebview，无法以软件窗口方式打开。")
        print("请先运行 install_dependencies.bat 安装依赖，然后再运行 run_desktop_app.bat。")
        print("也可以手动执行：py -3 -m pip install pywebview")
        return False

    url = "http://%s:%s/" % (APP_HOST, APP_PORT)
    webview.create_window(
        title="服务器资源查看器",
        url=url,
        width=1500,
        height=920,
        min_size=(1100, 720),
        resizable=True
    )
    webview.start()
    return True

def main():
    load_config()
    server = ThreadingHTTPServer((APP_HOST, APP_PORT), Handler)

    print("=" * 64)
    print("服务器资源查看器 V2.4 桌面窗口版 已启动")
    print("本地服务 V2：http://%s:%s/" % (APP_HOST, APP_PORT))
    print("请不要关闭这个黑色窗口；关闭软件窗口后会自动退出。")
    print("=" * 64)

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    try:
        ok = open_app_window()
        if not ok:
            input("按回车键退出...")
    except KeyboardInterrupt:
        pass
    finally:
        stop_monitor()
        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    main()
