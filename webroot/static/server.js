window.onload = function() {
    fetch('/cgi-bin/server.py', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('serverName').innerText = data.serverName;
        document.getElementById('serverAddress').innerText = data.serverAddress;
    })
    .catch(error => {
        console.error('Error:', error);
    });
};
