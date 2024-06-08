function queryStudent(event) {
    event.preventDefault();  // 阻止表单的默认提交行为

    const form = document.getElementById('queryForm');
    const formData = new FormData(form);

    fetch('/cgi-bin/query.py', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const table = document.getElementById('resultTable');
        const tbody = document.getElementById('resultBody');
        const error = document.getElementById('error');

        tbody.innerHTML = '';  // 清空表格内容
        error.textContent = '';  // 清空错误信息

        if (data.error) {
            table.style.display = 'none';
            error.textContent = data.error;
        } else {
            table.style.display = 'table';
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${data.student_id}</td>
                <td>${data.student_name}</td>
                <td>${data.class}</td>
            `;
            tbody.appendChild(row);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    return false;  // 防止表单的默认提交行为
}