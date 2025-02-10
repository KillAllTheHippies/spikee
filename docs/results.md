# Results Documentation

## Overview
The `results.py` module handles processing, analyzing, and reporting on test results. It supports JSONL input files and can generate Excel spreadsheets and HTML reports.

## Key Functions

### `read_jsonl_file(file_path)`
Reads a JSONL file and returns a list of dictionaries.

### `convert_results_to_excel(args)`
Converts JSONL results to Excel format. Handles special character encoding.

### `analyze_results(args)`
Analyzes results and provides detailed statistics. Can generate console output or HTML reports.

### `generate_html_report(result_file, results, total_entries, total_successes, total_failures, total_errors, attack_success_rate, breakdowns, combination_stats_sorted)`
Generates an HTML report with detailed analysis and visualizations.

## Input/Output Formats

### Input
- JSONL file format
- Each line is a JSON object with test results

### Output Formats
- Excel (.xlsx)
- HTML report
- Console output

## Analysis Metrics

### General Statistics
- Total entries
- Successful attacks
- Failed attacks
- Errors
- Attack success rate

### Breakdowns
- Jailbreak type
- Instruction type
- Task type
- Position
- Spotlighting data markers
- Injection delimiters
- Language
- Suffix ID
- Plugin

### Combinations
- Top 10 most successful combinations
- Top 10 least successful combinations

## Report Generation

### HTML Report Features
- General statistics
- Detailed breakdowns
- Combination analysis
- Responsive design
- Special character handling

## Usage Examples

```python
from results import convert_results_to_excel, analyze_results

# Convert results to Excel
convert_results_to_excel({'result_file': 'results.jsonl'})

# Analyze results with console output
analyze_results({'result_file': 'results.jsonl', 'output_format': 'console'})

# Generate HTML report
analyze_results({'result_file': 'results.jsonl', 'output_format': 'html'})
```

## Special Character Handling
The module automatically handles special characters:
- Newlines (\n)
- Carriage returns (\r)
- Tabs (\t)
- HTML entities

## Error Handling
The module includes robust error handling for:
- File I/O operations
- JSON parsing
- Data processing
- Report generation