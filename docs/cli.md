# CLI Documentation

## Overview
The `cli.py` file contains the main command-line interface for SPIKEE (Simple Prompt Injection Kit for Evaluation and Exploitation). It provides commands for managing the workspace, generating datasets, testing against targets, and analyzing results.

## Commands

### `init`
Initializes a local SPIKEE workspace by copying default resources.

**Options:**
- `--force`: Overwrite existing directories if they exist

### `generate`
Generates a dataset from seed files.

**Options:**
- `--seed-folder`: Name of seed folder (default: 'seeds-mini-test')
- `--positions`: Positions to insert jailbreaks (start, middle, end)
- `--injection-delimiters`: Patterns for injecting payloads
- `--plugins`: List of plugins to modify text
- `--standalone_attacks`: Path to standalone_attacks.jsonl
- `--format`: Output format (full-prompt, document, burp)
- `--spotlighting-data-markers`: Data markers for document format
- `--languages`: Filter jailbreaks and instructions by language
- `--match-languages`: Only combine matching language pairs
- `--instruction-filter`: Filter instruction types
- `--jailbreak-filter`: Filter jailbreak types
- `--include-suffixes`: Include advanced suffixes
- `--include-system-message`: Include system message

### `test`
Tests a dataset against a target.

**Options:**
- `--dataset`: Path to dataset file
- `--target`: Name of target to test
- `--threads`: Number of threads (default: 4)
- `--attempts`: Attempts per payload (default: 1)
- `--success-criteria`: Success criteria (canary, boolean)
- `--resume-file`: Path to results file to resume from
- `--throttle`: Wait time between requests (seconds)

### `results`
Analyzes or converts results.

**Subcommands:**
- `analyze`: Analyze results JSONL file
  - `--result-file`: Path to results file
  - `--output-format`: Output format (console, html)
- `convert-to-excel`: Convert results to Excel
  - `--result-file`: Path to results file

### `list`
Lists available resources.

**Subcommands:**
- `seeds`: List available seed folders
- `datasets`: List available dataset files
- `targets`: List available targets
- `plugins`: List available plugins

## Usage Examples

```bash
# Initialize workspace
spikee init

# Generate dataset
spikee generate --seed-folder seeds-mini-test --format full-prompt

# Test dataset
spikee test --dataset datasets/my_dataset.jsonl --target aws_claude_35_haiku

# Analyze results
spikee results analyze --result-file results/my_results.jsonl

# List available targets
spikee list targets
```

## Notes
- The workspace initialization copies default resources from the package to the current directory
- Use `--force` with `init` to overwrite existing files
- The `generate` command supports multiple output formats for different testing scenarios