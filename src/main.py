import sys
from copystatic import cleanup_public_content, copy_static_content
from build_site import generate_pages_recursively


dir_path_static = "static"
dir_path_public = "docs"
dir_path_content = "content"
template_path = "template.html"


def main():
    basepath = ""
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        print(basepath + dir_path_public)
    cleanup_public_content(basepath + dir_path_public)
    copy_static_content(dir_path_static, basepath + dir_path_public)
    generate_pages_recursively(dir_path_content, template_path, dir_path_public, basepath)

main()