from markdown_to_html   import markdown_to_html_node
from logging import log
import os

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.strip().startswith("# "):
            return line.lstrip(" #")
    raise Exception("No title in markdown document")

def check_and_create_path(path):
    if not os.path.exists(path):
        folders = path.split("/")[0:-1]
        log(f"folder list - {folders}")

        current_path = ""
        for folder in folders:
            target_path = current_path + folder + "/"
            if not os.path.exists(target_path):
                log(f"Creating folder {target_path}")
                os.mkdir(target_path)
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

def generate_pages_recursively(dir_path_content="content", template_path="template.html", dest_dir_path="public" ):
    log(f"Generating site from {dir_path_content} to {dest_dir_path} using {template_path}")
    if not os.path.exists(dir_path_content):
        raise FileNotFoundError("Provided content path does not exist")
    
    content_dir_contents = os.scandir(dir_path_content)
    for entity in content_dir_contents:
        current_content_path = dir_path_content
        if entity.is_file():
            if entity.name.split(".")[-1] == "md":
                markdown_file = dir_path_content + "/" + entity.name
                html_doc = dest_dir_path + "/" + entity.name.split(".")[0]  + ".html"
                generate_page(markdown_file, template_path, html_doc)
        elif entity.is_dir():
            current_content_path += "/" + entity.name
            current_dest_path = dest_dir_path + "/" + entity.name
            generate_pages_recursively(current_content_path, template_path, current_dest_path)
    