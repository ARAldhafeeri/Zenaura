# Virtual DOM Hydrator

- Virtual dom hyderator is the adapter composer single point of contact between real dom, virtual dom, compiler . Here is the planned next changes

**Attach compiled node to root** 

before :

```python
dom_node = document.getElementById("root")
dom_node.innerHTML = compiled_comp
```

after : 

```python
self.hyd_rdom_attach_to_root(page)
```

---

**compile , mount component on real dom, update virtual dom**

before :

```python
comp_tree = comp.node()
compiled_comp = compiler.compile(
    comp_tree, 
    componentId=comp.componentId,
    zenaura_dom_mode=True
)

dom_node = document.getElementById("root") 
dom_node.innerHTML = compiled_comp

self.zen_dom_table[comp.componentId] = comp_tree
```

after :

```python
# compile node
compiled_html= self.hyd_comp_compile_node(comp)
# attach node to real dom
self.hyd_rdom_attach_to_root(compiled_html)
# update virtual dom 
self.hyd_vdom_update(comp)
# set mounted 
self.prev_page_instance = comp
```

self.prev_page_instance : a breaking change coming next, where only a page can be mounted on a router, to allow for predictable structure in zenaura projects

---

**re-render mounted component differences in parent component**

before :

```python
 prevTree = self.zen_dom_table[comp.componentId]
  newTree = comp.node()
  diff = self.search(prevTree, newTree, comp.componentId)
  print(len(diff))
  while diff:
      prevNodeId, newNodeChildren, path= diff.pop()
      compiled_comp = compiler.compile(
          newNodeChildren, 
          componentId=comp.componentId,
          zenaura_dom_mode=True,
          path = path
      )
      print(prevNodeId)
      print(compiled_comp)

      foundNode = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{prevNodeId}"]')
      if foundNode:
          foundNode.outerHTML = compiled_comp
  # self.update(prevTree, prevNodeId, newNodeChildren)
  self.zen_dom_table[comp.componentId] = newTree
```

after: 

```python
while diff:
	prevNodeId, newNodeChildren, path= diff.pop()
	compiled_html = self.hyd_comp_compile_children(
		newNodeChildren, 
	  comp.componentId,
	  True,
		path
	)
	self.hyd_rdom_attach_to_mounted_comp(
		comp.componentId, 
		compiled_html
	)
	self.hyd_vdom_update(comp)
```

get keyed uuid from compiler 

before :

```python
compiled_comp = compiler.compile(
  newNodeChildren, 
  componentId=comp.componentId,
  zenaura_dom_mode=True,
  path = path
)
```

after :

```python
self.hyd_comp_get_keyed_uuid(
    componentId, 
    level, 
    child_index, 
    path
)
```

drivers should be used within the virtual dom only, for example in 

GracefulDegenerationLifeCycleWrapper

```python
class GracefulDegenerationLifeCycleWrapper(
    HydratorCompilerAdapter
):
```

part of mount, rerender we can use it here and delete compiler import