from zenaura.client.tags.builder import Builder
from .common import Div

def Input(
  label_text,
  attrs, 
  default_input_class="w-full p-2 border border-gray-300 rounded bg-light-white text-light-gray1 dark:text-dark-page1 hover:bg-light-green dark:bg-dark-gray2 dark:hover:bg-dark-gray1", 
  default_label_class="block mb-2 text-light-gray1 dark:text-dark-page1",
  default_wrapper_class="p-4"
  ):
  """
    Displays a form input field. 
    args:
      attrs: python dictionary trasfrom into html attributes.
      label: label_text : input label text.
      default_input_class : default input css class names
      default_label_class : default label css class names
      default_wrapper_class : default input wrapper css class names
    
  """
  return Div(default_wrapper_class, [
    Builder("label").with_attribute("class", default_label_class).with_text(label_text).build(),
    Builder('input').with_attribute("class", default_input_class).with_attributes(
      **attrs
    ).build(),
  ])