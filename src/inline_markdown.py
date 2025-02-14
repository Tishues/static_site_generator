from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
        alt_text, url = images[0]
        sections = old_node.text.split(f"![{alt_text}]({url})", 1)
        split_nodes = []
        if sections[0]:
            split_nodes.append(TextNode(sections[0], TextType.TEXT))   

        split_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

        if sections[1]:
            split_nodes.append(TextNode(sections[1], TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
        text, url = links[0]
        sections = old_node.text.split(f"[{text}]({url})", 1)
        split_nodes = []
        if sections[0]:
            split_nodes.append(TextNode(sections[0], TextType.TEXT))   

        split_nodes.append(TextNode(text, TextType.LINK, url))

        if sections[1]:
            split_nodes.append(TextNode(sections[1], TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches