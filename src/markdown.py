

def markdown_to_blocks(markdown):
    blocks = []
    c_string = ""

    split_m = markdown.split("\n")

    for i, line in enumerate(split_m):
        split_m[i] = line.strip()
    
    b = True
    for i in range(len(split_m)):
        
        if split_m[i] == "" and b == False:
            b = True
            blocks.append(c_string)
            blocks[-1] = blocks[-1].strip("\n")
            c_string = ""
            continue
        elif split_m[i] == "" and b == True:
            continue
        else:
            b = False
        
        c_string += split_m[i]
        c_string += "\n"
    
    if c_string == "":
        return blocks

    blocks.append(c_string)
    blocks[-1] = blocks[-1].strip("\n")

    return blocks
