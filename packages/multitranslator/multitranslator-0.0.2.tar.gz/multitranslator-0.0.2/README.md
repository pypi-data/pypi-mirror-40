# MultiTranslator
Multi Translator python package, for fun.

[![image](https://img.shields.io/pypi/v/multitranslator.svg)](https://pypi.org/project/multitranslator/)
[![image](https://img.shields.io/pypi/l/multitranslator.svg)](https://pypi.org/project/multitranslator/)
[![image](https://img.shields.io/pypi/pyversions/multitranslator.svg)](https://pypi.org/project/multitranslator/)
[![image](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/GreatBahram)

-----------------------------------
##  Installation
```bash
pip install multitranslator
```

## Usage
it's very easy and joyable.

```python
from multitranslator.translators import Cambridge, MultiTranslator

cambridge = Cambridge()

cambridge.translate('home')

print(cambridge.to_dict())
```
