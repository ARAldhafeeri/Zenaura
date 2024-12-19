ZENAURA_DOM_ATTRIBUTE = "data-zenaura"

# TODO add more 
allowed_tags = [
    'p', 'br', 'strong', 'em', 'b', 'i', 'u', 's', 'del', 'ins', 'sub', 'sup', 
    'ul', 'ol', 'li',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'a', 'img',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'blockquote', 'q',
    'pre', 'code', 
]

# TODO : add more
allowed_attributes = {
    '*': ['class', 'id', 'title', 'lang', 'dir', 'data-*', 'aria-*', 'role', 'py-*'], # py-* for pyscript 
    'a': ['href', 'target', 'rel'],
    'img': ['src', 'alt', 'width', 'height'],
}

self_closing_tags = [
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
     'meta', 'param', 'source', 'track', 'wbr', 'track',
]
