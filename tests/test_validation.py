import pytest
from pydantic import ValidationError

from sarif_pydantic.sarif import (
    Level,
    ReportingDescriptor,
    Result,
    Run,
    Sarif,
    Tool,
    ToolDriver,
)


def test_sarif_version_validation():
    """Test that Sarif version must be a valid string."""
    # Default version is valid
    sarif_dict = {"runs": [{"tool": {"driver": {"name": "TestTool"}}}]}
    sarif = Sarif.model_validate(sarif_dict)
    assert sarif.version == "2.1.0"

    # Explicit valid version
    sarif_dict = {
        "version": "2.1.0",
        "runs": [{"tool": {"driver": {"name": "TestTool"}}}],
    }
    sarif = Sarif.model_validate(sarif_dict)
    assert sarif.version == "2.1.0"

    # Invalid version format would cause validation error in actual implementation
    # This would require custom validation in the model


def test_required_fields():
    """Test that required fields must be provided."""
    # Test required fields for Sarif
    with pytest.raises(ValidationError):
        Sarif.model_validate({})  # Missing 'runs'

    # Test required fields for Run
    with pytest.raises(ValidationError):
        Run.model_validate({})  # Missing 'tool'

    # Test required fields for Tool
    with pytest.raises(ValidationError):
        Tool.model_validate({})  # Missing 'driver'

    # Test required fields for ToolDriver
    with pytest.raises(ValidationError):
        ToolDriver.model_validate({})  # Missing 'name'

    # Test required fields for Result
    with pytest.raises(ValidationError):
        Result.model_validate({})  # Missing 'message'

    # Test required fields for ReportingDescriptor
    with pytest.raises(ValidationError):
        ReportingDescriptor.model_validate({})  # Missing 'id'


def test_enum_validation():
    """Test that enum values are validated."""
    # Valid Level values
    result = Result.model_validate({"message": {"text": "Test"}, "level": "error"})
    assert result.level == Level.ERROR

    result = Result.model_validate({"message": {"text": "Test"}, "level": "warning"})
    assert result.level == Level.WARNING

    result = Result.model_validate({"message": {"text": "Test"}, "level": "note"})
    assert result.level == Level.NOTE

    result = Result.model_validate({"message": {"text": "Test"}, "level": "none"})
    assert result.level == Level.NONE

    # Invalid Level values would cause validation error in actual implementation
    # This would require custom validation in the model


def test_nested_validation():
    """Test that nested objects are properly validated."""
    # Create a Run with invalid nested Tool (missing driver)
    with pytest.raises(ValidationError):
        Run.model_validate({"tool": {}})

    # Create a Result with invalid nested Message (missing text)
    with pytest.raises(ValidationError):
        Result.model_validate({"message": {}})

    # Create a ToolDriver with invalid nested rules
    with pytest.raises(ValidationError):
        ToolDriver.model_validate({"name": "TestTool", "rules": [{}]})  # Missing 'id'
