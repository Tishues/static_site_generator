import os
import shutil
from copystatic import copy_files_recursive
from block_markdown import generate_page


dir_path_static = "./static"
dir_path_public = "./public"
from_path = "content/index.md"
template_path = "template.html" 
dest_path = "public/index.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_page(from_path, template_path, dest_path)
    

main()