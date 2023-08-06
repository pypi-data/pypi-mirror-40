# metabeyond - metadata utilities for modern Python code

A small set of utilities for writing self-documenting code, and for allowing introspection of metadata applied 
using decorators at runtime in a similar fashion to Java 6 annotation interfaces. This entire module is heavily
influenced by Java 6 annotations such as the following nonsensical example:

```java
@Configuration
@FunctionalInterface
@SafeForSpeedsNotExceeding( value = 1.15572735, units = ATTOPARSECS_PER_MICROFORTNIGHT) 
public class QuantumDecoherenceStabilizer {
    @Haiku 
    public void checkNodes() { 
        if (tree.hasAnyRealLeafNodes()) { 
            freshenLeavesOn(tree); 
        } 
    }
}
```

thus providing the following Python solution:

```python
@Configuration()
@FunctionalInterface()
@SafeForSpeedsNotExceeding(value=1.15572735, units=ATTOPARSECS_PER_MICROFORTNIGHT)
class QuantumDecoherenceStabilizer:
    @haiku
    def check_nodes(self) -> str:
        if tree.has_any_real_leaf_nodes():
            freshen_leaves_on(tree)
```

(See the [Google Annotation Gallery](https://code.google.com/archive/p/gag/) for more esoteric annotation examples!) 

## Hints

Hints are designed to add some description to a docstring for utilities such as Sphinx. The idea behind using
this as a decorator is that decorators are often much more visible to the reader than text in docstrings, so 
it is a simple way to exploit readability. Apart from manipulating the docstring, no reference to this decorator
is ever actually kept. It is essentially transparent.

- Definition of a hint:

```python
from metabeyond import hints


haiku = hints.Hint('This is designed to be poetic to read.')
```

- Applying a hint. **Hints never have parenthesis after their name in a decoration.**

```python
@haiku
def basho():
    """old pond"""
    frog.leap() in water
    sound()
```

- This provides the following effect:

```python
>>> import inspect
>>> get_docstring = lambda o: inspect.cleandoc(inspect.getdoc(o))

>>> print(get_docstring(basho))
old pond

This is designed to be poetic to read.
```

## Remarks

Remarks are the next step up from hints and are designed to register themselves unto a class or function to be detected
later. This is akin to how Java 6 annotations work.

- Defining a remark

```python
from metabeyond import remarks

class Bean(remarks.Remark):
    """Marks the object as a bean."""
```

- Applying a remark. **Remarks always have parenthesis. Failure to add parenthesis will result in the decorated item
  being replaced by the decorator that would otherwise be called, which will cause any dependant code to break, so don't
  try it.**

```python
@Bean()
def bar():
    return 69  # lol
```

- We may provide more complex definitions with validation constraints on the decorated element, or with
  attributes specific to each decoration. See the documentation for a full explanation, but the following gives you
  the general idea. This example defines a route decorator similar to what is provided by 
  [flask](http://flask.pocoo.org/). Applying it to a class will result in a failure. 
  
```python
class Route(remarks.Remark, constraint=inspect.isfunction):
    def __init__(self, route):
        self.route = route


@Route('/about-me')
def about_me():
    ...
```

- Inspecting any applied remarks is also pretty easy.

```python
>>> from metabeyond import remarks

>>> remarks.get_remark(Route, about_me)
Route(route='/about_me')
```

Other methods for searching and querying in various ways can be found in the documentation.
