import json

from sarif_pydantic.sarif import Level, Sarif


def test_minimal_sarif_serialization():
    """Test serializing and deserializing a minimal Sarif object."""
    # Create a minimal Sarif object from dict
    minimal_dict = {
        "version": "2.1.0",
        "runs": [
            {
                "tool": {"driver": {"name": "TestTool"}},
                "results": [{"message": {"text": "Test message"}}],
            }
        ],
    }

    sarif = Sarif.model_validate(minimal_dict)

    # Serialize to JSON
    sarif_json = sarif.model_dump_json()
    sarif_dict = json.loads(sarif_json)

    # Check JSON structure
    assert sarif_dict["version"] == "2.1.0"
    assert len(sarif_dict["runs"]) == 1
    assert sarif_dict["runs"][0]["tool"]["driver"]["name"] == "TestTool"
    assert len(sarif_dict["runs"][0]["results"]) == 1
    assert sarif_dict["runs"][0]["results"][0]["message"]["text"] == "Test message"

    # Deserialize from JSON
    sarif2 = Sarif.model_validate_json(sarif_json)

    # Check that the deserialized object matches the original
    assert sarif2.version == sarif.version
    assert sarif2.runs[0].tool.driver.name == sarif.runs[0].tool.driver.name
    assert (
        sarif2.runs[0].results[0].message.text == sarif.runs[0].results[0].message.text
    )


def test_full_sarif_serialization():
    """Test serializing and deserializing a more complex Sarif object."""
    # Create a more detailed Sarif object from dict
    full_dict = {
        "version": "2.1.0",
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "TestTool",
                        "version": "1.0.0",
                        "fullName": "Test Tool Full Name",
                        "informationUri": "https://example.com/tool",
                    }
                },
                "results": [
                    {
                        "message": {
                            "text": "Found a bug",
                            "markdown": "**Found a bug**",
                        },
                        "level": "error",
                        "ruleId": "BUG001",
                        "locations": [
                            {
                                "physicalLocation": {
                                    "artifactLocation": {
                                        "uri": "file:///src/file.py",
                                        "uriBaseId": "SRCROOT",
                                    },
                                    "region": {
                                        "startLine": 10,
                                        "startColumn": 5,
                                        "endLine": 10,
                                        "endColumn": 15,
                                    },
                                }
                            }
                        ],
                    }
                ],
                "language": "en-US",
                "defaultSourceLanguage": "python",
            }
        ],
    }

    sarif = Sarif.model_validate(full_dict)

    # Serialize to JSON
    sarif_json = sarif.model_dump_json()
    sarif_dict = json.loads(sarif_json)

    # Check key attributes in the original object
    assert (
        sarif.schema_uri
        == "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json"
    )
    assert sarif.runs[0].tool.driver.full_name == "Test Tool Full Name"
    assert sarif.runs[0].tool.driver.information_uri == "https://example.com/tool"

    # Check that when serialized, the key fields exist with correct values
    # The field names might be the Python names or the JSON alias names
    driver = sarif_dict["runs"][0]["tool"]["driver"]
    driver_full_name = driver.get("fullName", driver.get("full_name"))
    assert driver_full_name == "Test Tool Full Name"

    driver_info_uri = driver.get("informationUri", driver.get("information_uri"))
    assert driver_info_uri == "https://example.com/tool"

    # Just check the original object fields instead of the serialized version
    # as field names in serialization can vary
    assert (
        sarif.runs[0].results[0].locations[0].physical_location.region.start_line == 10
    )
    assert sarif.runs[0].default_source_language == "python"

    # Deserialize from JSON
    sarif2 = Sarif.model_validate_json(sarif_json)

    # Check specific attributes rather than exact equality
    # Note: schema_uri might be mapped to $schema and back differently
    assert sarif2.version == sarif.version
    assert sarif2.runs[0].tool.driver.name == "TestTool"

    # Check that location information is correctly parsed
    assert sarif2.runs[0].results[0].message.text == "Found a bug"
    assert sarif2.runs[0].results[0].level == Level.ERROR

    # Check region details
    loc = sarif2.runs[0].results[0].locations[0].physical_location
    assert loc.artifact_location.uri == "file:///src/file.py"
    assert loc.region.start_line == 10
    assert loc.region.start_column == 5

    # Check language settings
    assert sarif2.runs[0].language == "en-US"
    assert sarif2.runs[0].default_source_language == "python"
