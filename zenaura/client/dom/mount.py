
from zenaura.client.compiler import compiler
from .lifecycles.mount import MountLifeCycles
from zenaura.client.hyderator import Hyderator
from .error import GracefulDegenerationLifeCycleWrapper
from pyscript import document 

import traceback


class Mount(
    GracefulDegenerationLifeCycleWrapper,
    Hyderator,
    MountLifeCycles
    ):
    def mount(self, comp  ) -> None:
        """
            Mount only Page instance to the DOM. This will allow 
            for cleaner code. Seperation of concerns.
            try : 
                - mount the component.
            except:
                - call componentDidCatchError method.
            Parameters:
            - comp: An instance of the Component class.

            Returns:
            None
        """
        # wrapped life cycle method componentDidCatchError 
        # mount steps 1-4: componentWillMount -> mount -> unmount -> componentWillUnmount -> componentDidMount
        try : 
            # mount 1: lifecycle method to be called before mounting
            self.componentWillMount(comp)

            # mount 2: mount the component to the DOM
            comp_tree = comp.node()
            compiled_comp = compiler.compile(
                comp_tree, 
                componentId=comp.componentId,
                zenaura_dom_mode=True
            )

            dom_node = document.getElementById("root") 
            dom_node.innerHTML = compiled_comp

            self.zen_dom_table[comp.componentId] = comp_tree

            self.componentDidMount(comp)

            # mount 4 : update the previous mountd page instance
            self.prev_page_instance = comp

        except Exception as e:
            self.componentDidCatchError(comp, traceback.format_exc())