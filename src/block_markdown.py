
def markdown_to_blocks(markdown):  
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        if block != "":
            text = block.strip()
            result.append(text)
        else:
            continue
    return result