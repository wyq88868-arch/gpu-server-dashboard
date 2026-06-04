Server Resource Dashboard V2.3

This version makes the two deeper fixes you asked for:

1. Smooth scrolling:
   - V2.2 restored scroll position after rebuilding the GPU area.
   - V2.3 no longer rebuilds GPU cards every refresh.
   - It uses incremental DOM updates: only numbers, bars, temp, power, and process text are updated.
   - GPU cards are rebuilt only when the GPU/process structure changes.

2. CPU process section:
   - Renamed to CPU Processes.
   - Shows top 60 CPU processes.
   - Columns:
     PID
     User
     Core %
     Total %
     MEM
     Command

Explanation:
- Core % is the raw Linux ps CPU percentage.
  It can exceed 100% when a process uses multiple CPU cores.
  Example: 640% means about 6.4 CPU cores.

- Total % is normalized by server CPU core count.
  Example: 640% on a 128-core server equals 5.0% total machine CPU.

Recommended steps:
1. Close old dashboard windows.
2. Run:
   close_dashboard_ports.bat

3. Run:
   run_desktop_app_v23.bat

Backend:
- local port: 8766
- remote backend: python3 through SSH
