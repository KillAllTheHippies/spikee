# Tester Documentation

## Overview
The `tester.py` module is responsible for executing tests against various targets (LLMs or guardrails). It supports parallel execution, retries, and resume capabilities.

## Key Components

### `load_target_module(target_name)`
Loads a target module from either local files or built-in packages.

### `process_entry(entry, target_module, attempts, success_criteria, max_retries, throttle)`
Processes a single test entry through the target module with retry logic.

### `test_dataset(args)`
Main test execution function that handles parallel processing and result collection.

## Test Execution Flow

1. Load target module
2. Read dataset file
3. Check for resume file (if specified)
4. Create thread pool for parallel execution
5. Process each entry through the target module
6. Handle retries and rate limits
7. Collect and save results
8. Handle interruptions gracefully

## Configuration Options

### Execution Parameters
- `target`: Target module to test against
- `threads`: Number of parallel threads
- `dataset`: Input dataset file
- `attempts`: Number of attempts per entry
- `success_criteria`: Criteria for success ('canary' or 'boolean')
- `resume_file`: File to resume from
- `throttle`: Delay between attempts

### Target Module Requirements
Each target module must implement:
- `process_input(input_text, system_message)`

## Error Handling

### Rate Limits
- Exponential backoff with random delays
- Configurable max retries

### General Errors
- Logs errors with entry ID
- Continues with next entry

### Interruptions
- Graceful shutdown on CTRL+C
- Saves partial results

## Usage Examples

```python
# Basic test execution
test_dataset({
    'target': 'aws_claude',
    'threads': 10,
    'dataset': 'dataset.jsonl',
    'attempts': 3,
    'success_criteria': 'canary',
    'throttle': 1
})

# Resume interrupted test
test_dataset({
    'target': 'azure_gpt',
    'threads': 5,
    'dataset': 'dataset.jsonl',
    'attempts': 2,
    'resume_file': 'partial_results.jsonl'
})
```

## Result Format
Results are saved in JSONL format with the following fields:
- id: Entry ID
- long_id: Full entry ID
- input: Input text
- response: Model response
- success: Test result
- attempts: Number of attempts
- task_type: Task type
- jailbreak_type: Jailbreak type
- instruction_type: Instruction type
- document_id: Document ID
- position: Position in document
- spotlighting_data_markers: Data markers
- injection_delimiters: Delimiters
- suffix_id: Suffix ID
- lang: Language
- system_message: System message
- plugin: Plugin used
- error: Error message (if any)