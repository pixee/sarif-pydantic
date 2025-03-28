from pathlib import Path

from pydantic_sarif.sarif import (
    ArtifactLocation,
    Artifact,
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
    SarifLog,
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
    "SarifLog",
    "Tool",
    "ToolComponentReference",
    "ToolDriver",
    "load",
]


def load(path: Path | str) -> SarifLog:
    """
    Load a SARIF log from a file.

    Args:
        path (Path): The path to the SARIF log file.

    Returns:
        SarifLog: The loaded SARIF log.
    """
    return SarifLog.model_validate_json(Path(path).read_text())
