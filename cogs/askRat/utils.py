import re

def remove_xml_tags(input_string):
    """
    Removes all content enclosed in XML tags, including the tags themselves, from the input string.

    Args:
        input_string (str): The input string containing XML tags and content.

    Returns:
        str: The string with XML tags and their contents removed.
    """
    try:
        pattern = r"<[^>]+>.*?</[^>]+>|<[^/>]+/>"
        return re.sub(pattern, "", input_string, flags=re.DOTALL).strip()
    except re.error as e:
        print(f"Regex error: {e}")
        return input_string
    except Exception as e:
        print(f"Unexpected error: {e}")
        return input_string
