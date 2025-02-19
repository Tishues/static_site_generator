from htmlnode import ParentNode
from textnode import text_node_to_html_node, TextType, TextNode
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
            cleaned_text = " ".join(block.split())
            node = ParentNode("p", text_to_children(cleaned_text))
            all_blocks.append(node)

        elif block_type == block_type_heading:
            level = block.count('#')
            text = block.lstrip('#').strip()
            node = ParentNode(f"h{level}", text_to_children(text))
            all_blocks.append(node)

        elif block_type == block_type_quote:
            text = " ".join(line.lstrip('>').strip() for line in block.split('\n'))
            node = ParentNode("blockquote", text_to_children(text))
            all_blocks.append(node)

        elif block_type == block_type_code:
            text = block.strip('`').strip()
            if '\n' in text:
                text = text.split('\n', 1)[1]
            code_node = ParentNode("code", text_to_children(text))
            pre_node = ParentNode("pre", [code_node])
            all_blocks.append(pre_node)

        elif block_type == block_type_unordered_list:
            items = block.split('\n')
            list_nodes = []
            for item in items:
                item_text = ""
                for i, char in enumerate(item):
                    if char not in ['*', '-', '+', ' ']:
                        item_text = item[i:].strip()
                        break
                if not item_text:
                    item_text = item.strip("*-+ ")
                list_node = ParentNode("li", text_to_children(item_text))
                list_nodes.append(list_node)
            unlist_node = ParentNode("ul", list_nodes)
            all_blocks.append(unlist_node)

        elif block_type == block_type_ordered_list:
            items = block.split('\n')
            list_nodes = []
            for item in items:
                try:
                    item_text = item.split('. ', 1)[1].strip()
                except IndexError:
                    item_text = ''.join(c for c in item if not c.isdigit()).strip('. ')
                list_node = ParentNode("li", text_to_children(item_text))
                list_nodes.append(list_node)
            ordlist_node = ParentNode("ol", list_nodes)
            all_blocks.append(ordlist_node)

    return ParentNode("div", all_blocks)
            

def text_to_children(text):
    nodes = [TextNode(text, TextType.TEXT)]  #Gives a list of TextNodes
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "__", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    html_nodes = [] #Creates an empty list to store HTMLNodes
    for node in nodes: #Iterate though text_nodes
        html_node = text_node_to_html_node(node) #Convert each Textnode to HTMLNode
        html_nodes.append(html_node) #Add the new HTMLNode to our list
    return html_nodes