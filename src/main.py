import os
import shutil

from cpstatic import cp_dir

from genpage import generate_page_recur

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

    print(f"Copy files from static directory {dir_stat} to public directory {dir_pub}!")
    cp_dir(dir_stat, dir_pub)
    
    print(f"Generating all content from {dir_cont} to public directory {dir_pub}!")
    generate_page_recur(dir_cont, dir_temp, dir_pub)

main()
