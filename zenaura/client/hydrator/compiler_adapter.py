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
        id : str, 
        key : str
    ):
        """
            compiler operation : wraps compiler.getKeyedUID 
        """
        return compiler.getKeyedUID(
            id=id, 
            key=key,
        )
    
    def hyd_comp_compile_render(
        self,
        comp: Component,
    ):
        """
            compiler operation : wraps compiler compile, returns str "HTMLElement"
            compile node
        """
        return compiler.compile(
                comp.render(), 
                id=comp.id,
                zenaura_dom_mode=True
            )
    
    def hyd_comp_compile_children(
        self,
        children: List[Node],
        id: str,
        zenaura_dom_mode: bool,
        key: str=""
    ):
        """
            compiler operation : wraps compiler compile, returns str "HTMLElement"
            compiles node children
        """
        return compiler.compile(
            children, 
            id=id,
            zenaura_dom_mode=True,
        )
    
    def hyd_comp_compile_page(self, page: Page) -> str:
        """
            compiler operation : wraps compiler compile, returns str "HTMLElement"
            compiles page children
        """
        html = io.StringIO()
        for comp in page.children:
            html.write(
                compiler.compile(
                    comp.render(), 
                    comp.id,
                    zenaura_dom_mode=True,
                )
            )
        return html.getvalue()
    
