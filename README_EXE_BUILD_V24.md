# GPU Server Dashboard V2.4 EXE Build Package

This package fixes the issue where clicking **Connect** opens a black `ssh.exe` console window.

## What changed

V2.4 starts the SSH subprocess with Windows hidden-window flags:

- `STARTF_USESHOWWINDOW`
- `SW_HIDE`
- `CREATE_NO_WINDOW`

So after building the exe:

- the main app opens as a desktop window;
- no CMD window is shown;
- `ssh.exe` should not pop up when clicking Connect.

## Build

Double-click:

```text
build_exe_no_console_v24.bat
```

The generated exe will be:

```text
dist\GPU-Server-Dashboard.exe
```

## If it still pops up

Build the debug version:

```text
build_exe_debug_console_v24.bat
```

Then run:

```text
dist\GPU-Server-Dashboard-Debug.exe
```

Send `build_log.txt` or the debug output for diagnosis.
