window.onload = function() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/cgi-bin/server.py', true);
    xhr.onload = function() {
        if (this.status == 200) {
            var info = JSON.parse(this.responseText);
            document.getElementById('serverName').innerText = info.serverName;
            document.getElementById('serverAddress').innerText = info.serverAddress;
        }
    };
    xhr.send();
};
