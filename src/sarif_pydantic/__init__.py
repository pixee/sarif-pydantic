from pathlib import Path

from sarif_pydantic.sarif import (
    Artifact,
    ArtifactLocation,
    Invocation,
    Level,
    Location,
    LogicalLocation,
    Message,
    PhysicalLocation,
    Region,
    ReportingConfiguration,
    ReportingDescriptor,
    ReportingDescriptorReference,
    Result,
    Run,
    Sarif,
    Tool,
    ToolComponentReference,
    ToolDriver,
)

__all__ = [
    "ArtifactLocation",
    "Artifact",
    "Invocation",
    "Level",
    "Location",
    "LogicalLocation",
    "Message",
    "PhysicalLocation",
    "Region",
    "ReportingConfiguration",
    "ReportingDescriptor",
    "ReportingDescriptorReference",
    "Result",
    "Run",
    "Sarif",
    "Tool",
    "ToolComponentReference",
    "ToolDriver",
    "load",
]


def load(path: Path | str) -> Sarif:
    """
    Load a SARIF log from a file.

    Args:
        path (Path): The path to the SARIF log file.

    Returns:
        Sarif: The loaded SARIF log.
    """
    return Sarif.model_validate_json(Path(path).read_text())
