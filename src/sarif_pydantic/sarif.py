from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class SarifBaseModel(BaseModel):
    """Base model for all SARIF models with camelCase field serialization/deserialization."""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        extra="allow",
    )


class Message(SarifBaseModel):
    # text is technically required by the SARIF spec, but some tools (e.g., CodeQL)
    # generate SARIF with empty message objects in relatedLocations, so we make it optional
    text: Optional[str] = None
    markdown: Optional[str] = None
    id: Optional[str] = None
    arguments: Optional[List[str]] = None
    properties: Optional[Dict[str, Any]] = None


class ArtifactLocation(SarifBaseModel):
    uri: Optional[str] = None
    uri_base_id: Optional[str] = None
    index: Optional[int] = None
    description: Optional[Message] = None
    properties: Optional[Dict[str, Any]] = None


class ArtifactContent(SarifBaseModel):
    """Represents the contents of an artifact."""

    text: Optional[str] = None
    binary: Optional[str] = None
    rendered: Optional[Message] = None
    properties: Optional[Dict[str, Any]] = None


class Region(SarifBaseModel):
    start_line: Optional[int] = None
    start_column: Optional[int] = None
    end_line: Optional[int] = None
    end_column: Optional[int] = None
    char_offset: Optional[int] = None
    char_length: Optional[int] = None
    byte_offset: Optional[int] = None
    byte_length: Optional[int] = None
    snippet: Optional[ArtifactContent] = None
    message: Optional[Message] = None
    properties: Optional[Dict[str, Any]] = None


class Artifact(SarifBaseModel):
    location: Optional[ArtifactLocation] = None
    mime_type: Optional[str] = None
    encoding: Optional[str] = None
    source_language: Optional[str] = None
    roles: Optional[List[str]] = None
    contents: Optional[ArtifactContent] = None
    parent_index: Optional[int] = None
    offset: Optional[int] = None
    length: Optional[int] = None
    hashes: Optional[Dict[str, str]] = None
    last_modified: Optional[datetime] = None
    description: Optional[Message] = None
    properties: Optional[Dict[str, Any]] = None


class Address(SarifBaseModel):
    """Represents a physical or virtual address."""

    absolute_address: Optional[int] = None
    relative_address: Optional[int] = None
    offset_from_parent: Optional[int] = None
    length: Optional[int] = None
    name: Optional[str] = None
    fully_qualified_name: Optional[str] = None
    kind: Optional[str] = None
    parent_index: Optional[int] = None
    properties: Optional[Dict[str, Any]] = None


class PhysicalLocation(SarifBaseModel):
    artifact_location: Optional[ArtifactLocation] = None
    region: Optional[Region] = None
    context_region: Optional[Region] = None
    address: Optional[Address] = None
    properties: Optional[Dict[str, Any]] = None


class LogicalLocation(SarifBaseModel):
    name: Optional[str] = None
    full_name: Optional[str] = None
    decorated_name: Optional[str] = None
    kind: Optional[str] = None
    parent_index: Optional[int] = None
    index: Optional[int] = None
    fully_qualified_name: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None


class WebRequest(SarifBaseModel):
    """Describes an HTTP request as specified by RFC 7230."""

    protocol: Optional[str] = None
    version: Optional[str] = None
    target: Optional[str] = None
    method: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    parameters: Optional[Dict[str, str]] = None
    body: Optional[ArtifactContent] = None
    properties: Optional[Dict[str, Any]] = None


class WebResponse(SarifBaseModel):
    """Describes an HTTP response as specified by RFC 7230."""

    protocol: Optional[str] = None
    version: Optional[str] = None
    status_code: Optional[int] = None
    reason_phrase: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    body: Optional[ArtifactContent] = None
    no_response_received: Optional[bool] = None
    properties: Optional[Dict[str, Any]] = None


# Forward reference for Location since we have a circular reference
class StackFrame(SarifBaseModel):
    """A function call within a stack trace."""

    location: Optional["Location"] = None
    module: Optional[str] = None
    thread_id: Optional[int] = None
    parameter: Optional[List[str]] = None
    properties: Optional[Dict[str, Any]] = None


class Stack(SarifBaseModel):
    """A call stack that is relevant to a result."""

    message: Optional[Message] = None
    frames: List[StackFrame]
    properties: Optional[Dict[str, Any]] = None


