# DOM

- refactor algorithm into multiple steps see ./algorithm
- Dom diffing algorithm optimization

**Problem :** 

- in Node class, nodeId get regenerated in every re-render , hard to keep track of.

Solution :

- Instead of relying on nodeId, I have cut short the uuid  + unique path to each node.
- This will achieve the desired dynamic programming goal to keep track of the component change state.
- The compiler and the search step in the virtual dom do the same step to reconstruct identity for each node, I call this new algorithm “ keyed UUIDs”

```python
for idx, child in enumerate(elm.children):
    if  isinstance(child, Node):
        path += f"{level}{idx}"
        html += self.compile(
            child, 
            id, 
            zenaura_dom_mode=zenaura_dom_mode,
            level=level,
            child_index=child_index,
            path=path
        )
        child_index += idx
        level += 1
  # constructing the path recursivly uuid.parent.child.child.child......n
```

same in search step in the dom which passes the pass to the compare step:

```python
for idx, [prevNodeChild, newNodeChild] in enumerate(zip(prevNode.children, newNode.children)):
    # search and diff each child node
    path += f"{level}{idx}"
    helper(
        prevNodeChild, 
        newNodeChild, 
        level, 
        child_index,
        path
    )
    child_index += 1
    level += 1
```

# Tags

- remove HTMLTags, rename it as Builder