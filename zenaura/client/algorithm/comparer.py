from zenaura.client.tags import Node, Data
from zenaura.client.compiler import compiler

from typing import List

class Comparer:
    """
        comparison step in zenaura virtual dom algorithm.
    """
    def compare(
            self,
            prevNode : Node, 
            newNode : Node, 
            level : int, 
            child_index : int, 
            componentId : str, 
            diff : List[List[any]],
            path: str
    ) -> None:
            """
                method used by search to compare attributes of parent
                node, and leaf children.
                mutate diff stack
                args:
                    prevNode: The previous component tree
                    newNode: The new component tree
                    level: The current level of the component tree
                    child_index: The index of the current child node in the component tree
                    componentId: The id of the component in virtual dom
                    path: uinque path of the component tree to identify the nodes differences
                return None
            """
            self.compare_attributes(
                 prevNode, 
                 newNode, 
                 level, 
                 child_index, 
                 componentId, 
                 diff, 
                 path
            )
            
            # check if it's children is leaf node
            # this is for instances of Data
            self.compare_children(
                 prevNode, 
                 newNode, 
                 level, 
                 child_index, 
                 componentId, 
                 diff, 
                 path
            )

    def compare_attributes(
              self, 
              prevNode, 
              newNode, 
              level, 
              child_index, 
              componentId, 
              diff, 
              path
    ):
      
        for prevNodeAttributes, newNodeAttributes in zip(prevNode.attributes, newNode.attributes):
            prevDict = prevNodeAttributes.to_dict()
            newDict = newNodeAttributes.to_dict()

            if prevDict!= newDict:
                diff.append([
                        # in mount life cycle the compiler will
                        # generate a unique id for each node using componentId
                        # then componentId-level-dependent for each child
                        # which in result generate a unique keyed ZENAURA_DOM_ATTRIBUTE 
                        compiler.getKeyedUID(componentId, level, child_index, path),
                        newNode,
                        path
                    ])
                # break the loop node will be rerendered no need to compare further.
                break

    def compare_children(
              self, 
              prevNode, 
              newNode, 
              level, 
              child_index, 
              componentId, 
              diff, 
              path
    ):
        prevNodeChildren = prevNode.children
        newNodeCHildren = newNode.children
        # if nodes has children, if they are leaf nodes of str or Data
        # compare the children and update diff stack
        if len(prevNodeChildren) and len(newNodeCHildren) == 1:
            if isinstance(prevNodeChildren[0], (Data, str)) and isinstance(newNodeCHildren[0], (Data, str)):
                diff.append([
                        compiler.getKeyedUID(
                            componentId=componentId, 
                            level=level, 
                            child_index=child_index, 
                            path=path
                        ),
                        newNode,
                        path
                    ])