class ThreadFlowLocation(SarifBaseModel):
    """A location visited by an analysis tool in the course of simulating or monitoring code execution."""

    index: Optional[int] = None
    location: Optional["Location"] = None
    stack: Optional[Stack] = None
    kinds: Optional[List[str]] = None
    module: Optional[str] = None
    state: Optional[Dict[str, Any]] = None
    nesting_level: Optional[int] = None
    execution_order: Optional[int] = None
    execution_time_utc: Optional[datetime] = None
    importance: Optional[str] = None
    web_request: Optional[WebRequest] = None
    web_response: Optional[WebResponse] = None
    properties: Optional[Dict[str, Any]] = None


class ThreadFlow(SarifBaseModel):
    """Describes a sequence of code locations that specify a path through a single thread of execution."""

    id: Optional[str] = None
    message: Optional[Message] = None
    initial_state: Optional[Dict[str, Any]] = None
    immutable_state: Optional[Dict[str, Any]] = None
    locations: List[ThreadFlowLocation]
    properties: Optional[Dict[str, Any]] = None


class CodeFlow(SarifBaseModel):
    """Describes a set of threadFlows which together describe a pattern of code execution relevant to a result."""

    message: Optional[Message] = None
    thread_flows: List[ThreadFlow]
    properties: Optional[Dict[str, Any]] = None


class LocationRelationship(SarifBaseModel):
    """Represents a relationship between two locations."""

    target: int
    kinds: Optional[List[str]] = None
    description: Optional[Message] = None
    properties: Optional[Dict[str, Any]] = None


class Location(SarifBaseModel):
    id: Optional[int] = None
    physical_location: Optional[PhysicalLocation] = None
    logical_locations: Optional[List[LogicalLocation]] = None
    message: Optional[Message] = None
    annotations: Optional[List[Region]] = None
    relationships: Optional[List[LocationRelationship]] = None
    properties: Optional[Dict[str, Any]] = None


class ReportingDescriptorReference(SarifBaseModel):
    id: Optional[str] = None
    index: Optional[int] = None
    guid: Optional[str] = None
    tool_component: Optional[ToolComponentReference] = None
    properties: Optional[Dict[str, Any]] = None


class ReportingDescriptorRelationship(SarifBaseModel):
    """A relationship between a reporting descriptor and a related reporting descriptor."""

    target: ReportingDescriptorReference
    kinds: Optional[List[str]] = None
    description: Optional[Message] = None
    properties: Optional[Dict[str, Any]] = None


class ToolComponentReference(SarifBaseModel):
    name: Optional[str] = None
    index: Optional[int] = None
    guid: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None


class ReportingConfiguration(SarifBaseModel):
    enabled: bool = True
    level: Optional[str] = None
    rank: Optional[float] = None
    parameters: Optional[Dict[str, Any]] = None
    properties: Optional[Dict[str, Any]] = None


class ReportingDescriptor(SarifBaseModel):
    id: str
    name: Optional[str] = None
    short_description: Optional[Message] = None
    full_description: Optional[Message] = None
    default_configuration: Optional[ReportingConfiguration] = None
    help_uri: Optional[str] = None
    help: Optional[Message] = None
    relationships: Optional[List[ReportingDescriptorRelationship]] = None
    properties: Optional[Dict[str, Any]] = None


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
    properties: Optional[Dict[str, Any]] = None


class Tool(SarifBaseModel):
    driver: ToolDriver
    extensions: Optional[List[ToolComponent]] = None


class Level(str, Enum):
    NONE = "none"
    NOTE = "note"
    WARNING = "warning"
    ERROR = "error"


class Replacement(SarifBaseModel):
    """Represents a replacement of a region of bytes in a file."""

    deleted_region: Region
    inserted_content: Optional[ArtifactContent] = None
    properties: Optional[Dict[str, Any]] = None


class ArtifactChange(SarifBaseModel):
    """Describes a change to a single artifact."""

    artifact_location: ArtifactLocation
    replacements: List[Replacement]
    properties: Optional[Dict[str, Any]] = None


class Fix(SarifBaseModel):
    """Describes a proposed fix for a result."""

    description: Optional[Message] = None
    artifact_changes: List[ArtifactChange]
    properties: Optional[Dict[str, Any]] = None


