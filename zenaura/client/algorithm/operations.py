# UPDATER ALGORITHM OPERATION AND CONTEXT

ADD_NODE = "ADD_NODE"
"""
{
    name : "ADD_NODE",
    context: {
        "children" : child-node,
    }
}
"""
REMOVE_NODE = "REMOVE_NODE"
"""
{
    name : "REMOVE_NODE",
    context: {
        "children" : child-node,
    }
}
"""
NODE_INNER_TEXT = "NODE_INNER_TEXT"
"""
{
    name : "NODE_INNER_TEXT",
    context: {
        "text" : "sanitized-text",
    }
}
"""

# attributes operations
ADD_ATTRIBUTE = "ADD_ATTRIBUTE"
"""
{
    name : "ADD_ATTRIBUTE",
    context: {
        "attr_name" : "attr-name",
        "attr_value" : "attr-value",
    }
}
"""
REMOVE_ATTRIBUTE = "REMOVE_ATTRIBUTE"
"""
{
    name : "REMOVE_ATTRIBUTE",
    context: {
        "attr_name" : "attr-name",
    }
}
"""
REPLACE_ATTRIBUTE = "REPLACE_ATTRIBUTE"
"""
{
    name : "REPLACE_ATTRIBUTE",
    context: {
        "attr_name" : "attr-name",
        "attr_value" : "attr-value",
    }
}
"""
