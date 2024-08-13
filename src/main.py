import os
import shutil

from cpstatic import cp_dir

from genpage import generate_page 

dir_pub  = "./public"
dir_stat = "./static"
dir_cont = "./content"
dir_temp = "./template.html"

def main():

    res = os.path.exists(dir_pub)
    print(f"Check that ./public exists: {res}")
    
    print("Removing ./public!")
    if os.path.exists(dir_pub):
        shutil.rmtree(dir_pub)

    res = os.path.exists(dir_pub)
    print(f"Check that ./public was removed: {res}")

    cp_dir(dir_stat, dir_pub)


    generate_page(os.path.join(dir_cont, "index.md"), dir_temp, os.path.join(dir_pub, "index.html"))

main()
