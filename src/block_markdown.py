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
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered list"
    ordered_list = "ordered list"
    lines = markdown.split('\n')
    if markdown.startswith("# "):
        return heading
    if markdown.startswith("## "):
        return heading
    if markdown.startswith("### "):
        return heading
    if markdown.startswith("#### "):
        return heading
    if markdown.startswith("##### "):
        return heading
    if markdown.startswith("###### "):
        return heading
    if markdown.startswith("```") and markdown.endswith("```"):
        return code
    if all([line.startswith("> ") for line in lines]):
        return quote
    if all([line.startswith("* ") or line.startswith("- ") for line in lines]):
        return unordered_list
    is_ordered_list = True
    for i, line in enumerate(lines, 1):
        if not line.startswith(f"{i}. "):
            is_ordered_list = False  # Mark as not an ordered list, but keep going
    if is_ordered_list:
        return ordered_list
    return paragraph
