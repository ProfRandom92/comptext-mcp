$ErrorActionPreference = "Stop"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\pip.exe install .
.\.venv\Scripts\python.exe -c "import comptext_mcp; print('comptext-mcp import ok')"
