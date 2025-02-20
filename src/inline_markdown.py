from textnode import TextNode, TextType
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
    new_nodes = [] #creating an empty list
    for old_node in old_nodes: #iterating through old_nodes
        if old_node.text_type != TextType.TEXT: #checks to see if the node is plain text, if it isn't it's an image or a link
            new_nodes.append(old_node) #add any image/link to the result unchanged
            continue #skips the rest of the loop if plain text is not detected
        original_text = old_node.text #get the text content from the node
        images = extract_markdown_images(original_text) #gets a list of tuples from each image in the text(alt text, url)
        if len(images) == 0: #checks for alt_text and url
            new_nodes.append(old_node) #if none found return result unchanged
            continue
        for image in images: #loop through the images in the text one at a time
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1) #splitting the text from before and after the alt_text and url into sections
            if len(sections) != 2: #check to see there is 
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "": #check to see if the section is emtpy
                new_nodes.append(TextNode(sections[0], TextType.TEXT)) #if section is not emtpy, append it to the node
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1],)) #creates the node that represents the final image from the text
            original_text = sections[1] #takes the section after the current image in the loop and make it the new text to process
        if original_text != "": #checks to see if there's more text to process
            new_nodes.append(TextNode(original_text, TextType.TEXT)) #use the saved section of text for the new loop
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = [] #creating an empty list
    for old_node in old_nodes: #iterating through old_nodes
        if old_node.text_type != TextType.TEXT: #checks to see if the node is plain text, if it isn't it's an image or a link
            new_nodes.append(old_node) #add any image/link to the result unchanged
            continue #skips the rest of the loop if no plain text is detected
        original_text = old_node.text #get the text content from the node
        links = extract_markdown_links(original_text) #gets a list of tuples from each link in the text(text, url)
        if len(links) == 0: #checks for text and url
            new_nodes.append(old_node) #if none found return result unchanged
            continue
        for link in links: #loop through the links in the text one at a time
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1) #splitting the text from before and after the text and url into sections
            if len(sections) != 2: #check to see there is 
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "": #check to see if the section is emtpy
                new_nodes.append(TextNode(sections[0], TextType.TEXT)) #if section is not emtpy, append it to the node
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1],)) #creates the node that represents the final link from the text
            original_text = sections[1] #takes the section after the current image in the loop and make it the new text to process
        if original_text != "": #checks to see if there's more text to process
            new_nodes.append(TextNode(original_text, TextType.TEXT)) #use the saved section of text for the new loop
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