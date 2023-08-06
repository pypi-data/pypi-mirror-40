# FunkPy
_FunkPy_ is a small library which is trying to bring a few well-established concepts from functional programing to Python. The package was inspired by libraries like [lodash](https://lodash.com/) and [rambdajs](http://ramdajs.com/). The monads section is modeled after [Scala](https://www.scala-lang.org/) and influenced heavily by ["Scala with Cats"](https://underscore.io/books/scala-with-cats/)

The name _FunkPy_ comes from the necessity to choose a name, which did not clash with any exiting packages. It turned out there are plenty of those around, e.g. [PyFunctional](https://github.com/EntilZha/PyFunctional) and many more abandoned projects. Moreover, there is something funky about functional programming.

[Pytoolz](https://github.com/pytoolz/toolz) is an active project which is well document and it is definitely worth having a look.

One of the main drivers to start this library was the frustrating switch to generators/iterators in Python 3.x. They can be incredibly powerful if one needs to efficiently process thousands of entries. They are less convenient when the list has just 3 items. Hence, `funkpy.Collection` was born. `Collection` provides an implementation for side-effect free operations on collections, whereas many built-in operations are anything but.

Functional programing is not complete without `curry` and `compose` methods available directly from `funkpy.uitls` or `funkpy.Collection`.

Last but not least are the glorious _functor_ and _monads_ from `funkpy.Monads`, which many people are unfamiliar with.  

_FunkPy_ is not an attempt to re-define Python. It provides simple tools for more functional way of writing code and that's it. The implementation here does not make any claims on performance. Whereas, there are no obvious problems with functional approaches in Python, wrapping millions of values in a monad each, is not the right answer, either.

# Installation
```bash
pip3 install funkpy
```

# Examples

## Collection

```python
from funkpy import Collection as _

l = [1, 2, 3]
# concatenate n lists
_.concat(l, [4, 5, 6], [7, 8, 9], 10) # => [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# append a list
_.push(l, [4, 5, 6]) # => [1, 2, 3, [4, 5, 6]]

# flatten a list of lists
_.concat(*[[1, 2, 3], [1, 2, 3]]) # => [1, 2, 3, 1, 2, 3]
# is equivalent to
_.flatten([[1, 2, 3], [1, 2, 3]]) # => [1, 2, 3, 1, 2, 3]

# It's crazy to curry and compose!
addOne = _.curry(_.strictMap)(lambda i: i+1)
addOne([1, 2, 3]) # => [2, 3, 4]

addTwo = _.compose(addOne, addOne)
addTwo([1, 2, 3]) # => [3, 4, 5]
```

## Functors and Monads
A nice introduction to _containers_ of different kinds is Professor Frisby's [Mostly Adequate Guide to Functional Programming](https://github.com/MostlyAdequate/mostly-adequate-guide). If you are looking for a fun IT book to pick, go no further. "Professor Frisby" is hilarious. 

Jokes aside, this package implements:
* generic `Functor` class with a `map` interface;
* generic `Monad` class extending `Functor` with `flatMap`;
* `Option` and `Either` monads.

## Functors
```python
from funkpy.Monads import Functor, Monad, Option, Either

# How to construct this functor thing? 
Functor(5)
# OR
Functor.of(5)

# I love mapping functors
Functor.of("Start here").map(lambda i: i+" and keep walking!")

# and some extra magic for free allows you to compare functors based 
# on the values they hold

Functor.of(5) == Functor.of(5) # => True (fingers crossed) 

```

`Functor` class is a base class which be extended to do a number of things, i.e. it is a mere template for greater things.

## Monads
```python
from funkpy.Monads import Monad, Option, Either

# This looks familiar!
my_monad = Monad.of(5)
my_monad == Monad(5) # => True

# So far so good! How about something actually useful?
my_option = Option.of({"street": "Times Ave"}) \
    .map(lambda i: i.get("postcode")) \
    .maybe("postcode not found") # => "postcode not found

# Get it? It is an option to have a value or not!"
```

# Contributors
In case someone wants to contribute to this project, for whatever reasons, here are few rules (for pylint) which differ from [Python's PEP8 style guide](https://www.python.org/dev/peps/pep-0008/):

* longer lines are ok  => `max-line-length=150`;
* but empty spaces are gone => `indent-string='  '` (double space only);
* and underscore are discouraged in function names => `function-naming-style=camelCase`;
* two spaces required inside a hanging or continued line => `indent-after-paren=2`;

The project is linked to Travis CI and every build is tested automatically.

If, heaven forbid, you got this far and found bugs, just raise tickets on GitHub!
