# sarif-pydantic

An implementation of the [SARIF](https://sarifweb.azurewebsites.net/) (Static Analysis Results Interchange Format) format using [Pydantic](https://pydantic-docs.helpmanual.io/).

## Overview

This library provides Pydantic models for working with the SARIF specification (version 2.1.0). It enables Python developers to:

- Create, validate, and manipulate SARIF data
- Parse existing SARIF files into typed Python objects
- Export SARIF data to JSON with proper validation

## Installation

```bash
pip install sarif-pydantic
```

## Usage

### Creating a SARIF Log

```python
from sarif_pydantic import (
    ArtifactLocation, 
    Invocation, 
    Level, 
    Location, 
    Message, 
    PhysicalLocation, 
    Region, 
    Result, 
    Run, 
    Sarif, 
    Tool, 
    ToolDriver
)

# Create a tool driver
tool_driver = ToolDriver(
    name="Example Analyzer",
    version="1.0.0",
)

# Create a tool with the driver
tool = Tool(driver=tool_driver)

# Create a physical location
physical_location = PhysicalLocation(
    artifact_location=ArtifactLocation(
        uri="src/example.py",
    ),
    region=Region(
        start_line=42,
        start_column=5,
        end_line=42,
        end_column=32,
    ),
)

# Create a result
result = Result(
    rule_id="EX001",
    level=Level.WARNING,
    message=Message(
        text="Example warning message",
    ),
    locations=[Location(
        physical_location=physical_location,
    )],
)

# Create a SARIF log
sarif_log = Sarif(
    version="2.1.0",
    runs=[Run(
        tool=tool,
        invocations=[Invocation(
            execution_successful=True,
        )],
        results=[result],
    )],
)

# Export to JSON
sarif_json = sarif_log.model_dump_json(indent=2, exclude_none=True)
print(sarif_json)
```

### Loading a SARIF Log from JSON

```python
import json
from sarif_pydantic import Sarif

# Load from a file
with open("example.sarif", "r") as f:
    sarif_data = json.load(f)

# Parse into a Sarif object
sarif_log = Sarif.model_validate(sarif_data)

# Access data via typed objects
for run in sarif_log.runs:
    for result in run.results or []:
        print(f"Rule: {result.rule_id}, Level: {result.level}")
        print(f"Message: {result.message.text}")
```

## SARIF Specification

This implementation follows the [SARIF 2.1.0 specification](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html).

## License

[LICENSE]