from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Message(BaseModel):
    text: str
    markdown: Optional[str] = None
    id: Optional[str] = None
    arguments: Optional[List[str]] = Field(default=None)


class ArtifactLocation(BaseModel):
    uri: Optional[str] = None
    uri_base_id: Optional[str] = Field(None, alias="uriBaseId")
    index: Optional[int] = None
    description: Optional[Message] = None


class Region(BaseModel):
    start_line: Optional[int] = Field(None, alias="startLine")
    start_column: Optional[int] = Field(None, alias="startColumn")
    end_line: Optional[int] = Field(None, alias="endLine")
    end_column: Optional[int] = Field(None, alias="endColumn")
    char_offset: Optional[int] = Field(None, alias="charOffset")
    char_length: Optional[int] = Field(None, alias="charLength")
    byte_offset: Optional[int] = Field(None, alias="byteOffset")
    byte_length: Optional[int] = Field(None, alias="byteLength")
    snippet: Optional[Any] = None
    message: Optional[Message] = None


class Artifact(BaseModel):
    location: Optional[ArtifactLocation] = None
    mime_type: Optional[str] = Field(None, alias="mimeType")
    encoding: Optional[str] = None
    source_language: Optional[str] = Field(None, alias="sourceLanguage")
    roles: Optional[List[str]] = None
    contents: Optional[Any] = None
    parent_index: Optional[int] = Field(None, alias="parentIndex")
    offset: Optional[int] = None
    length: Optional[int] = None
    hashes: Optional[Dict[str, str]] = None
    last_modified: Optional[datetime] = Field(None, alias="lastModified")
    description: Optional[Message] = None


class PhysicalLocation(BaseModel):
    artifact_location: Optional[ArtifactLocation] = Field(None, alias="artifactLocation")
    region: Optional[Region] = None
    context_region: Optional[Region] = Field(None, alias="contextRegion")
    address: Optional[Any] = None


class LogicalLocation(BaseModel):
    name: Optional[str] = None
    full_name: Optional[str] = Field(None, alias="fullName")
    decorated_name: Optional[str] = Field(None, alias="decoratedName")
    kind: Optional[str] = None
    parent_index: Optional[int] = Field(None, alias="parentIndex")
    index: Optional[int] = None


class Location(BaseModel):
    id: Optional[int] = None
    physical_location: Optional[PhysicalLocation] = Field(None, alias="physicalLocation")
    logical_locations: Optional[List[LogicalLocation]] = Field(None, alias="logicalLocations")
    message: Optional[Message] = None
    annotations: Optional[List[Any]] = None
    relationships: Optional[List[Any]] = None


class ReportingDescriptorReference(BaseModel):
    id: Optional[str] = None
    index: Optional[int] = None
    guid: Optional[UUID] = None
    tool_component: Optional[Any] = Field(None, alias="toolComponent")


class ToolComponentReference(BaseModel):
    name: Optional[str] = None
    index: Optional[int] = None
    guid: Optional[UUID] = None


class ReportingConfiguration(BaseModel):
    enabled: bool = True
    level: Optional[str] = None
    rank: Optional[float] = None
    parameters: Optional[Dict[str, Any]] = None


class ReportingDescriptor(BaseModel):
    id: str
    name: Optional[str] = None
    short_description: Optional[Message] = Field(None, alias="shortDescription")
    full_description: Optional[Message] = Field(None, alias="fullDescription")
    default_configuration: Optional[ReportingConfiguration] = Field(None, alias="defaultConfiguration")
    help_uri: Optional[str] = Field(None, alias="helpUri")
    help: Optional[Message] = None
    relationships: Optional[List[Any]] = None


class ToolDriver(BaseModel):
    name: str
    full_name: Optional[str] = Field(None, alias="fullName")
    version: Optional[str] = None
    semantic_version: Optional[str] = Field(None, alias="semanticVersion")
    information_uri: Optional[str] = Field(None, alias="informationUri")
    rules: Optional[List[ReportingDescriptor]] = None
    notifications: Optional[List[ReportingDescriptor]] = None
    taxa: Optional[List[ReportingDescriptor]] = None
    language: Optional[str] = None
    contents: Optional[List[str]] = None


