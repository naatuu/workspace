# 人工知能実験開発環境

## 1. コンテナを開く

1. このフォルダを VS Code で開く
2. `Reopen in Container` を実行する

## 2. 依存を同期する

コンテナ内のターミナルで実行:

```bash
uv sync --python 3.12
source .venv/bin/activate
```

## 3. Python を実行する

```bash
python src/main.py
```

## 4. GUI を実行する

`pygame` を使う GUI はホスト OS 側で実行する。

Linux / macOS:

```bash
python3.12 -m venv .venv-gui
source .venv-gui/bin/activate
python -m pip install pygame
PYTHONPATH=src python src/reversi-gui.py
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv-gui
.\.venv-gui\Scripts\Activate.ps1
python -m pip install pygame
$env:PYTHONPATH="src"
python src/reversi-gui.py
```

