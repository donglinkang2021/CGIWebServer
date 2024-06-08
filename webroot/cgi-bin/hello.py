import cgi
template = open('hello.html', 'r').read()
form = cgi.FieldStorage()
name = form.getvalue("name")
html_content = template.replace('{{name}}', name)
print("Content-Type: text/html\n")
print(html_content)