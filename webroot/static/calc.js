document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();

    var num1 = document.querySelector('input[name="num1"]').value;
    var num2 = document.querySelector('input[name="num2"]').value;
    var operation = document.querySelector('select[name="operation"]').value;

    fetch('/cgi-bin/calc.py', {
        method: 'POST',
        body: new URLSearchParams({
            'num1': num1,
            'num2': num2,
            'operation': operation
        })
    })
    .then(response => response.json())
    .then(data => {
        // Update the page with the result
        document.querySelector('#result').textContent = data.result;
    });
});