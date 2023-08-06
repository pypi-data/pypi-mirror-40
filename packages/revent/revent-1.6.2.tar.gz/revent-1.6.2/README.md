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

### optional environment variable

```
URL_REDIS="redis://[:PASSWORD@]REDIS_HOST[:6379][/DB_INDEX]"
URL_REDIS="redis://:xxxx@redis.host:12345/2"
```
