import cgi
import cgitb

# Enable CGI traceback for debugging
cgitb.enable()

def read_template(filename):
    with open(filename, 'r') as file:
        return file.read()

# Read the HTML template
template = read_template('pages/hello.html')

print("Content-type: text/html\n")

form = cgi.FieldStorage()
name = form.getvalue("name")

# Replace placeholder with actual name
html_content = template.replace('{{name}}', name)

print(html_content)
