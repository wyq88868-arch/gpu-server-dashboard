# Fixed Conda Build Script

The previous BAT exited after:

```text
Installing dependencies in isolated environment...
```

Cause:

On Windows, `conda` is commonly implemented as `conda.bat`.
Calling another BAT file without `call` transfers control away from the current script.

The fixed script uses:

```bat
call conda ...
```

for every Conda command.

## Run

Open Anaconda Prompt and enter the project folder:

```cmd
cd /d D:\桌面\查看
```

Then run:

```cmd
build_exe_clean_conda_FIXED.bat
```

Output:

```text
dist\GPU-Server-Dashboard.exe
```

If it still fails, run:

```cmd
build_manual_visible.bat
```

This shows each command directly and pauses on failure.
