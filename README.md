```python
                               /00           /00
                              | 00          | 00
 /000000/0000   /000000   /0000000  /000000 | 00
| 00_  00_  00 /00__  00 /00__  00 /00__  00| 00
| 00 \ 00 \ 00| 00  \ 00| 00  | 00| 00000000| 00
| 00 | 00 | 00| 00  | 00| 00  | 00| 00_____/| 00
| 00 | 00 | 00|  000000/|  0000000|  0000000| 00
|__/ |__/ |__/ \______/  \_______/ \_______/|__/
```

# About

`model` is the [typedsystem](https://github.com/typedsystem) approach to composite types, through the so-called _models_. In few words: 

1. A _model_ is a type with _typed fields_.
2. To each model is assigned a _schema_, which is a dictionary whose values are types.
3. Each _schema_ can be _unwrapped_ to a conventional dictionary.

```
Model --schema-> Schema --unwrap-> Dict
```

# Install

For the stable version:

```bash
pip install typedsystem-model
```

For the dev version:

```bash
pip install git+https://github.com/typedsystem/model  
```

# Docs

See [typedsystem.com](https://typedsystem.com).
