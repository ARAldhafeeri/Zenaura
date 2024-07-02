from .common import *


def Select(
  label_text,
  attrs,
  options, 
  default_input_class="w-full p-2 border border-gray-300 rounded bg-light-white text-light-gray1 dark:text-dark-page1 hover:bg-light-green dark:bg-dark-gray2 dark:hover:bg-dark-gray1", 
  default_label_class="block mb-2 text-light-gray1 dark:text-dark-page1",
  default_wrapper_class="p-4",
  ):
  """
    Displays a form input field. 
    args:
      attrs: python dictionary trasfrom into html attributes.
      label: label_text : input label text.
      default_input_class : default input css class names
      default_label_class : default label css class names
      default_wrapper_class : default input wrapper css class names
      options: select options List[Option]
    
  """
  return Div(default_wrapper_class, [
    Builder("label").with_attribute("class", default_label_class).with_text(label_text).build(),
    Builder('select').with_attribute("class", default_input_class).with_attributes(
      **attrs
    ).with_children(*options).build(),
  ])

def Option(
  label,
  attrs,
  default_input_class="w-full p-2 border border-gray-300 rounded bg-light-white text-light-gray1 dark:text-dark-page1 hover:bg-light-green dark:bg-dark-gray2 dark:hover:bg-dark-gray1", 
  ):
  """
    Displays a form input field. 
    args:
      attrs: python dictionary trasfrom into html attributes.
      default_input_class : default input css class names
      default_label_class : default label css class names
      value : text value of option      
  """
  return Builder('option').with_attribute("class", default_input_class).with_attributes(
    **attrs
  ).with_text(label).build()
