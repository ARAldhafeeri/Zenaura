
from zenaura.client.compiler import compiler
from .lifecycles.mount import MountLifeCycles
from zenaura.client.hyderator import Hyderator
from .error import GracefulDegenerationLifeCycleWrapper
from pyscript import document 

import traceback


class Mount(
    GracefulDegenerationLifeCycleWrapper,
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
            # hyderation steps:
            compiled_html = self.hyd_comp_compile_node(comp)

            self.hyd_rdom_attach_to_root(compiled_html)

            self.hyd_vdom_update(comp)

            self.componentDidMount(comp)

            # mount 4 : update the previous mountd page instance
            self.prev_page_instance = comp

        except Exception as e:
            self.componentDidCatchError(comp, traceback.format_exc())