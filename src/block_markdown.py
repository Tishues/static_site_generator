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
        print("Processing block:", repr(block))
        if "```" in block:
            # Debug: print blocks that contain ```
            #print("Found code block:", repr(block))
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
            code_content = '\n'.join(lines[1:-1]) #keeps everything except the first and last lines which should be ``` in a code block
            code_node = LeafNode("code", code_content)  # Use LeafNode instead of text_to_children
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
    nodes = split_nodes_link(nodes)  # Add this line!
    
     #Rest of your processing...
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
            if node.text_type == TextType.TEXT:
                html_nodes.append(LeafNode(None, node.text))
            elif node.text_type == TextType.BOLD:
                html_nodes.append(LeafNode("b", node.text))
            elif node.text_type == TextType.ITALIC:
                html_nodes.append(LeafNode("i", node.text))
            elif node.text_type == TextType.CODE:
                html_nodes.append(LeafNode("code", node.text))
            elif node.text_type == TextType.LINK:  # Add this case!
                html_nodes.append(LeafNode("a", node.text, {"href": node.url}))
    
    return html_nodes
#def text_to_children(text):
 #   nodes = [TextNode(text, TextType.TEXT)]  #Gives a list of TextNodes
  #  nodes = split_nodes_link(nodes)
   # nodes = split_nodes_image(nodes)
    #nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
#    nodes = split_nodes_delimiter(nodes, "__", TextType.BOLD)
 #   nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
  #  nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
   # nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    #html_nodes = [] #Creates an empty list to store HTMLNodes
#    for node in nodes: #Iterate though text_nodes
 #       html_node = text_node_to_html_node(node) #Convert each Textnode to HTMLNode
  #      html_nodes.append(html_node) #Add the new HTMLNode to our list
   # return html_nodes


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

#def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
 #   print("\n=== DEBUG ===")
  #  print(f"Current content dir: {dir_path_content}")
   # print(f"Template path: {template_path}")
    #print(f"Destination dir: {dest_dir_path}")
#    print("Files found:")
 #   for item in os.listdir(dir_path_content):
  #      print(f"  - {item}")
   # print("============")
    #print(f"\nProcessing directory: {dir_path_content}")
    # Process all entries in the current directory
#    for item in os.listdir(dir_path_content):
 #       source_path = os.path.join(dir_path_content, item)
  #      print(f"Looking at: {source_path}")
   #     
    #    if os.path.isfile(source_path) and item.endswith('.md'):
     #       # Create matching directory in public
      #      print(f"Found MD file: {source_path}")
       #     print(f"Will create HTML in: {dest_dir_path}")
        #    os.makedirs(dest_dir_path, exist_ok=True)
            # if you have:
            # dir_path_content = "content"
            # source_path = "content/majesty/index.md"

            # you can get:
         #   rel_path = os.path.relpath(source_path, dir_path_content)
          #  filename = os.path.basename(rel_path)
           # if filename == 'index.md':
                # For index.md files, we want the parent directory path
            #    parent_dir = os.path.dirname(rel_path)
             #   dest_file = os.path.join(dest_dir_path, parent_dir, 'index.html')
#            else:
 #               # For other .md files, replace extension with .html
  #              rel_path_html = rel_path.replace('.md', '.html')
   #             dest_file = os.path.join(dest_dir_path, rel_path_html)
    #            print(f"Generating: {dest_file}")
     #       generate_page(source_path, template_path, dest_file)
      #  
       # elif os.path.isdir(source_path):
        #    # Process subdirectory
         #   sub_dest_dir = os.path.join(dest_dir_path, item)
          #  print(f"Found directory, recursing into: {source_path}")
           # print(f"Will create files in: {sub_dest_dir}")
            #generate_pages_recursive(source_path, template_path, sub_dest_dir)
#def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
 #   print(f"Processing directory: {dir_path_content}")  # Debug print
  #  items = os.listdir(dir_path_content)
   # for item in items:
    #    content_full_path = os.path.join(dir_path_content, item)
     #   print(f"Looking at: {content_full_path}")  # Debug print
      #  
       # if os.path.isfile(content_full_path) and item.endswith('.md'):
            # Create equivalent directory structure in destination
        #    relative_path = os.path.relpath(os.path.dirname(content_full_path), dir_path_content)
         #   dest_dir = os.path.join(dest_dir_path, relative_path)
          #  os.makedirs(dest_dir, exist_ok=True)
            
            # This is where we change the destination path logic
           # if item == "index.md":
#                dest_full_path = os.path.join(dest_dir_path, os.path.dirname(relative_path), 'index.html')
 #           else:
  #              dest_full_path = os.path.join(dest_dir, item.replace('.md', '.html'))   
            # Generate the HTML file
            #dest_full_path = os.path.join(dest_dir, 'index.html')
   #         print(f"Generating: {dest_full_path}")  # Debug print
    #        generate_page(content_full_path, template_path, dest_full_path)
        
     #   elif os.path.isdir(content_full_path):
      #      new_dest_path = os.path.join(dest_dir_path, item)
       #     os.makedirs(new_dest_path, exist_ok=True)
        #    generate_pages_recursive(content_full_path, template_path, new_dest_path)

#def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
 #   items = os.listdir(dir_path_content)
  #  for item in items:
   #     content_full_path = os.path.join(dir_path_content, item)
    #    if os.path.isfile(content_full_path) and item.endswith('.md'):
     #       # Keep the name 'index.html' if the source is 'index.md'
      #      if item == 'index.md':
       #         html_name = 'index.html'
        #    else:
         #       html_name = item.replace('.md', '.html')
          #  dest_full_path = os.path.join(dest_dir_path, html_name)
           # generate_page(content_full_path, template_path, dest_full_path)
#        elif os.path.isdir(content_full_path):
 #           if item != "__pycache__":  # ignore Python cache directories
  #              new_dest_path = os.path.join(dest_dir_path, item)
   #             os.makedirs(new_dest_path, exist_ok=True)
    #            generate_pages_recursive(content_full_path, template_path, new_dest_path)

#os.listdir() - to see what's inside a directory
#os.path.join() - to create proper file paths
#os.path.isfile() - to check if something is a file (vs a directory)