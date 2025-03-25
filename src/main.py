from copystatic import cleanup_public_content, copy_static_content
from build_doc import generate_page



def main():
    cleanup_public_content()
    copy_static_content()
    generate_page("content/index.md", "template.html", "public/index.html")

main()