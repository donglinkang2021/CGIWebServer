#!/usr/bin/env python3
import cgi
import cgitb
import json

cgitb.enable()

form = cgi.FieldStorage()

num1 = float(form.getvalue('num1'))
num2 = float(form.getvalue('num2'))
operation = form.getvalue('operation')

if operation == 'add':
    result = num1 + num2
elif operation == 'subtract':
    result = num1 - num2
elif operation == 'multiply':
    result = num1 * num2
elif operation == 'divide':
    if num2 != 0:
        result = num1 / num2
    else:
        result = 'Error: Division by zero'

response = {
    'result': result
}

print('Content-Type: application/json\n')
print(json.dumps(response))