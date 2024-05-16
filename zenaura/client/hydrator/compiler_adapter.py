from zenaura.client.tags import Node
from zenaura.client.page import Page
from zenaura.client.compiler import compiler
from zenaura.client.config import ZENAURA_DOM_ATTRIBUTE
from zenaura.client.component import Component
from typing import List
import io

class HydratorCompilerAdapter:
    """
        hyderator adapter for all real dom operations
        methods should start with:
        hyd_comp_
    """        
    def hyd_comp_get_keyed_uuid(
        self,
        componentId : str, 
        level : int, 
        child_index : int, 
        path : str
    ):
        """
            compiler operation : wraps compiler.getKeyedUID 
        """
        return compiler.getKeyedUID(
            componentId, 
            level, 
            child_index, 
            path
        )
    
    def hyd_comp_compile_node(
        self,
        comp: Component,
    ):
        """
            compiler operation : wraps compiler compile, returns str "HTMLElement"
            compile node
        """
        return compiler.compile(
                comp.node(), 
                componentId=comp.componentId,
                zenaura_dom_mode=True
            )
    
    def hyd_comp_compile_children(
        self,
        children: List[Node],
        componentId: str,
        zenaura_dom_mode: bool,
        path: str
    ):
        """
            compiler operation : wraps compiler compile, returns str "HTMLElement"
            compiles node children
        """
        return compiler.compile(
            children, 
            componentId=componentId,
            zenaura_dom_mode=True,
            path = path
        )
    
    def hyd_comp_compile_page(self, page: Page) -> str:
        html = io.StringIO()
        for comp in page.children:
            html.write(
                compiler.compile(
                    comp.node(), 
                    comp.componentId,
                    zenaura_dom_mode=True,
                    path=""
                )
            )
        return html.getvalue()
