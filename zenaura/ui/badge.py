from zenaura.client.tags.builder import Builder

def Badge(
    text,
    attrs, 
    default_class="p-2 text-xs font-medium me-2 px-2.5 py-0.5 rounded bg-light-green text-light-gray1 dark:text-dark-page1 dark:bg-dark-gray2", 
    ):
    """
      Displays a form input field. 
      args:
        text : badge text.
        attrs: span attributes.
        default_class: default css class names.
      
    """
    return Builder("span").with_text(text).with_attribute("class", default_class).with_attributes(**attrs).build()