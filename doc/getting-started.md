# Getting Started

Install
```bash
git clone https://bas-im.emcs.cornell.edu/223/si-builder.git
cd si-builder
pip install . python-dotenv
```

Verify import
```python
# ipython
import bob  # si-builder package
```

Load .env (recommended)
```python
from dotenv import load_dotenv
load_dotenv()  # reads ./.env for environment configuration
```

Minimal YAML (single Equipment)
```yaml
# file: hello-equipment.yaml
name: hello_equipment
template_class: Equipment
params:
  label: "Hello Device"
cp:
  airInlet: AirInletConnectionPoint
  airOutlet: AirOutletConnectionPoint
```

Load/validate via tests runner (recommended while authoring)
```bash
cd d:\0Programmes\Ashrae\si-builder
pytest -q -k create_from_yaml
```

Next steps
- Read Environment to configure .env.
- Read Basics to model a tiny System.
- See Syntax Operators to use >, >>, @, | shorthands.
- Use Worked Examples to mirror patterns from tests.
