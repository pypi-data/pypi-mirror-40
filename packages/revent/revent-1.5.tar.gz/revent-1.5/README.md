# Revent

```
pip install revent
```

### subscribe events

```python
from revent import sub

@sub
def some_event_occurs(foo, bar, **others):
    foo
    bar
    blah...
```

### start listen events and run

```python
from revent import loop

# do some thing
# ...
# and

loop()
```

or auto subscribe events and run
```sh
python -m revent module_xxx module_yyy
```

