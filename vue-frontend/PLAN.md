# Plan for the front-end

> Note: this is subject to change

## What we want

A fully customizable user experience where the user can import their own 3d scene and assign real-time elements
as they see fit

## 5-second idea

json!

## better idea

node based editor

### Node based editor

three node types: input, modifier, output

> Note: output nodes are split into models, camera, and lights (maybe add textures later)

inputs are the keys given to the server by the `local_misc_client` (should also include constants)

modifiers are things that some how change those outputs

outputs are things that are actually in the three.js scene

# Tasks:

> Note: this list is subject to change

- [ ] store the current scene arrangement in a file
- [ ] load scene from file
- [ ] backend node parsing
- [ ] graphical node based editor


# Thinking about how to structure nodes

for now let's just pretend that they are stored in a json
TODO: how would modifiers that have multiple outputs handle their outputs

sudo example of current plan:
```json
{
    // lets say that if 'node-key' is in `general_keys` it automatically gets filled with the value from general keys
    'node-key': {
        'type': 'input',
        'output': 'whatever',
    },
    // assuming 'other-node' is not in `general_keys`
    'other-node': {
        'type': 'input',
        'output': 'a constant'
    },
    'third-node': {
        'type': 'input',
        'output': '5'
    },
    'modifier-example': {
        'type': 'modifier',
        'input': ['node-key', 'other-node'],
        'modifier': 'function-name', // lets pass the inputs as the arguments func(*modifier-example.input)
        'output': 'modifier-output' // need to decide how to send the modifier output to the output of this node
    },
    'output-example': {
        'type': 'model',
        'file-path': '/path/to/model',
        'x': 'modifier-example',
        'y': 'other-node',
        'z': 'third-node'
        // ... the rest of the attributes would also be stored here
    }
}
```

> note: a good parser would only update values that change, the one below updates everything
> which would be useful when first starting, but would be wastful when running continuously

sudo-code parser:
```python
for node in node-json:
    assert 'type' in node, "whoops, bad node"
    if node.type == 'input':
        if node in general_keys:
            node.output = general_keys[node]
    elif node.type == 'modifier':
        node.output = functions[node.modifier](node.input)
    elif node.type == 'model':
        model = load-model(node.file-path)
        for attribute in node:
            if attribute.value in node-json:
                model.attribute = node.json[attribute.value].output
        scene.add(model)

```