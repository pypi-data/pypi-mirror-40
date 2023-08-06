# json_repository
![travis build](https://img.shields.io/travis/:mandrewcito/:json_repository.svg)
![Pypi](https://img.shields.io/pypi/v/json-repository.svg)
![Pypi - downloads month](https://img.shields.io/pypi/dm/json-repository.svg)

# Install

[https://pypi.org/project/json-repository/](Pypi)
pip install json-repository

# Examples

You can also go to [tests](test/sample/foobar_test.py) to check a good how-to !
 
## Creating custom repository 

```python
class FoobarRepository(BaseJsonRepository):
  def __init__(self):
    super(FoobarRepository, self).__init__("foo")
```

## using created repository

```python
  with FoobarRepository() as repo:
    for entity in repo.get_all():
      repo.delete(entity)
    repo.context.commit()
```
