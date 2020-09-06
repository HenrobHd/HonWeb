import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from markdown2 import Markdown

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))

def list_entries_html():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("encyclopedia/templates/encyclopedia")
    return list(sorted(re.sub(r"\.html$", "", filename)
                for filename in filenames if filename.endswith(".html")))

def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def save_entry_html(title, content):
    link_patterns = [
            # Match a wiki page link LikeThis.
        (re.compile(r"(\b[A-Z][a-z]+[A-Z]\w+\b)"), r"/\1")
    ]
    markdowner = Markdown(extras=["link-patterns"],
                               link_patterns=link_patterns)
    content = markdowner.convert(content)
    content = "{% extends 'encyclopedia/greet.html' %}{% block element %}" + content + "{% endblock %}"
    filename = f"encyclopedia/templates/encyclopedia/{title}.html"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def delete_entry(title):
    filename = f"entries/{title}.md"
    default_storage.delete(filename)

def delete_entry_html(title):
    filename = f"encyclopedia/templates/encyclopedia/{title}.html"
    default_storage.delete(filename)

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def get_entry_html(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"encyclopedia/templates/encyclopedia/{title}.html")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
