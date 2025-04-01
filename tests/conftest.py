import pytest

from sarif_pydantic.sarif import (
    ArtifactLocation,
    Level,
    Location,
    Message,
    PhysicalLocation,
    Region,
    ReportingDescriptor,
    Result,
    Run,
    Sarif,
    Tool,
    ToolDriver,
)


@pytest.fixture
def minimal_sarif():
    """Create a minimal valid Sarif object."""
    tool_driver = ToolDriver(name="TestTool")
    tool = Tool(driver=tool_driver)
    run = Run(tool=tool)
    return Sarif(version="2.1.0", runs=[run])


@pytest.fixture
def sarif_with_result():
    """Create a Sarif object with a single result."""
    tool_driver = ToolDriver(name="TestTool")
    tool = Tool(driver=tool_driver)
    message = Message(text="Test result")
    result = Result(message=message)
    run = Run(tool=tool, results=[result])
    return Sarif(version="2.1.0", runs=[run])


@pytest.fixture
def sarif_with_location():
    """Create a Sarif object with a result that has location information."""
    tool_driver = ToolDriver(name="TestTool")
    tool = Tool(driver=tool_driver)

    artifact_location = ArtifactLocation(uri="file:///src/file.py")
    region = Region(startLine=10, startColumn=5, endLine=10, endColumn=15)
    physical_location = PhysicalLocation(
        artifactLocation=artifact_location, region=region
    )
    location = Location(physicalLocation=physical_location)

    message = Message(text="Test result with location")
    result = Result(
        message=message,
        level=Level.ERROR,
        locations=[location],
    )

    run = Run(tool=tool, results=[result])
    return Sarif(version="2.1.0", runs=[run])


@pytest.fixture
def sarif_with_rule():
    """Create a Sarif object with a result that references a rule."""
    rule = ReportingDescriptor(
        id="RULE001",
        name="TestRule",
        shortDescription=Message(text="Test rule short description"),
        fullDescription=Message(text="Test rule full description"),
    )

    tool_driver = ToolDriver(name="TestTool", rules=[rule])
    tool = Tool(driver=tool_driver)

    message = Message(text="Test result with rule")
    result = Result(
        message=message,
        ruleId="RULE001",
        ruleIndex=0,
    )

    run = Run(tool=tool, results=[result])
    return Sarif(version="2.1.0", runs=[run])
