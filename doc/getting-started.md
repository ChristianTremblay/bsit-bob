# Getting Started

Install
```bash
git clone https://bas-im.emcs.cornell.edu/223/si-builder.git
cd si-builder
pip install .
```

Verify import
```python
# ipython
import bob  # si-builder package
```

Environment configuration
- We suggest you install python-dotenv. si-builder automatically loads a .env file in your project root if present.
- See Environment (environment.md) for available variables and their effects.

Load/validate via tests runner (recommended while authoring)
```bash
cd d:\0Programmes\Ashrae\si-builder
pytest .\tests\
```

Next steps
- Read Environment to configure .env.
- Read Basics to model a tiny System.
- See Syntax Operators to use >, >>, @, | shorthands.
- Use Worked Examples to mirror patterns from tests.
