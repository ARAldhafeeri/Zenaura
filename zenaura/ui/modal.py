from .common import *


def Modal(content, close_btn, show_modal=False, class_names="shadow z-40 rounded bg-light-white text-light-gray1 dark:text-dark-page1 dark:bg-dark-gray2"):
  """
  Creates a modal component with given content.
  
  args:
      content: Content to be displayed inside the modal, typically a Component.
      show_modal: Boolean to control the visibility of the modal.
      close_btn: Button to close modal when it's open
      class_names : Default class names
  """
  attrs = {"open": "", "class": class_names} if show_modal else {}
  modal_content = Dialog([
    content,
    close_btn,
  ], attrs)
  
  return modal_content