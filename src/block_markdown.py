block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered list"
block_type_ordered_list = "ordered list"


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


def block_to_block_type(markdown):
    lines = markdown.split('\n')
    
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if markdown.startswith("```") and markdown.endswith("```"):
        return block_type_code
    if all([line.startswith("> ") for line in lines]):
        return block_type_quote
    if all([line.startswith("* ") or line.startswith("- ") for line in lines]):
        return block_type_unordered_list
    is_ordered_list = True
    for i, line in enumerate(lines, 1):
        if not line.startswith(f"{i}. "):
            is_ordered_list = False  # Mark as not an ordered list, but keep going
    if is_ordered_list:
        return block_type_ordered_list
    return block_type_paragraph
