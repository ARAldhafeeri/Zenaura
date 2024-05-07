from zenui.tags import Element, Child, Attribute
from typing import List
import io

class ZenuiCompiler:
    def __init__(self):
        self.attrKeyWords= {
             "styles" : "class"
        }
    def compile(self, elm : Element ):
            tag = elm.name
            if elm.name == "text":
                 return str(elm.children[0])
            children, attributes = self.split_children_attributes(elm)
            attributes = self.process_attributes(attributes)
            children = self.compile_children(children)
            return f"<{tag}{attributes}>{children if children else ''}</{tag}>"

    def split_children_attributes(self, elm : Element):
        """
            gets Element as input return children and attributes split
        """
        children = []
        attributes = []
        for i in elm.children:
              match str(i):
                    case "Element":
                        children.append(i)
                    case "Attribute":
                        attributes.append(i)
                    case _:
                        print("not matched")
        return [children, attributes]

                    
    def process_attributes(self, attrs : List[Attribute]) -> str:
        """
            return formated tags of element
        """
        s = io.StringIO()

        n = len(attrs) - 1
        for i, attr in enumerate(attrs):
            attrKey = attr.key
            if attrKey in self.attrKeyWords.keys():
                attrKey = self.attrKeyWords[attrKey]
            if i == 0 or i == n:
                s.write(f' {attrKey}="{attr.value}"')
            else:
                s.write(f'{attrKey}="{attr.value}" ')
        res = s.getvalue()
        s.close()
        return res


    def compile_children(self, children):
        """
            compiles children recuresivly
        """
        if not children:
             return
        s = io.StringIO()
        for child in children:
            s.write(self.compile(child))
        res = s.getvalue()
        s.close()
        return res