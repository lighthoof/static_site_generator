from copystatic import cleanup_public_content, copy_static_content
from build_site import generate_pages_recursively



def main():
    cleanup_public_content()
    copy_static_content()
    generate_pages_recursively("content", "template.html", "public")

main()