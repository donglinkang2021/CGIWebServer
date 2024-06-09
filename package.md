# Package

Here we will package the written program into an executable `exe` file.

## 1. Create `venv` virtual environment

```shell
python -m venv venv
venv\Scripts\Activate.ps1
```

```shell
pip install pyinstaller
```

## 2. Package

Here we have the following requirements

- The packaged program is `main.py`
- The icon file is `favicon.ico`

```shell
pyinstaller -F -i favicon.ico main.py
```
