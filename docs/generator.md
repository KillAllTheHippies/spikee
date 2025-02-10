# Generator Documentation

## Overview
The `generator.py` module is responsible for creating datasets by combining base documents with jailbreaks and instructions. It supports multiple output formats and includes a plugin system for text modification.

## Key Functions

### `generate_dataset(args)`
Main entry point for dataset generation. Handles:
- Loading and filtering input files
- Applying plugins
- Generating variations
- Writing output files
- Printing statistics

### `generate_variations(base_docs, jailbreaks, instructions, positions, injection_delimiters, spotlighting_data_markers_list, plugins, adv_suffixes=None, output_format='full-prompt', match_languages=False, system_message_config=None)`
Generates dataset variations by combining documents with jailbreaks and instructions.

### `load_plugins(plugin_names)`
Loads plugins from local or built-in locations.

### `apply_plugin(plugin_module, text)`
Applies a plugin's transform function to text.

### `process_standalone_attacks(standalone_attacks, dataset, entry_id, output_format='full-prompt')`
Processes standalone attacks and adds them to the dataset.

## Data Structures

### Base Document
```json
{
  "id": "unique_id",
  "document": "text content",
  "question": "optional question",
  "ideal_answer": "optional answer",
  "ideal_summary": "optional summary"
}
```

### Jailbreak
```json
{
  "id": "unique_id",
  "text": "jailbreak text",
  "canary": "detection string",
  "jailbreak_type": "type identifier",
  "lang": "language code"
}
```

### Instruction
```json
{
  "id": "unique_id",
  "instruction": "instruction text",
  "canary": "detection string",
  "instruction_type": "type identifier",
  "lang": "language code"
}
```

## Plugin System
Plugins can modify jailbreak text. They must:
1. Be placed in the `plugins/` directory
2. Have a `.py` extension
3. Implement a `transform(text)` function

Example plugin:
```python
def transform(text):
    return text.upper()
```

## Configuration Options

### Output Formats
- `full-prompt`: Complete prompts with instructions
- `document`: Modified documents only
- `burp`: Burp Suite compatible format

### Injection Positions
- `start`: Beginning of document
- `middle`: Middle of document
- `end`: End of document

### System Messages
Configured in `system_messages.toml`:
```toml
[configurations]
spotlighting_data_markers = "marker"
system_message = "message"
```

## Usage Example
```python
from generator import generate_dataset

args = {
    'seed_folder': 'seeds-mini-test',
    'format': 'full-prompt',
    'positions': ['start', 'end'],
    'plugins': ['uppercase']
}

generate_dataset(args)