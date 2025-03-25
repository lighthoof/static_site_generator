import os
import shutil
from logging import log

def cleanup_public_content():
    folder = "public"
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            except Exception as e:
                log("failed to delete %s. Reason: %s" % (path, e))
    else:
        os.mkdir("public")

def copy_static_content(folder="static", target_folder="public"):
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        try:
            if os.path.isfile(path):
                log(f"Copying file {path} to {target_folder}")
                shutil.copy(path, target_folder)
            if os.path.isdir(path):
                log(f"Copying folder {path} to {target_folder}")
                os.mkdir(os.path.join(target_folder, filename))

                current_folder = os.path.join(folder, filename)
                new_target_folder = os.path.join(target_folder, filename)
                log(f"Going into {current_folder} subfolder")
                copy_static_content(current_folder, new_target_folder)
        except Exception as e:
            log(f"Copying of %s to %s is unsuccessful. Reason : %s" % (filename, target_folder, e))
