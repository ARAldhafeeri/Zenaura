from zenaura.client.tags import Node
from typing import List
from zenaura.client.hydrator.compiler_adapter import HydratorCompilerAdapter
from itertools import zip_longest
from .operations import *

class Searcher(
    HydratorCompilerAdapter
):
    """
    This class implements the searching step of the Zenaura virtual DOM algorithm.

    It takes two virtual DOM trees, the previous and the new one, and identifies the differences between them.
    These differences are then used to update the real DOM efficiently.

    Attributes:
        None
    """

    def updater_context_builder(self, name: str, context: dict) -> dict:
        """
        Builds the context for the updater.

        This method takes the name of the operation and its context and returns a dictionary that will be used by the updater.

        Args:
            name: The name of the operation.
            context: The context of the operation.

        Returns:
            A dictionary containing the name and context of the operation.
        """

        return {
            "name": name,
            "context": context
        }

    def patches_builder(self, prev_child_node, new_child_node, id, child_id):
        """
        Builds the patches for the updater.

        This method takes the previous and new child nodes, the component ID, and the child ID, and returns a list of patches that will be used by the updater.

        Args:
            prev_child_node: The previous child node.
            new_child_node: The new child node.
            id: The ID of the component.
            child_id: The ID of the child.

        Returns:
            A list of patches containing the operation name, the new child node, the child ID, and the context for the updater.
        """

        return [
            self.hyd_comp_get_keyed_uuid(
                id=id,
                child_id=child_id
            ),
            new_child_node,
            child_id,
            self.updater_context_builder(
                name=REMOVE_NODE,
                context={"children": prev_child_node}
            )
        ]

    def search(self, prevNode: Node, newNode: Node, id: str) -> List[List[any]]:
        """
        Searches for the differences between the previous and new virtual DOM trees.

        This method takes the previous and new virtual DOM trees and the component ID, and returns a list of lists of differences. Each difference is represented as a list containing the operation name, the new child node, the path of the child, and the context for the updater.

        Args:
            prevNode: The previous virtual DOM tree.
            newNode: The new virtual DOM tree.
            id: The ID of the component.

        Returns:
            A list of lists of differences.
        """

        # Error handling:
        if not prevNode and not newNode:
            return []
        if not isinstance(prevNode, Node) or not isinstance(newNode, Node):
            return []

        differences = []

        def helper(prev_child_node: Node, new_child_node: Node, id, prev_child_path: str, new_child_path) -> None:
            """
            Helper method for the search method.

            This method recursively compares the previous and new child nodes and their attributes and children, and adds the differences to the `differences` list.

            Args:
                prev_child_node: The previous child node.
                new_child_node: The new child node.
                id: The ID of the component.
                prev_child_path: The path of the previous child node.
                new_child_path: The path of the new child node.
            """

            nonlocal differences

            # Added node
            if not prev_child_node and new_child_node:
                differences.append([
                    self.hyd_comp_get_keyed_uuid(
                        id=id,
                        key=prev_child_path
                    ),
                    new_child_node,
                    prev_child_path,
                    self.updater_context_builder(
                        name=ADD_NODE,
                        context={"children": new_child_node}
                    )
                ])
                return

            # Removed node
            if prev_child_node and not new_child_node:
                differences.append([
                    self.hyd_comp_get_keyed_uuid(
                        id=id,
                        key=prev_child_path
                    ),
                    prev_child_node,
                    prev_child_path,
                    self.updater_context_builder(
                        name=REMOVE_NODE,
                        context={"children": prev_child_node}
                    )
                ])
                return

            # Changed child by name
            if prev_child_node.name != new_child_node.name:
                differences.append([
                    self.hyd_comp_get_keyed_uuid(
                        id=id,
                        key=prev_child_path
                    ),
                    prev_child_node,
                    prev_child_path,
                    self.updater_context_builder(
                        name=REMOVE_NODE,
                        context={"children": prev_child_node}
                    )
                ])
                differences.append([
                    self.hyd_comp_get_keyed_uuid(
                        id=id,
                        key=new_child_path
                    ),
                    new_child_node,
                    new_child_path,
                    self.updater_context_builder(
                        name=ADD_NODE,
                        context={"children": new_child_node}
                    )
                ])
                return

            # Compare attributes
            for [prev_attr, new_attr] in zip_longest(prev_child_node.attributes, new_child_node.attributes):

                # Removed attribute
                if prev_attr and not new_attr:
                    differences.append([
                        self.hyd_comp_get_keyed_uuid(
                            id=id,
                            key=prev_child_path
                        ),
                        new_child_node,
                        prev_child_path,
                        self.updater_context_builder(
                            name=REMOVE_ATTRIBUTE,
                            context={"attr_name": prev_attr.key}
                        )
                    ])
                    continue

                # Added attribute
                if not prev_attr and new_attr:
                    differences.append([
                        self.hyd_comp_get_keyed_uuid(
                            id=id,
                            key=new_child_path
                        ),
                        new_child_node,
                        new_child_path,
                        self.updater_context_builder(
                            name=ADD_ATTRIBUTE,
                            context={"attr_name": new_attr.key, "attr_value": new_attr.value}
                        )
                    ])
                    continue

                # Replaced value attribute
                if prev_attr and new_attr:
                    if prev_attr.value != new_attr.value:
                        differences.append([
                            self.hyd_comp_get_keyed_uuid(
                                id=id,
                                key=prev_child_path
                            ),
                            new_child_node,
                            prev_child_path,
                            self.updater_context_builder(
                                name=ADD_ATTRIBUTE,
                                context={"attr_name": new_attr.key, "attr_value": new_attr.value}
                            )
                        ])

            # Compare children
            for idx, (prev_child, new_child) in enumerate(zip_longest(prev_child_node.children, new_child_node.children)):
                # Leaf text nodes
                if prev_child and new_child:
                    if prev_child.is_text_node and new_child.is_text_node and (prev_child.text != new_child.text):
                        differences.append([
                            self.hyd_comp_get_keyed_uuid(
                                id=id,
                                key=prev_child_path
                            ),
                            new_child_node,
                            prev_child_path,
                            self.updater_context_builder(
                                name=NODE_INNER_TEXT,
                                context={"text": new_child.text}
                            )
                        ])
                        continue

                new_child_path = new_child.path if isinstance(new_child, Node) else ""
                prev_child_path = prev_child.path if isinstance(prev_child, Node) else ""
                helper(prev_child, new_child, id, prev_child_path=prev_child_path, new_child_path=new_child_path)

        helper(prevNode, newNode, id, 0, 0)
        return differences