# CGI Multithreaded Web Server in Python: `webserver`🚀

## Quick start😋

1. Drag the `release\webserver.exe` to the folder you want to serve.
2. Double click the `webserver.exe` to start the server.
3. Open the browser and visit [localhost:8888](http://localhost:8888).

## Usage🧰

```shell
python main.py --port 8888 --work_dir ./webroot 
```

To compare the performance with default `http.server` in python:

```shell
cd webroot
python -m http.server --cgi 8888
```
