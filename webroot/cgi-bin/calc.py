#!/usr/bin/env python3

import cgi
import cgitb
import json

cgitb.enable()

def calculate(num1, num2, op):
    try:
        num1 = float(num1)
        num2 = float(num2)
        if op == 'plus':
            return num1 + num2
        elif op == 'minus':
            return num1 - num2
        elif op == 'multiply':
            return num1 * num2
        elif op == 'devide':
            if num2 == 0:
                return "Cannot divide by zero!"
            else:
                return num1 / num2
        else:
            return "Invalid operator"
    except Exception as e:
        return str(e)

print("Content-Type: application/json\n")

form = cgi.FieldStorage()
num1 = form.getvalue('num1')
num2 = form.getvalue('num2')
op = form.getvalue('op')

result = calculate(num1, num2, op)

if type(result) == str:
    print(json.dumps({"error": result}))
else:
    print(json.dumps({"result": result}))