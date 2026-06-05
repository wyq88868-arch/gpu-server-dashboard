# Clean Conda Build Fix

Your build failed because the current Anaconda base environment contains the obsolete `pathlib` backport:

```text
ERROR: The 'pathlib' package is an obsolete backport ...
```

Do not build in the base environment.

## Recommended method

Open **Anaconda Prompt**, go to this folder, and run:

```text
build_exe_clean_conda.bat
```

The script creates an isolated environment:

```text
gpu-dashboard-build
```

It installs only:

```text
Python 3.12
pywebview
PyInstaller
```

Then it builds:

```text
dist\GPU-Server-Dashboard.exe
```

Your base environment is not modified.

## Manual quick fix

If you insist on using the current environment, remove the obsolete package:

```text
conda remove pathlib
```

or:

```text
py -3 -m pip uninstall pathlib
```

But using the isolated build environment is safer.
