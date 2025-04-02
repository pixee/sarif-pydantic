from datetime import datetime, timezone

from sarif_pydantic.sarif import ArtifactLocation, Invocation


def test_invocation_from_dict():
    # Test minimal creation with required fields
    minimal_dict = {"executionSuccessful": True}
    invocation = Invocation.model_validate(minimal_dict)
    assert invocation.execution_successful is True
    assert invocation.command_line is None
    assert invocation.arguments is None
    assert invocation.response_files is None
    assert invocation.start_time_utc is None
    assert invocation.end_time_utc is None
    assert invocation.machine is None
    assert invocation.account is None
    assert invocation.process_id is None
    assert invocation.executable_location is None
    assert invocation.working_directory is None
    assert invocation.environment_variables is None
    assert invocation.stdin is None
    assert invocation.stdout is None
    assert invocation.stderr is None
    assert invocation.stdout_stderr is None
    assert invocation.properties is None

    # Test creation with all fields
    start_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    end_time = datetime(2023, 1, 1, 12, 1, 0, tzinfo=timezone.utc)

    full_dict = {
        "commandLine": "pylint src/",
        "arguments": ["--rcfile=.pylintrc", "src/"],
        "responseFiles": [{"uri": "file:///project/.pylintrc"}],
        "startTimeUtc": start_time.isoformat(),
        "endTimeUtc": end_time.isoformat(),
        "executionSuccessful": True,
        "machine": "test-machine",
        "account": "test-user",
        "processId": 12345,
        "executableLocation": {"uri": "file:///usr/bin/pylint"},
        "workingDirectory": {"uri": "file:///project"},
        "environmentVariables": {"PYTHONPATH": "/project", "ENV": "test"},
        "stdin": {"uri": "file:///project/stdin.txt"},
        "stdout": {"uri": "file:///project/stdout.txt"},
        "stderr": {"uri": "file:///project/stderr.txt"},
        "stdoutStderr": {"uri": "file:///project/stdout_stderr.txt"},
        "properties": {"exitCode": 0},
    }

    invocation = Invocation.model_validate(full_dict)

    assert invocation.command_line == "pylint src/"
    assert invocation.arguments == ["--rcfile=.pylintrc", "src/"]
    assert invocation.response_files == [
        ArtifactLocation(uri="file:///project/.pylintrc")
    ]
    assert invocation.start_time_utc == start_time
    assert invocation.end_time_utc == end_time
    assert invocation.execution_successful is True
    assert invocation.machine == "test-machine"
    assert invocation.account == "test-user"
    assert invocation.process_id == 12345
    assert invocation.executable_location.uri == "file:///usr/bin/pylint"
    assert invocation.working_directory.uri == "file:///project"
    assert invocation.environment_variables == {"PYTHONPATH": "/project", "ENV": "test"}
    assert invocation.stdin.uri == "file:///project/stdin.txt"
    assert invocation.stdout.uri == "file:///project/stdout.txt"
    assert invocation.stderr.uri == "file:///project/stderr.txt"
    assert invocation.stdout_stderr.uri == "file:///project/stdout_stderr.txt"
    assert invocation.properties == {"exitCode": 0}