class Occurrence(SarifBaseModel):
    """Represents the specific occurrence of a result within a code location."""

    physical_location: PhysicalLocation
    logical_locations: Optional[List[LogicalLocation]] = None
    message: Optional[Message] = None
    properties: Optional[Dict[str, Any]] = None


class Node(SarifBaseModel):
    """Represents a node in a graph."""

    id: str
    label: Optional[Message] = None
    location: Optional[Location] = None
    children: Optional[List[str]] = None
    properties: Optional[Dict[str, Any]] = None


class Edge(SarifBaseModel):
    """Represents a directed edge in a graph."""

    id: str
    source_node_id: str
    target_node_id: str
    label: Optional[Message] = None
    properties: Optional[Dict[str, Any]] = None


class Graph(SarifBaseModel):
    """Represents a directed graph."""

    description: Optional[Message] = None
    nodes: Optional[List[Node]] = None
    edges: Optional[List[Edge]] = None
    properties: Optional[Dict[str, Any]] = None


class EdgeTraversal(SarifBaseModel):
    """Represents the traversal of a single edge during a graph traversal."""

    edge_id: str
    final_state: Optional[Dict[str, Any]] = None
    message: Optional[Message] = None
    properties: Optional[Dict[str, Any]] = None


class GraphTraversal(SarifBaseModel):
    """Represents a path through a graph."""

    result_graph_index: Optional[int] = None
    run_graph_index: Optional[int] = None
    description: Optional[Message] = None
    edge_traversals: Optional[List[EdgeTraversal]] = None
    properties: Optional[Dict[str, Any]] = None


class Suppression(SarifBaseModel):
    """Describes a request to suppress a result."""

    kind: str
    status: Optional[str] = None
    location: Optional[Location] = None
    guid: Optional[str] = None
    justification: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None


class Attachment(SarifBaseModel):
    """An artifact relevant to a result."""

    description: Optional[Message] = None
    artifact_location: ArtifactLocation
    regions: Optional[List[Region]] = None
    rectangles: Optional[List[Dict[str, Any]]] = None  # For simplicity, keeping as Dict
    properties: Optional[Dict[str, Any]] = None


class Result(SarifBaseModel):
    rule_id: Optional[str] = None
    rule_index: Optional[int] = None
    rule: Optional[ReportingDescriptorReference] = None
    kind: Optional[str] = None
    level: Optional[Level] = None
    message: Message
    locations: Optional[List[Location]] = None
    analysis_target: Optional[ArtifactLocation] = None
    guid: Optional[str] = None
    correlation_guid: Optional[str] = None
    fixes: Optional[List[Fix]] = None
    occurrences: Optional[List[Occurrence]] = None
    partial_fingerprints: Optional[Dict[str, str]] = None
    fingerprints: Optional[Dict[str, str]] = None
    stacks: Optional[List[Stack]] = None
    code_flows: Optional[List[CodeFlow]] = None
    graphs: Optional[List[Graph]] = None
    graph_traversals: Optional[List[GraphTraversal]] = None
    related_locations: Optional[List[Location]] = None
    suppression: Optional[Suppression] = None
    rank: Optional[float] = None
    attachments: Optional[List[Attachment]] = None
    hosted_viewer_uri: Optional[str] = None
    work_item_uris: Optional[List[str]] = None
    properties: Optional[Dict[str, Any]] = None


class Invocation(SarifBaseModel):
    command_line: Optional[str] = None
    arguments: Optional[List[str]] = None
    response_files: Optional[List[ArtifactLocation]] = None
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


class Conversion(SarifBaseModel):
    """Describes how a converter transformed the output of a static analysis tool from the analysis tool's native output format into the SARIF format."""

    tool: Tool
    invocation: Optional[Invocation] = None
    analysis_tool_log_files: Optional[List[ArtifactLocation]] = None
    properties: Optional[Dict[str, Any]] = None


class VersionControlDetails(SarifBaseModel):
    """Describes a version control system (VCS)."""

    repository_uri: Optional[str] = None
    revision_id: Optional[str] = None
    branch: Optional[str] = None
    tag: Optional[str] = None
    mapping_commits: Optional[List[Dict[str, Any]]] = None
    properties: Optional[Dict[str, Any]] = None


class RunAutomationDetails(SarifBaseModel):
    """Information that describes a run's identity and role within an engineering system."""

    id: Optional[str] = None
    guid: Optional[str] = None
    correlation_guid: Optional[str] = None
    description: Optional[Message] = None
    properties: Optional[Dict[str, Any]] = None


