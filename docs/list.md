# List Documentation

## Overview
The `list.py` module provides functionality to list available resources in the SPIKEE system, including seeds, datasets, targets, and plugins. It supports both local and built-in resources.

## Listing Functions

### `list_seeds(args)`
Lists local seed folders in the `datasets/` directory. A seed folder must contain `base_documents.jsonl`.

### `list_datasets(args)`
Lists `.jsonl` dataset files in the top-level `datasets/` directory.

### `list_targets(args)`
Lists both local and built-in targets:
- Local: `.py` files in the `targets/` directory
- Built-in: Modules in `spikee.targets`

### `list_plugins(args)`
Lists both local and built-in plugins:
- Local: `.py` files in the `plugins/` directory
- Built-in: Modules in `spikee.plugins`

## Resource Locations

### Local Resources
- Seeds: `datasets/<seed_folder>/`
- Datasets: `datasets/*.jsonl`
- Targets: `targets/*.py`
- Plugins: `plugins/*.py`

### Built-in Resources
- Targets: `spikee.targets.*`
- Plugins: `spikee.plugins.*`

## File Structure Requirements

### Seed Folder
Must contain:
- `base_documents.jsonl`
- `jailbreaks.jsonl`
- `instructions.jsonl`

### Target/Plugin Files
- Must be `.py` files
- Must not be `__init__.py`
- Must be in the correct directory

## Usage Examples

```python
from list import list_seeds, list_datasets, list_targets, list_plugins

# List all available seeds
list_seeds(None)

# List all available datasets
list_datasets(None)

# List all available targets
list_targets(None)

# List all available plugins
list_plugins(None)
```

## Output Format
Each listing function prints output in the following format:
```
[resource_type] Description
 - item1
 - item2
```

Example output:
```
[targets] Local targets in './targets/':
 - my_target
 - another_target

[targets] Built-in targets in spikee.targets:
 - aws_claude
 - azure_gpt