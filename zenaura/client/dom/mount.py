
from .lifecycles.mount import MountLifeCycles
from .error import GracefulDegenerationLifeCycleWrapper
from zenaura.client.page import Page
from zenaura.client.hydrator import HydratorRealDomAdapter
import traceback

rdom_hyd = HydratorRealDomAdapter()

class Mount(
    GracefulDegenerationLifeCycleWrapper,
    MountLifeCycles,
    ):
    async def mount(self, page: Page  ) -> None:
        """
            Mount only Page instance to the DOM.
            Only one page instance can be mounted at a time.
            Lifecycle:
            2. in-time compile html for the page components.
            3. attach compiled html to the DOM.
            4. trigger attached for page components.
            5. update state in vdom for each component.
            6. cleanup vdom from unmounted components.
            try : 
                - mount the component.
            except:
                - call componentDidCatchError method.
            Parameters:
            - comp: An instance of the Component class.

            Returns:
            None
        """

        try :
            
            compiled_html = self.hyd_comp_compile_page(page)

            self.hyd_rdom_attach_to_root(compiled_html)

            # clean up perviously mounted components :
            self.zen_dom_table.clear()

            # wait for DOMContent to be loaded 
            await rdom_hyd.hyd_rdom_wait_for_dom_content_loaded()
            # trigger attached for page components
            for comp in page.children:
                # trigger attached for page components
                self.attached(comp)
                # update state in vdom
                self.hyd_vdom_update(comp)

        except Exception as e:
            self.componentDidCatchError(page.children[0], traceback.format_exc())