class ToolComponent(SarifBaseModel):
    """Tool extension details."""

    name: str
    guid: Optional[str] = None
    product: Optional[str] = None
    full_name: Optional[str] = None
    version: Optional[str] = None
    semantic_version: Optional[str] = None
    rules: Optional[List[ReportingDescriptor]] = None
    notifications: Optional[List[ReportingDescriptor]] = None
    information_uri: Optional[str] = None
    download_uri: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None


class ExceptionData(SarifBaseModel):
    """Describes a runtime exception encountered during the execution of an analysis tool."""

    kind: Optional[str] = None
    message: Optional[str] = None
    stack: Optional[Stack] = None
    inner_exceptions: Optional[List["ExceptionData"]] = None
    properties: Optional[Dict[str, Any]] = None


class Notification(SarifBaseModel):
    """Describes a condition relevant to a tool's operation."""

    descriptor: Optional[ReportingDescriptorReference] = None
    associated_rule: Optional[ReportingDescriptorReference] = None
    level: Optional[Level] = None
    message: Message
    locations: Optional[List[Location]] = None
    time_utc: Optional[datetime] = None
    exception: Optional[ExceptionData] = None
    thread_id: Optional[int] = None
    properties: Optional[Dict[str, Any]] = None


class Run(SarifBaseModel):
    tool: Tool
    invocations: Optional[List[Invocation]] = None
    conversion: Optional[Conversion] = None
    language: Optional[str] = None
    version_control_provenance: Optional[List[VersionControlDetails]] = None
    original_uri_base_ids: Optional[Dict[str, ArtifactLocation]] = None
    artifacts: Optional[List[Artifact]] = None
    logical_locations: Optional[List[LogicalLocation]] = None
    graphs: Optional[List[Graph]] = None
    results: Optional[List[Result]] = None
    automation_details: Optional[RunAutomationDetails] = None
    baseline_guid: Optional[str] = None
    redaction_tokens: Optional[List[str]] = None
    default_encoding: Optional[str] = None
    default_source_language: Optional[str] = None
    newline_sequences: Optional[List[str]] = None
    notifications: Optional[List[Notification]] = None
    properties: Optional[Dict[str, Any]] = None


class ExternalPropertyFileReference(SarifBaseModel):
    """Refers to an external property file that should be merged with this run."""

    guid: Optional[str] = None
    item_count: Optional[int] = None
    location: ArtifactLocation
    properties: Optional[Dict[str, Any]] = None


class ExternalPropertyFileReferences(SarifBaseModel):
    """References to external property files that should be merged with this run."""

    conversion: Optional[ExternalPropertyFileReference] = None
    graphs: Optional[List[ExternalPropertyFileReference]] = None
    externalizedProperties: Optional[ExternalPropertyFileReference] = None
    artifacts: Optional[List[ExternalPropertyFileReference]] = None
    invocations: Optional[List[ExternalPropertyFileReference]] = None
    logical_locations: Optional[List[ExternalPropertyFileReference]] = None
    thread_flow_locations: Optional[List[ExternalPropertyFileReference]] = None
    results: Optional[List[ExternalPropertyFileReference]] = None
    taxonomies: Optional[List[ExternalPropertyFileReference]] = None
    addresses: Optional[List[ExternalPropertyFileReference]] = None
    driver: Optional[ExternalPropertyFileReference] = None
    extensions: Optional[List[ExternalPropertyFileReference]] = None
    policies: Optional[List[ExternalPropertyFileReference]] = None
    translations: Optional[List[ExternalPropertyFileReference]] = None
    web_requests: Optional[List[ExternalPropertyFileReference]] = None
    web_responses: Optional[List[ExternalPropertyFileReference]] = None
    properties: Optional[Dict[str, Any]] = None


class Sarif(SarifBaseModel):
    version: str = "2.1.0"
    schema_uri: Optional[str] = Field(None, alias="$schema")
    runs: List[Run]
    inline_external_properties: Optional[List[ExternalPropertyFileReferences]] = None
    properties: Optional[Dict[str, Any]] = None


# Update forward references for classes with circular dependencies
StackFrame.model_rebuild()
ThreadFlowLocation.model_rebuild()
ExceptionData.model_rebuild()
