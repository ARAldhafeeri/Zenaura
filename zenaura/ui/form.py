from zenaura.client.tags.builder import Builder


def Form(
    attrs,
    fields,
    on_submit,
    default_form_styles="w-full p-2 border border-gray-300 rounded bg-light-white text-light-gray1 dark:text-dark-page1 hover:bg-light-green dark:bg-dark-gray2 dark:hover:bg-dark-gray1", 
    ):
    """
      Displays a form input field. 
      args:
        attrs: python dictionary trasfrom into html attributes.
        default_form_styles : default input css class names for form
        fields: list of zenaura input fields or custom elements
      
    """
    return Builder("form").with_attribute("class", default_form_styles).with_attributes(**attrs).with_children(*fields).with_attribute("py-submit", on_submit).build()
