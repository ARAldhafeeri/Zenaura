
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
    async def mount(self, page: Page) -> None:
        """
            Mount only Page instance to the DOM.
            Only one page instance can be mounted at a time.
            Lifecycle:
                 server on run already hydrate all app pages and overwrite index.html
                 in App class we toggle hidden visibility 
                 in Mount we just trigger attached lifecycle. 
            try : 
                - mount the component.
            except:
                - call componentDidCatchError method.
            Parameters:
            - comp: An instance of the Component class.

            params : 
             page - zenaura page which is list of components with unique ID. 
            Returns:
            None
        """

        try :
            for comp in page.children:
                # update state in vdom
                self.hyd_vdom_update(comp)
                # trigger attached for page components
                await self.attached(comp)

        except Exception as e:
            self.componentDidCatchError(page.children[0], traceback.format_exc())