class Tool(BaseModel):
    driver: ToolDriver
    extensions: Optional[List[Any]] = None


class Level(str, Enum):
    NONE = "none"
    NOTE = "note"
    WARNING = "warning"
    ERROR = "error"


class Result(BaseModel):
    rule_id: Optional[str] = Field(None, alias="ruleId")
    rule_index: Optional[int] = Field(None, alias="ruleIndex")
    rule: Optional[ReportingDescriptorReference] = None
    kind: Optional[str] = None
    level: Optional[Level] = None
    message: Message
    locations: Optional[List[Location]] = None
    analysis_target: Optional[ArtifactLocation] = Field(None, alias="analysisTarget")
    fixes: Optional[List[Any]] = None
    occurrences: Optional[List[Any]] = None
    stacks: Optional[List[Any]] = None
    code_flows: Optional[List[Any]] = Field(None, alias="codeFlows")
    graphs: Optional[List[Any]] = None
    graph_traversals: Optional[List[Any]] = Field(None, alias="graphTraversals")
    related_locations: Optional[List[Location]] = Field(None, alias="relatedLocations")
    suppression: Optional[Any] = None
    rank: Optional[float] = None
    attachments: Optional[List[Any]] = None
    hosted_viewer_uri: Optional[str] = Field(None, alias="hostedViewerUri")
    work_item_uris: Optional[List[str]] = Field(None, alias="workItemUris")
    properties: Optional[Dict[str, Any]] = None


class Invocation(BaseModel):
    command_line: Optional[str] = Field(None, alias="commandLine")
    arguments: Optional[List[str]] = None
    response_files: Optional[List[Any]] = Field(None, alias="responseFiles")
    start_time_utc: Optional[datetime] = Field(None, alias="startTimeUtc")
    end_time_utc: Optional[datetime] = Field(None, alias="endTimeUtc")
    execution_successful: bool = Field(..., alias="executionSuccessful")
    machine: Optional[str] = None
    account: Optional[str] = None
    process_id: Optional[int] = Field(None, alias="processId")
    executable_location: Optional[ArtifactLocation] = Field(None, alias="executableLocation")
    working_directory: Optional[ArtifactLocation] = Field(None, alias="workingDirectory")
    environment_variables: Optional[Dict[str, str]] = Field(None, alias="environmentVariables")
    stdin: Optional[ArtifactLocation] = None
    stdout: Optional[ArtifactLocation] = None
    stderr: Optional[ArtifactLocation] = None
    stdout_stderr: Optional[ArtifactLocation] = Field(None, alias="stdoutStderr")
    properties: Optional[Dict[str, Any]] = None


class Run(BaseModel):
    tool: Tool
    invocations: Optional[List[Invocation]] = None
    conversion: Optional[Any] = None
    language: Optional[str] = None
    version_control_provenance: Optional[List[Any]] = Field(None, alias="versionControlProvenance")
    original_uri_base_ids: Optional[Dict[str, Any]] = Field(None, alias="originalUriBaseIds")
    artifacts: Optional[List[Artifact]] = None
    logical_locations: Optional[List[LogicalLocation]] = Field(None, alias="logicalLocations")
    graphs: Optional[List[Any]] = None
    results: Optional[List[Result]] = None
    automation_details: Optional[Any] = Field(None, alias="automationDetails")
    baseline_guid: Optional[UUID] = Field(None, alias="baselineGuid")
    redaction_tokens: Optional[List[str]] = Field(None, alias="redactionTokens")
    default_encoding: Optional[str] = Field(None, alias="defaultEncoding")
    default_source_language: Optional[str] = Field(None, alias="defaultSourceLanguage")
    newline_sequences: Optional[List[str]] = Field(None, alias="newlineSequences")
    tool_extensions: Optional[List[Any]] = Field(None, alias="toolExtensions")
    notifications: Optional[List[Any]] = None
    properties: Optional[Dict[str, Any]] = None


class SarifLog(BaseModel):
    version: str = "2.1.0"
    schema_uri: Optional[str] = Field(None, alias="$schema")
    runs: List[Run]
    inline_external_properties: Optional[List[Any]] = Field(None, alias="inlineExternalProperties")
    properties: Optional[Dict[str, Any]] = None
