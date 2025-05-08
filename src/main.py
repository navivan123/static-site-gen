import os
import shutil
import sys

from cpstatic import cp_dir

from genpage import generate_page_recur

dir_docs  = "./docs"
dir_stat = "./static"
dir_cont = "./content"
dir_temp = "./template.html"

def main():
    basepath = "/" if len(sys.argv) < 2 else sys.argv[1]

    print(f"Using base path: {basepath}")

    res = os.path.exists(dir_docs)
    print(f"Check that {dir_docs} exists: {res}")
    
    print(f"Removing {dir_docs}!")
    if os.path.exists(dir_docs):
        shutil.rmtree(dir_docs)

    res = os.path.exists(dir_docs)
    print(f"Check that {dir_docs} was removed: {res}")

    print(f"Copy files from static directory {dir_stat} to docs directory {dir_docs}!")
    cp_dir(dir_stat, dir_docs)
    
    print(f"Generating all content from {dir_cont} to docs directory {dir_docs}!")
    generate_page_recur(dir_cont, dir_temp, dir_docs, basepath)

main()
