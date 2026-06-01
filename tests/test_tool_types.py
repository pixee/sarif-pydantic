from uuid import UUID

from sarif_pydantic.sarif import (
    ReportingConfiguration,
    ReportingDescriptor,
    ReportingDescriptorReference,
    Tool,
    ToolComponent,
    ToolComponentReference,
    ToolDriver,
)


def test_reporting_descriptor_reference_from_dict():
    # Test minimal creation
    minimal_dict = {}
    ref = ReportingDescriptorReference.model_validate(minimal_dict)
    assert ref.id is None
    assert ref.index is None
    assert ref.guid is None
    assert ref.tool_component is None

    # Test full creation
    full_dict = {
        "id": "RULE001",
        "index": 0,
        "guid": "12345678-1234-5678-1234-567812345678",
        "toolComponent": {"name": "TestTool"},
    }

    ref = ReportingDescriptorReference.model_validate(full_dict)
    assert ref.id == "RULE001"
    assert ref.index == 0
    assert ref.guid == "12345678-1234-5678-1234-567812345678"
    assert ref.tool_component == ToolComponentReference(name="TestTool")


def test_tool_component_reference_from_dict():
    # Test minimal creation
    minimal_dict = {}
    ref = ToolComponentReference.model_validate(minimal_dict)
    assert ref.name is None
    assert ref.index is None
    assert ref.guid is None

    # Test full creation
    full_dict = {
        "name": "TestComponent",
        "index": 0,
        "guid": "12345678-1234-5678-1234-567812345678",
    }

    ref = ToolComponentReference.model_validate(full_dict)
    assert ref.name == "TestComponent"
    assert ref.index == 0
    assert ref.guid == "12345678-1234-5678-1234-567812345678"


def test_reporting_configuration_from_dict():
    # Test minimal creation
    minimal_dict = {}
    config = ReportingConfiguration.model_validate(minimal_dict)
    assert config.enabled is True
    assert config.level is None
    assert config.rank is None
    assert config.parameters is None

    # Test full creation
    full_dict = {
        "enabled": False,
        "level": "warning",
        "rank": 75.5,
        "parameters": {"key": "value"},
    }

    config = ReportingConfiguration.model_validate(full_dict)
    assert config.enabled is False
    assert config.level == "warning"
    assert config.rank == 75.5
    assert config.parameters == {"key": "value"}


def test_reporting_descriptor_from_dict():
    # Test minimal creation with required fields
    minimal_dict = {"id": "RULE001"}

    descriptor = ReportingDescriptor.model_validate(minimal_dict)
    assert descriptor.id == "RULE001"
    assert descriptor.name is None
    assert descriptor.short_description is None
    assert descriptor.full_description is None
    assert descriptor.default_configuration is None
    assert descriptor.help_uri is None
    assert descriptor.help is None
    assert descriptor.relationships is None

    # Test full creation
    full_dict = {
        "id": "RULE001",
        "name": "TestRule",
        "shortDescription": {"text": "Short description"},
        "fullDescription": {"text": "Full description"},
        "defaultConfiguration": {"enabled": True, "level": "warning"},
        "helpUri": "https://example.com/help",
        "help": {"text": "Help message"},
        "relationships": [],
    }

    descriptor = ReportingDescriptor.model_validate(full_dict)

    assert descriptor.id == "RULE001"
    assert descriptor.name == "TestRule"
    assert descriptor.short_description.text == "Short description"
    assert descriptor.full_description.text == "Full description"
    assert descriptor.default_configuration.level == "warning"
    assert descriptor.help_uri == "https://example.com/help"
    assert descriptor.help.text == "Help message"
    assert descriptor.relationships == []


def test_tool_driver_from_dict():
    # Test minimal creation with required fields
    minimal_dict = {"name": "TestTool"}

    driver = ToolDriver.model_validate(minimal_dict)
    assert driver.name == "TestTool"
    assert driver.full_name is None
    assert driver.version is None
    assert driver.semantic_version is None
    assert driver.information_uri is None
    assert driver.rules is None
    assert driver.notifications is None
    assert driver.taxa is None
    assert driver.language is None
    assert driver.contents is None

    # Test full creation
    full_dict = {
        "name": "TestTool",
        "fullName": "Test Tool Full Name",
        "version": "1.0.0",
        "semanticVersion": "1.0.0",
        "informationUri": "https://example.com/tool",
        "rules": [{"id": "RULE001", "name": "TestRule"}],
        "notifications": [{"id": "NOTIF001", "name": "TestNotification"}],
        "taxa": [{"id": "TAXA001", "name": "TestTaxa"}],
        "language": "en-US",
        "contents": ["localizedData", "nonLocalizedData"],
    }

    driver = ToolDriver.model_validate(full_dict)

    assert driver.name == "TestTool"
    assert driver.full_name == "Test Tool Full Name"
    assert driver.version == "1.0.0"
    assert driver.semantic_version == "1.0.0"
    assert driver.information_uri == "https://example.com/tool"
    assert driver.rules[0].id == "RULE001"
    assert driver.notifications[0].id == "NOTIF001"
    assert driver.taxa[0].id == "TAXA001"
    assert driver.language == "en-US"
    assert driver.contents == ["localizedData", "nonLocalizedData"]


def test_tool_from_dict():
    # Test minimal creation with required fields
    minimal_dict = {"driver": {"name": "TestTool"}}

    tool = Tool.model_validate(minimal_dict)
    assert tool.driver.name == "TestTool"
    assert tool.extensions is None

    # Test full creation
    full_dict = {
        "driver": {
            "name": "TestTool",
            "version": "1.0.0",
            "rules": [{"id": "RULE001"}],
        },
        "extensions": [{"name": "TestExtension"}],
    }

    tool = Tool.model_validate(full_dict)
    assert tool.driver.name == "TestTool"
    assert tool.driver.version == "1.0.0"
    assert tool.driver.rules[0].id == "RULE001"
    assert tool.extensions == [ToolComponent(name="TestExtension")]
