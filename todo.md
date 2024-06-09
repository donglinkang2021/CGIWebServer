# todo

- [x] HTTP Implementation
- [x] Ports and Addresses
- [x] Max Connections and Thread pool
- [x] CGI
- [x] Log File
- [x] File Organization
- [x] Test Cases
- [x] Performance Analysis

- [x] test `js` files
- [x] add `calc.html` use `cgi-bin/calc.py` to test
- [x] modify the `calc.html` return the result to the page
- [x] modify cgi code so that it can return `json` reponse
- [x] already stay problem here, because my `cgi` code is not working

- [x] already fix webroot bug here, now it can handle `cgi` correctly
- [x] modify my server to handle `cgi` correctly
- [x] `list_directory`
- [x] handle with 中文路径

- [x] Max Connections and Thread pool
- [x] we can `ctrl+c` to stop the server now

- [x] add logger

- one request one log line
- log format:
  - the visitor ip `remote_addr`
  - the request date and time `request_time`
  - the request first line `request_line`
  - the request `headers`
    - `User-Agent`
    - `Referer`

- [x] release
