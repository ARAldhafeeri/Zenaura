
from zenaura.client.compiler import compiler
from .lifecycles.mount import MountLifeCycles
from .lookup import LookupTable
from .error import GracefulDegenerationLifeCycleWrapper
from pyscript import document 

import traceback


class Mount(
    GracefulDegenerationLifeCycleWrapper,
    LookupTable,
    MountLifeCycles
    ):
    def mount(self, comp  ) -> None:
        """
            Mount the component, goes through the life cycle methods and mounts the component to the DOM.
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

            # mount 3: lifecycle method the component will be unmountted
            # assign the component id to the mounted component id
            self.unmount(self.prev_component_instance)

            # mount 4 : lifecycle method to be called after mounting
            self.mounted_component_id = comp.componentId

        
            self.componentDidMount(comp)

        except Exception as e:
            self.componentDidCatchError(comp, traceback.format_exc())