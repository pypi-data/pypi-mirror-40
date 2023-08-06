# paladin-utils
#### A small utility collection.


## Utils

### Namespace
##### A dict accessible by getattr/setattr.
Example:
```python
from paladin_util.namespace import Namespace
namespace = Namespace({
    'data': 'a'
})
print(namespace.data) #=> 'a'
namespace.data = 'b'
print(namespace.data) #=> 'b'
```

### complexrange
##### A range over the complex space

Example:
```python
from paladin_util.complexrange import complexrange
for i in complexrange((1, 32, -1), (32, 1)):
    print(i.real + i.imag)
```