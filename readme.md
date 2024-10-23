# INSERT SQL Compiler Tool

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Examples](#examples)
- [License](#license)

## Project Overview

The **SQL Compiler Tool** is designed to streamline and enhance the management of process flows within your platform. It transitions from using a single, monolithic `.sql` file filled with numerous `INSERT` statements and embedded MVEL rules to a more modular and maintainable approach utilizing YAML files. These YAML definitions are compiled into a consolidated SQL file, simplifying the process of defining, validating, and managing complex SQL insertions.

## Features

- **Modular Definitions:** Define process flows and related entities using organized YAML files.
- **Flexible Mappings:** Easily map YAML definitions to different database tables.
- **Template-Based SQL Generation:** Utilize Jinja2 templates for dynamic and readable SQL statement generation.
- **Include Support:** Embed external rule files (e.g., MVEL scripts) into SQL statements seamlessly.
- **Comprehensive Validation:** Ensure YAML definitions adhere to the required schema and business rules using JSON Schema.
- **Robust Logging:** Detailed logs for tracking the compilation process and troubleshooting errors.
- **Command-Line Interface (CLI):** Flexible CLI options for specifying directories and logging verbosity.
- **Extensible Architecture:** Modular code structure facilitating easy maintenance and future enhancements.

## Directory Structure

```
project_root/
├── compile.py
├── requirements.txt
├── config/
│   ├── templates/
│   │   └── insert_template.sql
│   ├── mappings.yaml
│   └── schema.json
├── definitions/
│   ├── example_process_flow.yaml
│   └── example_task.yaml
├── includes/
│   ├── some_rule.mvel
│   ├── another_rule.mvel
│   └── task_rule.mvel
├── output/
│   └── compiled_YYYYMMDD_HHMMSS.sql
├── compilation_log/
│   └── compilation_YYYYMMDD_HHMMSS.log
├── src/
│   ├── __init__.py
│   ├── compiler.py
│   ├── config_loader.py
│   ├── logger.py
│   ├── validator.py
│   └── sql_generator.py
```

### Description of Key Directories and Files

- **`compile.py`**: The main entry point for the compiler script. Provides a CLI for compiling YAML definitions into a consolidated SQL file.
- **`requirements.txt`**: Lists all Python dependencies required to run the compiler.
- **`config/`**: Contains configuration files.
  - **`templates/`**: Holds Jinja2 SQL templates.
  - **`mappings.yaml`**: Defines mappings between YAML definitions and database tables.
  - **`schema.json`**: JSON Schema used for validating YAML definition files.
- **`definitions/`**: Stores all YAML files that define process flows and related entities.
- **`includes/`**: Contains additional files (e.g., MVEL scripts) to be included in SQL statements.
- **`output/`**: Destination for compiled SQL files, named with timestamps for versioning.
- **`compilation_log/`**: Stores logs related to the compilation process, aiding in troubleshooting.
- **`src/`**: Contains modular Python code for different components of the compiler.
  - **`compiler.py`**: Orchestrates the compilation process.
  - **`config_loader.py`**: Handles loading of configuration files.
  - **`logger.py`**: Sets up logging configurations.
  - **`validator.py`**: Validates YAML definitions against the JSON Schema.
  - **`sql_generator.py`**: Generates SQL statements from validated definitions.

## Installation

### Prerequisites

- **Python 3.6** or newer installed on your system.
- **Git** installed to clone the repository.

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/sql-compiler-tool.git
   cd sql-compiler-tool
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python -m venv .venv
   ```

3. **Activate the Virtual Environment**

   - **Windows:**

     ```bash
     .venv\Scripts\activate
     ```

   - **Unix/Linux/MacOS:**

     ```bash
     source .venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### 1. **Mappings (`config/mappings.yaml`)**

Define how YAML definitions map to your database tables.

```yaml
# config/mappings.yaml

table_mappings:
  process_flow:
    table_name: process_flows
    fields:
      id: id
      name: name
      created_at: created_at
      description: description
      rule_content: rule_content

  task:
    table_name: tasks
    fields:
      task_id: task_id
      task_name: task_name
      task_description: task_description
      task_rule: task_rule
```

### 2. **SQL Template (`config/templates/insert_template.sql`)**

Customize how SQL `INSERT` statements are generated using Jinja2 templating.

```jinja2
-- {{ metadata.comment }}
INSERT INTO {{ mappings.table_mappings[definition["table"]].table_name }} (
  {% for field in definition.fields %}
    {{ field }}{% if not loop.last %},{% endif %}
  {% endfor %}
) VALUES (
  {% for value in definition["values"] %}
    {% if value is is_string %}
      '{{ value }}'
    {% else %}
      {{ value }}
    {% endif %}
    {% if not loop.last %},{% endif %}
  {% endfor %}
);
```

### 3. **Schema Validation (`config/schema.json`)**

Ensure YAML definitions adhere to the required structure.

```json
{
  "type": "object",
  "properties": {
    "table": { "type": "string" },
    "fields": {
      "type": "array",
      "items": { "type": "string" }
    },
    "values": {
      "type": "array",
      "items": {
        "anyOf": [
          { "type": "string" },
          { "type": "number" },
          {
            "type": "object",
            "properties": {
              "include": { "type": "string" }
            },
            "required": ["include"]
          }
        ]
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "comment": { "type": "string" }
      }
    }
  },
  "required": ["table", "fields", "values"]
}
```

## Usage

### 1. **Prepare Directories**

Ensure the following directories exist in your project root:

- `config/`
- `definitions/`
- `includes/`
- `output/`
- `compilation_log/`

If they do not exist, create them:

```bash
mkdir -p config/templates definitions includes output compilation_log src tests
```

### 2. **Place Files**

- **Configuration Files (`config/`):**
  - Place `mappings.yaml`, `templates/insert_template.sql`, and `schema.json` in the `config/` directory.
  
- **Definition Files (`definitions/`):**
  - Place your YAML definition files (e.g., `example_process_flow.yaml`, `example_task.yaml`) in the `definitions/` directory.
  
- **Include Files (`includes/`):**
  - Place any files to be included in SQL statements (e.g., `some_rule.mvel`, `task_rule.mvel`) in the `includes/` directory.

### 3. **Run the Compiler**

From the project root, execute the compiler script:

```bash
python compile.py
```

#### **Additional Options:**

- **Specify Custom Directories:**

  ```bash
  python compile.py --definitions-dir my_definitions --config-dir my_config --includes-dir my_includes --output-dir my_output --log-dir my_logs
  ```

- **Enable Verbose Logging:**

  ```bash
  python compile.py --verbose
  ```

### 4. **Check Output**

The compiled SQL file will be located in the `output/` directory with a timestamped filename, such as `compiled_20231024_153045.sql`.

**Example Output (`output/compiled_YYYYMMDD_HHMMSS.sql`):**

```sql
-- Insert example process flow with rule
INSERT INTO process_flows (
  id,name,description,rule_content
) VALUES (
  1,'Example Process Flow',CURRENT_TIMESTAMP,'This is an example process flow.',
  '// some_rule.mvel

if (condition) {
    // Do something
}'
);

-- Insert sample task with rule
INSERT INTO tasks (
  task_id,task_name,task_description,task_rule
) VALUES (
  101,'Sample Task','This is a sample task.',
  '// task_rule.mvel

if (task_condition) {
    // Execute task-related logic
}'
);
```

### 5. **Review Logs**

Any errors or informational messages are logged in the `compilation_log/` directory with a timestamped filename, such as `compilation_20231024_153045.log`.

**Example Log (`compilation_log/compilation_YYYYMMDD_HHMMSS.log`):**

```
DEBUG - Mappings configuration loaded successfully.
DEBUG - Insert template loaded successfully with custom 'is_string' test.
DEBUG - Schema loaded successfully.
INFO - Starting compilation process.
DEBUG - Found 2 definition file(s) in definitions.
INFO - Processing file: definitions\example_process_flow.yaml
DEBUG - Validation successful for file: definitions\example_process_flow.yaml
DEBUG - Included content from: includes\some_rule.mvel
DEBUG - Context for template rendering: {'definition': {'table': 'process_flow', 'fields': ['id', 'name', 'description', 'rule_content'], 'values': [1, 'Example Process Flow', 'This is an example process flow.', '// some_rule.mvel\n\nif (condition) {\n    // Do something\n}']}, 'mappings': {'table_mappings': {'process_flow': {'table_name': 'process_flows', 'fields': {'id': 'id', 'name': 'name', 'description': 'description', 'rule_content': 'rule_content'}}}}, 'metadata': {'comment': 'Insert example process flow with rule'}}
DEBUG - SQL statement generated for file: definitions\example_process_flow.yaml
INFO - Processing file: definitions\example_task.yaml
DEBUG - Validation successful for file: definitions\example_task.yaml
DEBUG - Included content from: includes\task_rule.mvel
DEBUG - Context for template rendering: {'definition': {'table': 'task', 'fields': ['task_id', 'task_name', 'task_description', 'task_rule'], 'values': [101, 'Sample Task', 'This is a sample task.', '// task_rule.mvel\n\nif (task_condition) {\n    // Execute task-related logic\n}']}, 'mappings': {'table_mappings': {'process_flow': {'table_name': 'process_flows', 'fields': {'id': 'id', 'name': 'name', 'description': 'description', 'rule_content': 'rule_content'}}, 'task': {'table_name': 'tasks', 'fields': {'task_id': 'task_id', 'task_name': 'task_name', 'task_description': 'task_description', 'task_rule': 'task_rule'}}}}, 'metadata': {'comment': 'Insert sample task with rule'}}
DEBUG - SQL statement generated for file: definitions\example_task.yaml
INFO - Compiled SQL written to output\compiled_20231024_153045.sql
INFO - Compilation process completed successfully.
```

## Examples

### **1. Defining a Process Flow**

**`definitions/example_process_flow.yaml`:**

```yaml
# definitions/example_process_flow.yaml

table: process_flow
fields:
  - id
  - name
  - created_at
  - description
  - rule_content
values:
  - 1
  - 'Example Process Flow'
  - raw: CURRENT_TIMESTAMP
  - 'This is an example process flow.'
  - include: 'some_rule.mvel'
metadata:
  comment: 'Insert example process flow with rule'
```

### **2. Defining a Task**

**`definitions/example_task.yaml`:**

```yaml
# definitions/example_task.yaml

table: task
fields:
  - task_id
  - task_name
  - task_description
  - task_rule
values:
  - 101
  - 'Sample Task'
  - 'This is a sample task.'
  - include: 'task_rule.mvel'
metadata:
  comment: 'Insert sample task with rule'
```

### **3. Include Files**

- **`includes/some_rule.mvel`:**

  ```mvel
  // some_rule.mvel

  if (condition) {
      // Do something
  }
  ```

- **`includes/task_rule.mvel`:**

  ```mvel
  // task_rule.mvel

  if (task_condition) {
      // Execute task-related logic
  }
  ```

## License

This project is licensed under the [MIT License](LICENSE).
