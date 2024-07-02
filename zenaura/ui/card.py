from zenaura.client.tags.builder import Builder

def Card(
    content,
    attrs, 
    default_class="shadow  w-64 me-2 px-2.5 py-0.5 rounded bg-light-white text-light-gray1 dark:text-dark-page1 dark:bg-dark-gray2", 
    ):
    """
      Displays a a card with content. 
      args:
        content : card content of zenaura components or elements.
        attrs: card attributes.
        default_class: default css class names.
      
    """
    return Builder("div").with_attribute("class", default_class).with_attributes(**attrs).with_children(*content).build()
