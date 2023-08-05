# dict-converter
A chain-line dict converter in Python 3
#Install
```bash
pip install dict-converter
```
# Use
```python
from dict_converter import DictConverter
a = {'a': 'a', 'b': 'b', 0: 0}
_a = DictConverter(a).add(0, lambda s: s + 1).add(['a', 'b'], str.upper).result()
_a == {'a':'A', 'b':'B', 0: 1}
```