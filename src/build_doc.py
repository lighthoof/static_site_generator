from markdown_to_html   import markdown_to_html_node
from logging import log
import os

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.strip().startswith("# "):
            return line.strip(" #")
    raise Exception("No title in markdown document")

def check_and_create_path(path):
    if not os.path.exists(path):
        folders = path.split("/")[0:-1]
        log(f"folder list : {folders}")
        #filename = dest_path.split("/")[-1]
        #log(f"filename - {filename}")

        current_path = ""
        for folder in folders:
            if not os.path.exists(folder):
                os.mkdir.folder()
            current_path += folder + "/"
            log(f"current folder - {current_path}")

def generate_page(from_path, template_path, dest_path):
    log(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as markdown_file:
        markdown_doc = markdown_file.read()
    with open(template_path, "r") as template_file:
        template_doc = template_file.read()

    html_doc = markdown_to_html_node(markdown_doc).to_html()
    title = extract_title(markdown_doc)

    
    html_in_template = template_doc.replace("{{ Content }}", html_doc)
    html_with_title = html_in_template.replace("{{ Title }}", title)

    check_and_create_path(dest_path)
        
    with open(dest_path, "w") as dest_file:
        dest_file.write(html_with_title)

    pass