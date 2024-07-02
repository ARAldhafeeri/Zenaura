from .common import *


def Popover(
  content,
  over_content,
  show=False,
  position="bottom-0"
  ):
  """
    Displays a button and popover appears when button is hovered over. 
    args:
      content : popover content
      attrs: card attributes.
      default_class: default css class names for content
      over_content: content that popover appear when overed over
      show: when user hover over over_content content card will be visible, elease will be hidden
      position: position of content to over_content, left-0, right-0, top-0, bottom-0 relative position
  """
  return Div(
      "relative",
    [
        over_content,
      Div(f"absolute z-10  {position}" + (" hidden" if not show else ""), [
        content
      ]),
    ]
    )