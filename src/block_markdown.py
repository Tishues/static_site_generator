from htmlnode import HTMLNode
from textnode import text_node_to_html_node
from inline_markdown import split_nodes_delimiter


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


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    all_blocks = []
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == block_type_paragraph:
            node = HTMLNode("p", None, text_to_children(block))
            all_blocks.append(node)

        if block_type == block_type_heading:
            level = block.count('#')
            text = block.lstrip('#').strip()
            node = HTMLNode(f"h{level}", None, text_to_children(text))
            all_blocks.append(node)

        if block_type == block_type_quote:
            node = HTMLNode("blockquote", None, text_to_children(block))
            all_blocks.append(node)

        if block_type == block_type_code:
            code_node = HTMLNode("code", None, text_to_children(block))
            pre_node = HTMLNode("pre", None, [code_node])
            all_blocks.append(pre_node)

        if block_type == block_type_unordered_list:
            items = block.split('\n')
            list_nodes = []
            for item in items:
                item_text = item.lstip('- ').lstrip('* ').lstrip('+ ').strip()
                list_node = HTMLNode("li", None, text_to_children(item_text))
                list_nodes.append(list_node)
            unlist_node = HTMLNode("ul", None, list_nodes)
            all_blocks.append(unlist_node)

        elif block_type == block_type_ordered_list:
            items = block.spit('\n')
            list_nodes = []
            for item in items:
                item_text = item.split('. ', 1)[1].strip()
                list_node = HTMLNode("li", None, text_to_children(item_text))
                list_nodes.append(list_node)
            ordlist_node = HTMLNode("ol", None, list_nodes)
            all_blocks.append(ordlist_node)

    return HTMLNode("div", None, all_blocks)
            

def text_to_children(text):
    text_nodes = split_nodes_delimiter(text) #Gives a list of TextNodes
    html_nodes = [] #Creates an empty list to store HTMLNodes
    for text_node in text_nodes: #Iterate though text_nodes
        html_node = text_node_to_html_node(text_node) #Convert each Textnode to HTMLNode
        html_nodes.append(html_node) #Add the new HTMLNode to our list
    return html_nodes