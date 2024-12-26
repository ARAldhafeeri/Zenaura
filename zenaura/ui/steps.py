from .tags import tag 
from zenaura.client.tags import Node

def Steps(
    steps: list,
    current: int = 0,
    direction: str = "horizontal",
    class_: str = "",
    **attrs
) -> Node:
    """
    A steps component for visualizing a step-by-step workflow.

    Args:
        steps (list): List of step names or titles.
        current (int): Index of the current active step.
        direction (str): Layout direction ('horizontal' or 'vertical').
        class_ (str): Tailwind classes for styling.
        **attrs: Additional attributes.

    Returns:
        Node: The steps container.
    """
    direction_class = "flex" if direction == "horizontal" else "flex-col"
    step_items = []
    for i, step in enumerate(steps):
        step_class = (
            "text-blue-500 font-bold"
            if i == current
            else "text-gray-500"
        )
        step_items.append(
            tag("div", step, class_=f"step-item {step_class}")
        )
        if i < len(steps) - 1:
            step_items.append(
                tag("div", "|", class_="mx-2 text-gray-400")
                if direction == "horizontal"
                else tag("div", "", class_="h-4 border-l border-gray-400 mx-auto")
            )

    return tag(
        "div",
        *step_items,
        class_=f"{direction_class} items-center {class_}",
        **attrs
    )
