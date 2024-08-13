from markdown import markdown_to_html_node

import os

from pathlib import Path

def extract_title(markdown):
    
    lines = markdown.split("\n")

    for line in lines:
        if line[0:2] == "# ":
            return line[2:]

    raise Exception("Markdown does not have title!")

def generate_page(src_path, template_path, dst_path):
    
    print(f"Generating page from {src_path} to {dst_path} using {template_path}!")

    fo = open(src_path)
    markdown = fo.read()
    fo.close()

    fo = open(template_path)
    template = fo.read()
    fo.close()

    html_body = markdown_to_html_node(markdown).to_html()
    html_title = extract_title(markdown)

    ba_title = template.split("{{ Title }}")
    html = ba_title[0] + html_title + ba_title[1]
    ba_content = html.split("{{ Content }}")
    html = ba_content[0] + html_body + ba_content[1]

    dest = os.path.dirname(dst_path)
    if dest != "":
        os.makedirs(dest, exist_ok=True)

    fo = open(dst_path, "w")
    fo.write(html)
    fo.close()

def generate_page_recur(src_path, template_path, dst_path):

    for fn in os.listdir(src_path):
        fp = os.path.join(src_path, fn)
        dp = os.path.join(dst_path, fn)
        
        if os.path.isfile(fp):
            dp = Path(dp).with_suffix(".html")
            generate_page(fp, template_path, dp)
        else:
            generate_page_recur(fp, template_path, dp)

        
    
