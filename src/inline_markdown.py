from textnode import TextNode, TextType
from htmlnode import LeafNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)
        if len(sections) == 1:
            new_nodes.append(old_node)
            continue

        for i in range(len(sections)):
            if i % 2 == 0:
                if sections[i]:
                    new_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(sections[i], text_type))

    return new_nodes
#def split_nodes_delimiter(old_nodes, delimiter, text_type):
 #   print(f"\nStarting split_nodes_delimiter with delimiter: {delimiter}")
  #  new_nodes = [] #creating a new empty list
   # for old_node in old_nodes: #iterating through old nodes
        #print(f"Processing node: {old_node.text} of type: {old_node.text_type}")
    #    if old_node.text_type != TextType.TEXT: #checking if old node text type is .TEXT or not
     #       new_nodes.append(old_node) #if it isn't .TEXT append it because it's either an image or a link already
      #      continue #skip the rest ofthe code if it isn't a .TEXT type
       # split_nodes = [] #creating a new empty list for split nodes
        #sections = old_node.text.split(delimiter) #split the line at each delimiter
        #print(f"Original text: {old_node.text}")
#        print(f"Delimiter: {delimiter}")
 #       print(f"Sections: {sections}")
        #print(f"Number of sections: {len(sections)}")
  #      if len(sections) == 1:
   #         new_nodes.append(old_node)
    #        continue
     #   if len(sections) % 2 == 0: #checks to see if there's an even number of sections
      #      raise ValueError("invalid markdown, formatted section not closed")
       # for i in range(len(sections)): #loops through each section
        #    if sections[i] == "": #if the section is empty
         #       continue #skip the rest of the code in the block
          #  if i % 2 == 0: #checks for even indexes
           #     split_nodes.append(TextNode(sections[i], TextType.TEXT)) #even indexes are .TEXT type
            #else:
             #   split_nodes.append(TextNode(sections[i], text_type)) #odd indices are other text types
#        new_nodes.extend(split_nodes) #takes all elemenets from split_nodes and adds them individually to new_nodes
 #   return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
            
        for image in images:
            alt_text, url = image  # unpack the tuple
            sections = original_text.split(f"![{alt_text}]({url})", 1)
            
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
                
            if sections[0]:  # text before image
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            # Create LeafNode for image instead of TextNode
            img_node = LeafNode("img", "", {"src": url, "alt": alt_text})
            new_nodes.append(img_node)
            
            original_text = sections[1]
            
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
            
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if isinstance(old_node, LeafNode):  # Handle LeafNodes
            new_nodes.append(old_node)
            continue
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes