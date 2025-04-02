from sarif_pydantic.sarif import (
    ArtifactContent,
    Location,
    LogicalLocation,
    PhysicalLocation,
    Region,
)


def test_region_from_dict():
    # Test minimal creation
    minimal_dict = {}
    region = Region.model_validate(minimal_dict)
    assert region.start_line is None
    assert region.start_column is None
    assert region.end_line is None
    assert region.end_column is None
    assert region.char_offset is None
    assert region.char_length is None
    assert region.byte_offset is None
    assert region.byte_length is None
    assert region.snippet is None
    assert region.message is None

    # Test full creation
    full_dict = {
        "startLine": 10,
        "startColumn": 5,
        "endLine": 20,
        "endColumn": 15,
        "charOffset": 100,
        "charLength": 200,
        "byteOffset": 300,
        "byteLength": 400,
        "snippet": {"text": "code snippet"},
        "message": {"text": "Region message"},
    }

    region = Region.model_validate(full_dict)
    assert region.start_line == 10
    assert region.start_column == 5
    assert region.end_line == 20
    assert region.end_column == 15
    assert region.char_offset == 100
    assert region.char_length == 200
    assert region.byte_offset == 300
    assert region.byte_length == 400
    assert region.snippet == ArtifactContent(text="code snippet")
    assert region.message.text == "Region message"


def test_physical_location_from_dict():
    # Test minimal creation
    minimal_dict = {}
    physical_location = PhysicalLocation.model_validate(minimal_dict)
    assert physical_location.artifact_location is None
    assert physical_location.region is None
    assert physical_location.context_region is None
    assert physical_location.address is None

    # Test full creation
    full_dict = {
        "artifactLocation": {"uri": "file:///src/file.py"},
        "region": {"startLine": 10, "startColumn": 5, "endLine": 20, "endColumn": 15},
        "contextRegion": {
            "startLine": 8,
            "startColumn": 1,
            "endLine": 22,
            "endColumn": 1,
        },
        "address": {"absoluteAddress": 12345678},
    }

    physical_location = PhysicalLocation.model_validate(full_dict)
    assert physical_location.artifact_location.uri == "file:///src/file.py"
    assert physical_location.region.start_line == 10
    assert physical_location.context_region.start_line == 8
    assert physical_location.address.absolute_address == 12345678


def test_logical_location_from_dict():
    # Test minimal creation
    minimal_dict = {}
    logical_location = LogicalLocation.model_validate(minimal_dict)
    assert logical_location.name is None
    assert logical_location.full_name is None
    assert logical_location.decorated_name is None
    assert logical_location.kind is None
    assert logical_location.parent_index is None
    assert logical_location.index is None

    # Test full creation
    full_dict = {
        "name": "function_name",
        "fullName": "module.class.function_name",
        "decoratedName": "module::class::function_name()",
        "kind": "function",
        "parentIndex": 0,
        "index": 1,
    }

    logical_location = LogicalLocation.model_validate(full_dict)
    assert logical_location.name == "function_name"
    assert logical_location.full_name == "module.class.function_name"
    assert logical_location.decorated_name == "module::class::function_name()"
    assert logical_location.kind == "function"
    assert logical_location.parent_index == 0
    assert logical_location.index == 1


def test_location_from_dict():
    # Test minimal creation
    minimal_dict = {}
    location = Location.model_validate(minimal_dict)
    assert location.id is None
    assert location.physical_location is None
    assert location.logical_locations is None
    assert location.message is None
    assert location.annotations is None
    assert location.relationships is None

    # Test full creation
    full_dict = {
        "id": 1,
        "physicalLocation": {
            "artifactLocation": {"uri": "file:///src/file.py"},
            "region": {"startLine": 10, "startColumn": 5},
        },
        "logicalLocations": [
            {"name": "function_name", "fullName": "module.function_name"}
        ],
        "message": {"text": "Location message"},
        "annotations": [],
        "relationships": [],
    }

    location = Location.model_validate(full_dict)
    assert location.id == 1
    assert location.physical_location.artifact_location.uri == "file:///src/file.py"
    assert location.logical_locations[0].name == "function_name"
    assert location.message.text == "Location message"
    assert location.annotations == []
    assert location.relationships == []
