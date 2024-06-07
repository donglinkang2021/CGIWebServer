import cgi
template = open('pages/hello.html', 'r').read()
form = cgi.FieldStorage()
name = form.getvalue("name")
html_content = template.replace('{{name}}', name)
print(html_content)
