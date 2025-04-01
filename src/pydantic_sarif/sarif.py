from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class SarifBaseModel(BaseModel):
    """Base model for all SARIF models with camelCase field serialization/deserialization."""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )


class Message(SarifBaseModel):
    text: str
    markdown: Optional[str] = None
    id: Optional[str] = None
    arguments: Optional[List[str]] = None


class ArtifactLocation(SarifBaseModel):
    uri: Optional[str] = None
    uri_base_id: Optional[str] = None
    index: Optional[int] = None
    description: Optional[Message] = None


class Region(SarifBaseModel):
    start_line: Optional[int] = None
    start_column: Optional[int] = None
    end_line: Optional[int] = None
    end_column: Optional[int] = None
    char_offset: Optional[int] = None
    char_length: Optional[int] = None
    byte_offset: Optional[int] = None
    byte_length: Optional[int] = None
    snippet: Optional[Any] = None
    message: Optional[Message] = None


class Artifact(SarifBaseModel):
    location: Optional[ArtifactLocation] = None
    mime_type: Optional[str] = None
    encoding: Optional[str] = None
    source_language: Optional[str] = None
    roles: Optional[List[str]] = None
    contents: Optional[Any] = None
    parent_index: Optional[int] = None
    offset: Optional[int] = None
    length: Optional[int] = None
    hashes: Optional[Dict[str, str]] = None
    last_modified: Optional[datetime] = None
    description: Optional[Message] = None


class PhysicalLocation(SarifBaseModel):
    artifact_location: Optional[ArtifactLocation] = None
    region: Optional[Region] = None
    context_region: Optional[Region] = None
    address: Optional[Any] = None


class LogicalLocation(SarifBaseModel):
    name: Optional[str] = None
    full_name: Optional[str] = None
    decorated_name: Optional[str] = None
    kind: Optional[str] = None
    parent_index: Optional[int] = None
    index: Optional[int] = None


class Location(SarifBaseModel):
    id: Optional[int] = None
    physical_location: Optional[PhysicalLocation] = None
    logical_locations: Optional[List[LogicalLocation]] = None
    message: Optional[Message] = None
    annotations: Optional[List[Any]] = None
    relationships: Optional[List[Any]] = None


class ReportingDescriptorReference(SarifBaseModel):
    id: Optional[str] = None
    index: Optional[int] = None
    guid: Optional[UUID] = None
    tool_component: Optional[Any] = None


class ToolComponentReference(SarifBaseModel):
    name: Optional[str] = None
    index: Optional[int] = None
    guid: Optional[UUID] = None


class ReportingConfiguration(SarifBaseModel):
    enabled: bool = True
    level: Optional[str] = None
    rank: Optional[float] = None
    parameters: Optional[Dict[str, Any]] = None


class ReportingDescriptor(SarifBaseModel):
    id: str
    name: Optional[str] = None
    short_description: Optional[Message] = None
    full_description: Optional[Message] = None
    default_configuration: Optional[ReportingConfiguration] = None
    help_uri: Optional[str] = None
    help: Optional[Message] = None
    relationships: Optional[List[Any]] = None


class ToolDriver(SarifBaseModel):
    name: str
    full_name: Optional[str] = None
    version: Optional[str] = None
    semantic_version: Optional[str] = None
    information_uri: Optional[str] = None
    rules: Optional[List[ReportingDescriptor]] = None
    notifications: Optional[List[ReportingDescriptor]] = None
    taxa: Optional[List[ReportingDescriptor]] = None
    language: Optional[str] = None
    contents: Optional[List[str]] = None


class Tool(SarifBaseModel):
    driver: ToolDriver
    extensions: Optional[List[Any]] = None


class Level(str, Enum):
    NONE = "none"
    NOTE = "note"
    WARNING = "warning"
    ERROR = "error"


class Result(SarifBaseModel):
    rule_id: Optional[str] = None
    rule_index: Optional[int] = None
    rule: Optional[ReportingDescriptorReference] = None
    kind: Optional[str] = None
    level: Optional[Level] = None
    message: Message
    locations: Optional[List[Location]] = None
    analysis_target: Optional[ArtifactLocation] = None
    fixes: Optional[List[Any]] = None
    occurrences: Optional[List[Any]] = None
    stacks: Optional[List[Any]] = None
    code_flows: Optional[List[Any]] = None
    graphs: Optional[List[Any]] = None
    graph_traversals: Optional[List[Any]] = None
    related_locations: Optional[List[Location]] = None
    suppression: Optional[Any] = None
    rank: Optional[float] = None
    attachments: Optional[List[Any]] = None
    hosted_viewer_uri: Optional[str] = None
    work_item_uris: Optional[List[str]] = None
    properties: Optional[Dict[str, Any]] = None


class Invocation(SarifBaseModel):
    command_line: Optional[str] = None
    arguments: Optional[List[str]] = None
    response_files: Optional[List[Any]] = None
    start_time_utc: Optional[datetime] = None
    end_time_utc: Optional[datetime] = None
    execution_successful: bool
    machine: Optional[str] = None
    account: Optional[str] = None
    process_id: Optional[int] = None
    executable_location: Optional[ArtifactLocation] = None
    working_directory: Optional[ArtifactLocation] = None
    environment_variables: Optional[Dict[str, str]] = None
    stdin: Optional[ArtifactLocation] = None
    stdout: Optional[ArtifactLocation] = None
    stderr: Optional[ArtifactLocation] = None
    stdout_stderr: Optional[ArtifactLocation] = None
    properties: Optional[Dict[str, Any]] = None


class Run(SarifBaseModel):
    tool: Tool
    invocations: Optional[List[Invocation]] = None
    conversion: Optional[Any] = None
    language: Optional[str] = None
    version_control_provenance: Optional[List[Any]] = None
    original_uri_base_ids: Optional[Dict[str, Any]] = None
    artifacts: Optional[List[Artifact]] = None
    logical_locations: Optional[List[LogicalLocation]] = None
    graphs: Optional[List[Any]] = None
    results: Optional[List[Result]] = None
    automation_details: Optional[Any] = None
    baseline_guid: Optional[UUID] = None
    redaction_tokens: Optional[List[str]] = None
    default_encoding: Optional[str] = None
    default_source_language: Optional[str] = None
    newline_sequences: Optional[List[str]] = None
    tool_extensions: Optional[List[Any]] = None
    notifications: Optional[List[Any]] = None
    properties: Optional[Dict[str, Any]] = None


class Sarif(SarifBaseModel):
    version: str = "2.1.0"
    schema_uri: Optional[str] = Field(None, alias="$schema")
    runs: List[Run]
    inline_external_properties: Optional[List[Any]] = None
    properties: Optional[Dict[str, Any]] = None
