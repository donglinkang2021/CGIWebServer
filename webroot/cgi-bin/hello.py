import cgi

def read_template(filename):
    with open(filename, 'r') as file:
        return file.read()

# Read the HTML template
template = read_template('pages/hello.html')

form = cgi.FieldStorage()
name = form.getvalue("name")

# Replace placeholder with actual name
html_content = template.replace('{{name}}', name)

print(html_content)
