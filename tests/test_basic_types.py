from sarif_pydantic.sarif import Artifact, ArtifactContent, ArtifactLocation, Message


def test_message_from_dict():
    # Test minimal creation
    minimal_dict = {"text": "Test message"}
    message = Message.model_validate(minimal_dict)
    assert message.text == "Test message"
    assert message.markdown is None
    assert message.id is None
    assert message.arguments is None

    # Test full creation
    full_dict = {
        "text": "Test message",
        "markdown": "**Test** message",
        "id": "MSG001",
        "arguments": ["arg1", "arg2"],
    }
    message = Message.model_validate(full_dict)
    assert message.text == "Test message"
    assert message.markdown == "**Test** message"
    assert message.id == "MSG001"
    assert message.arguments == ["arg1", "arg2"]


def test_artifact_location_from_dict():
    # Test minimal creation
    minimal_dict = {}
    location = ArtifactLocation.model_validate(minimal_dict)
    assert location.uri is None
    assert location.uri_base_id is None
    assert location.index is None
    assert location.description is None

    # Test full creation
    full_dict = {
        "uri": "file:///src/file.py",
        "uriBaseId": "SRCROOT",
        "index": 0,
        "description": {"text": "Location description"},
    }
    location = ArtifactLocation.model_validate(full_dict)
    assert location.uri == "file:///src/file.py"
    assert location.uri_base_id == "SRCROOT"
    assert location.index == 0
    assert location.description.text == "Location description"


def test_artifact_from_dict():
    # Test minimal creation
    minimal_dict = {}
    artifact = Artifact.model_validate(minimal_dict)
    assert artifact.location is None
    assert artifact.mime_type is None
    assert artifact.encoding is None
    assert artifact.source_language is None
    assert artifact.roles is None
    assert artifact.contents is None
    assert artifact.parent_index is None
    assert artifact.offset is None
    assert artifact.length is None
    assert artifact.hashes is None
    assert artifact.last_modified is None
    assert artifact.description is None

    # Test full creation
    full_dict = {
        "location": {"uri": "file:///src/file.py"},
        "mimeType": "text/python",
        "encoding": "utf-8",
        "sourceLanguage": "python",
        "roles": ["driver"],
        "contents": {"text": "print('Hello, world!')"},
        "parentIndex": 0,
        "offset": 0,
        "length": 100,
        "hashes": {"sha-256": "abcdef1234567890"},
        "description": {"text": "Artifact description"},
    }
    artifact = Artifact.model_validate(full_dict)
    assert artifact.location.uri == "file:///src/file.py"
    assert artifact.mime_type == "text/python"
    assert artifact.encoding == "utf-8"
    assert artifact.source_language == "python"
    assert artifact.roles == ["driver"]
    assert artifact.contents == ArtifactContent(text="print('Hello, world!')")
    assert artifact.parent_index == 0
    assert artifact.offset == 0
    assert artifact.length == 100
    assert artifact.hashes == {"sha-256": "abcdef1234567890"}
    assert artifact.description.text == "Artifact description"
