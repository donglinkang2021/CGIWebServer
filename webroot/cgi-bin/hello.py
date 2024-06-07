import cgi
template = open('pages/hello.html', 'r').read()
form = cgi.FieldStorage()
name = form.getvalue("name")
html_content = template.replace('{{name}}', name)

# caculate content length
# the content length should be the length of the content in bytes
# and when we send the content to stdout
# the `\n` should be replaced by `\r\n
# and add an extra `\r\n` at the end of the content
content_length = len(html_content.replace("\n", "\r\n") + "\r\n")

head = "HTTP/1.1 200 OK\n"
head += "Content-Type: text/html\n"
head += f"Content-Length: {content_length}\n\n"
print(head + html_content)
