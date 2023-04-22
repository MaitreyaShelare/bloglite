from jinja2 import Template
from weasyprint import HTML

def format_report(template_file, data={}):
    with open(template_file) as f:
        template = Template(f.read())
    return template.render(data=data)

def generate_report(data):
    message = format_report("bloglite/server/report.html", data=data)
    html=HTML(string=message)
    file_name = str(data['name']) + ".pdf"
    html.write_pdf(target=file_name)

def main():
    data = {
        "name": "John Doe",
        "age": 42,
        "occupation": "Software Engineer",
        "hobbies": ["Programming", "Reading", "Hiking"]
    }
    generate_report(data)

if __name__ == "__main__":
    main()