from uuid import UUID

from sarif_pydantic.sarif import Level, Result


def test_level_enum():
    assert Level.NONE == "none"
    assert Level.NOTE == "note"
    assert Level.WARNING == "warning"
    assert Level.ERROR == "error"


def test_result_from_dict():
    # Test minimal creation with required fields
    minimal_dict = {"message": {"text": "Result message"}}

    result = Result.model_validate(minimal_dict)
    assert result.message.text == "Result message"
    assert result.rule_id is None
    assert result.rule_index is None
    assert result.rule is None
    assert result.kind is None
    assert result.level is None
    assert result.locations is None
    assert result.analysis_target is None
    assert result.guid is None
    assert result.correlation_guid is None
    assert result.fixes is None
    assert result.occurrences is None
    assert result.stacks is None
    assert result.code_flows is None
    assert result.graphs is None
    assert result.graph_traversals is None
    assert result.related_locations is None
    assert result.suppression is None
    assert result.rank is None
    assert result.attachments is None
    assert result.hosted_viewer_uri is None
    assert result.work_item_uris is None
    assert result.properties is None

    # Test creation with all fields
    full_dict = {
        "ruleId": "RULE001",
        "ruleIndex": 0,
        "rule": {"id": "RULE001", "index": 0},
        "kind": "fail",
        "level": "error",
        "message": {"text": "Result message"},
        "locations": [
            {
                "id": 1,
                "physicalLocation": {
                    "artifactLocation": {"uri": "file:///src/file.py"},
                    "region": {"startLine": 10, "startColumn": 5},
                },
            }
        ],
        "analysisTarget": {"uri": "file:///src/file.py"},
        "guid": "11111111-1111-1111-1111-111111111111",
        "correlationGuid": "22222222-2222-2222-2222-222222222222",
        "fixes": [],
        "occurrences": [],
        "stacks": [],
        "codeFlows": [],
        "graphs": [],
        "graphTraversals": [],
        "relatedLocations": [
            {
                "id": 2,
                "physicalLocation": {
                    "artifactLocation": {"uri": "file:///src/related.py"},
                    "region": {"startLine": 20, "startColumn": 15},
                },
            }
        ],
        "suppression": {"kind": "inSource", "status": "accepted"},
        "rank": 95.0,
        "attachments": [],
        "hostedViewerUri": "https://example.com/viewer",
        "workItemUris": ["https://example.com/issue/123"],
        "properties": {"key": "value"},
    }

    result = Result.model_validate(full_dict)

    assert result.rule_id == "RULE001"
    assert result.rule_index == 0
    assert result.rule.id == "RULE001"
    assert result.kind == "fail"
    assert result.level == Level.ERROR
    assert result.message.text == "Result message"
    assert len(result.locations) == 1
    assert result.locations[0].id == 1
    assert result.analysis_target.uri == "file:///src/file.py"
    assert result.guid == "11111111-1111-1111-1111-111111111111"
    assert result.correlation_guid == "22222222-2222-2222-2222-222222222222"
    assert result.fixes == []
    assert result.occurrences == []
    assert result.stacks == []
    assert result.code_flows == []
    assert result.graphs == []
    assert result.graph_traversals == []
    assert len(result.related_locations) == 1
    assert result.related_locations[0].id == 2
    assert result.suppression.kind == "inSource"
    assert result.suppression.status == "accepted"
    assert result.rank == 95.0
    assert result.attachments == []
    assert result.hosted_viewer_uri == "https://example.com/viewer"
    assert result.work_item_uris == ["https://example.com/issue/123"]
    assert result.properties == {"key": "value"}
