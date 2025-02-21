from htmlnode import ParentNode, LeafNode
import re
import os
from textnode import text_node_to_html_node, TextType, TextNode
from inline_markdown import split_nodes_image, split_nodes_delimiter, split_nodes_link


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
        # print("Processing block:", repr(block))
        if "```" in block:
            result.append(block)
        else:
            cleaned  = block.strip()
            if cleaned:
                result.append(cleaned)
    return result


def block_to_block_type(markdown):
    lines = markdown.split('\n')
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if markdown.startswith("```") and markdown.endswith("```"):
        return block_type_code
    if all([line.startswith("> ") for line in lines]):
        return block_type_quote
    if any([line.startswith(("- ", "* ")) for line in lines if line.strip()]):
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
            # Remove the backticks but keep the rest of the formatting by splitting at lines
            lines = block.split('\n')
            # Keeps everything except the first and last lines which should be ``` in a code block
            code_content = '\n'.join(lines[1:-1]) 
            code_node = LeafNode("code", code_content) 
            pre_node = ParentNode("pre", [code_node])
            all_blocks.append(pre_node)

        elif block_type == block_type_unordered_list:
            items = block.split('\n')
            list_nodes = []
            for item in items:
                if item.startswith('- '):
                    item_text = item[2:]  # Just remove the "- " prefix
                elif item.startswith('* '):
                    item_text = item[2:]  # Just remove the "* " prefix
                else:
                    item_text = item
                list_node = ParentNode("li", text_to_children(item_text))
                list_nodes.append(list_node)
            unlist_node = ParentNode("ul", list_nodes)
            all_blocks.append(unlist_node)

        elif block_type == block_type_ordered_list:
            items = [item.strip() for item in block.split('\n') if item.strip()]
            list_nodes = []
            # Check if first item starts with a number
            is_ordered = items[0][0].isdigit()
            for item in items:
                # Strip numbers or dashes
                if is_ordered:
                    item_text = item[item.find('.')+1:].strip()
                else:
                    item_text = item[2:] if item.startswith(('- ', '* ')) else item
                list_nodes.append(ParentNode("li", text_to_children(item_text)))
            list_type = "ol" if is_ordered else "ul"
            all_blocks.append(ParentNode(list_type, list_nodes))

    return ParentNode("div", all_blocks)


def text_to_children(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)  
    processed_nodes = []
    for node in nodes:
        if isinstance(node, LeafNode):
            processed_nodes.append(node)
        else:
            temp_nodes = [node]
            temp_nodes = split_nodes_delimiter(temp_nodes, "**", TextType.BOLD)
            temp_nodes = split_nodes_delimiter(temp_nodes, "*", TextType.ITALIC)
            temp_nodes = split_nodes_delimiter(temp_nodes, "`", TextType.CODE)
            processed_nodes.extend(temp_nodes)
    
    html_nodes = []
    for node in processed_nodes:
        if isinstance(node, LeafNode):
            html_nodes.append(node)
        else:  # It's a TextNode
            html_nodes.append(text_node_to_html_node(node))

    return html_nodes


def extract_title(markdown):  
    h1_match = re.search(r"#\s+(.+)", markdown)
    if h1_match:
        return h1_match.group(1).strip()
    else:
        raise Exception("no header found")
    

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        read_from_path = file.read()
    with open(template_path) as file:
        read_from_template = file.read()
    node = markdown_to_html_node(read_from_path)
    html = node.to_html()
    page_title = extract_title(read_from_path)
    read_from_template = read_from_template.replace("{{ Title }}", page_title)
    read_from_template = read_from_template.replace("{{ Content }}", html)
    directory = os.path.dirname(dest_path)
    os.makedirs(directory, exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(read_from_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Get list of everything in the content directory
    entries = os.listdir(dir_path_content)
    
    for entry in entries:
        # Create full paths
        content_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(content_path) and entry.endswith('.md'):
            # It's a markdown file, generate the HTML
            if entry == 'index.md':
                # Always create index.html in the current dest directory
                html_path = os.path.join(dest_dir_path, 'index.html')
            else:
                # Handle other .md files
                base_name = os.path.splitext(entry)[0]
                html_path = os.path.join(dest_dir_path, base_name, 'index.html')
            
            # Make sure the destination directory exists
            os.makedirs(os.path.dirname(html_path), exist_ok=True)
            # Generate the page
            generate_page(content_path, template_path, html_path)
            
        elif os.path.isdir(content_path):
            # It's a directory, recurse into it
            new_dest = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(content_path, template_path, new_dest)
