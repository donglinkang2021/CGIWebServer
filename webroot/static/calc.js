function calculate(event) {
    event.preventDefault();  // 阻止表单的默认提交行为

    const form = document.getElementById('calcForm');
    const formData = new FormData(form);

    fetch('/cgi-bin/calc.py', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const para = document.getElementById('result');
        para.style.display = 'block';    
        if (data.error) {
            para.innerHTML = `
                <span style="color: red;">
                ${data.error}
                </span>
            `;
        } else {
            para.innerHTML = `
                <span style="color: blue;">
                Result = ${data.result}
                </span>
            `;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    return false;  // 防止表单的默认提交行为
}