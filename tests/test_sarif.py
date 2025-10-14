from uuid import UUID

from sarif_pydantic.sarif import Run, Sarif


def test_run_from_dict():
    # Test minimal creation with required fields
    minimal_dict = {"tool": {"driver": {"name": "TestTool"}}}
    run = Run.model_validate(minimal_dict)
    assert run.tool.driver.name == "TestTool"
    assert run.invocations is None
    assert run.conversion is None
    assert run.language is None
    assert run.version_control_provenance is None
    assert run.original_uri_base_ids is None
    assert run.artifacts is None
    assert run.logical_locations is None
    assert run.graphs is None
    assert run.results is None
    assert run.automation_details is None
    assert run.baseline_guid is None
    assert run.redaction_tokens is None
    assert run.default_encoding is None
    assert run.default_source_language is None
    assert run.newline_sequences is None
    assert run.notifications is None
    assert run.properties is None

    # Test creation with all fields
    full_dict = {
        "tool": {
            "driver": {
                "name": "TestTool",
                "version": "1.0.0",
                "rules": [{"id": "RULE001", "name": "TestRule"}],
            }
        },
        "invocations": [{"executionSuccessful": True}],
        "conversion": {"tool": {"driver": {"name": "Converter"}}},
        "language": "en-US",
        "versionControlProvenance": [
            {"repositoryUri": "https://github.com/example/repo"}
        ],
        "originalUriBaseIds": {"SRCROOT": {"uri": "file:///src/"}},
        "artifacts": [{"location": {"uri": "file:///src/file.py"}}],
        "logicalLocations": [{"name": "function_name"}],
        "graphs": [],
        "results": [{"message": {"text": "Result message"}, "ruleId": "RULE001"}],
        "automationDetails": {"id": "TEST-ID-123"},
        "baselineGuid": "12345678-1234-5678-1234-567812345678",
        "redactionTokens": ["SECRET"],
        "defaultEncoding": "utf-8",
        "defaultSourceLanguage": "python",
        "newlineSequences": ["\n", "\r\n"],
        "toolExtensions": [],
        "notifications": [],
        "properties": {"key": "value"},
    }

    run = Run.model_validate(full_dict)

    assert run.tool.driver.name == "TestTool"
    assert run.invocations[0].execution_successful is True
    assert run.conversion.tool.driver.name == "Converter"
    assert run.language == "en-US"
    assert (
        run.version_control_provenance[0].repository_uri
        == "https://github.com/example/repo"
    )
    assert run.original_uri_base_ids["SRCROOT"].uri == "file:///src/"
    assert run.artifacts[0].location.uri == "file:///src/file.py"
    assert run.logical_locations[0].name == "function_name"
    assert run.graphs == []
    assert run.results[0].message.text == "Result message"
    assert run.automation_details.id == "TEST-ID-123"
    assert run.baseline_guid == "12345678-1234-5678-1234-567812345678"
    assert run.redaction_tokens == ["SECRET"]
    assert run.default_encoding == "utf-8"
    assert run.default_source_language == "python"
    assert run.newline_sequences == ["\n", "\r\n"]
    assert run.notifications == []
    assert run.properties == {"key": "value"}


def test_sarif_from_dict():
    # Test minimal creation with required fields
    minimal_dict = {
        "version": "2.1.0",
        "runs": [{"tool": {"driver": {"name": "TestTool"}}}],
    }

    sarif = Sarif.model_validate(minimal_dict)

    assert sarif.version == "2.1.0"
    assert sarif.schema_uri is None
    assert len(sarif.runs) == 1
    assert sarif.runs[0].tool.driver.name == "TestTool"
    assert sarif.inline_external_properties is None
    assert sarif.properties is None

    # Test full creation
    full_dict = {
        "version": "2.1.0",
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "runs": [{"tool": {"driver": {"name": "TestTool"}}}],
        "inlineExternalProperties": [],
        "properties": {"key": "value"},
    }

    sarif = Sarif.model_validate(full_dict)

    assert sarif.version == "2.1.0"
    assert (
        sarif.schema_uri
        == "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json"
    )
    assert len(sarif.runs) == 1
    assert sarif.runs[0].tool.driver.name == "TestTool"
    assert sarif.inline_external_properties == []
    assert sarif.properties == {"key": "value"}


def test_sarif_with_multiple_runs_from_dict():
    """Test creating a Sarif object with multiple runs."""
    multi_run_dict = {
        "version": "2.1.0",
        "runs": [
            {"tool": {"driver": {"name": "Tool1"}}},
            {"tool": {"driver": {"name": "Tool2"}}},
        ],
    }

    sarif = Sarif.model_validate(multi_run_dict)

    assert len(sarif.runs) == 2
    assert sarif.runs[0].tool.driver.name == "Tool1"
    assert sarif.runs[1].tool.driver.name == "Tool2"
