#!/usr/bin/env python

""" Tests for the deploy module, which is used to configure and execute Overwatch scripts.

.. codeauthor:: Raymond Ehlers <raymond.ehlers@yale.edu>, Yale University
"""

from future.utils import iteritems

import pytest
import copy
import os
try:
    # For whatever reason, import StringIO from io doesn't behave nicely in python 2.
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import signal
import stat
import inspect
import subprocess
import collections
import pkg_resources
import logging
logger = logging.getLogger(__name__)

import ruamel.yaml as yaml

from overwatch.base import deploy

def testExpandEnvironmentVars(loggingMixin):
    """ Test the YAML constructor to expand environment vars. """
    testYaml = """
    normalVar: 3
    normalWithDollarSign: "$ Hello World"
    environmentVar: !expandVars $HOME
    expandedWithoutVar: !expandVars "Hello world"
    """
    # Setup the YAML to be read from a stream
    s = StringIO()
    s.write(testYaml)
    s.seek(0)

    config = deploy.configModule.yaml.load(s, Loader = yaml.SafeLoader)

    assert config["normalVar"] == 3
    # Should have no impact because it explicitly needs to be tagged (a `$` on it's own is not enough)
    assert config["normalWithDollarSign"] == "$ Hello World"
    assert config["environmentVar"] == os.environ["HOME"]
    # Should have no impact because there are no environment ars
    assert config["expandedWithoutVar"] == "Hello world"

def testRetrieveExecutable(loggingMixin):
    """ Tests for retrieving executables. """
    e = deploy.retrieveExecutable("zodb", config = {})
    assert isinstance(e, deploy._available_executables["zodb"])

    with pytest.raises(KeyError) as exceptionInfo:
        e = deploy.retrieveExecutable("helloWorld", config = {})
    assert exceptionInfo.value.args[0] == "Executable helloWorld is invalid."

#: Simple named tuple to contain the execution expectations.
executableExpected = collections.namedtuple("executableExpected", ["name", "description", "args", "config"])

@pytest.fixture
def setupBasicExecutable(loggingMixin, mocker):
    """ Setup an executable object.

    Returns:
        tuple: (executable, expected) where executable is an executable object and expected are the expected
            parameters.
    """
    # Mock folder creation. We want to make it a noop so we don't make a bunch of random empty folders.
    mMakedirs = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.os.makedirs", mMakedirs)

    expected = {
        "name": "{label}Executable",
        "description": "Basic executable for {label}ing",
        "args": ["execTest", "arg1", "arg2", "test{hello}"],
        "config": {"hello": "world", "label": "test"},
    }
    executable = deploy.executable(**expected)

    for k in ["name", "description"]:
        expected[k] = expected[k].format(**expected["config"])
    expected["args"] = [arg.format(**expected["config"]) for arg in expected["args"]]
    expected = executableExpected(**expected)
    return executable, expected

@pytest.mark.parametrize("processIdentifier", [
    "",
    "unique process identifier",
], ids = ["Default process identifier", "Unique process identifier"])
def testSetupExecutable(setupBasicExecutable, processIdentifier):
    """ Test setting up a basic executable. """
    executable, expected = setupBasicExecutable

    executable.processIdentifier = processIdentifier
    executable.setup()

    assert executable.name == expected.name
    assert executable.description == expected.description
    assert executable.args == expected.args
    assert executable.config == expected.config
    assert executable.processIdentifier == (processIdentifier if processIdentifier else " ".join(expected.args))

def testExecutableFromConfig(loggingMixin):
    """ Test for configuring an executable via a config.

    This duplicates some code from ``setupBasicExecutable``, but it's necessary because we need to create the
    executable in the test function to properly test the initialization.
    """
    expected = {
        "name": "{label}Executable",
        "description": "Basic executable for {label}ing",
        "args": ["execTest", "arg1", "arg2", "test{hello}"],
        "config": {"runInBackground": True, "enabled": True, "label": "test", "hello": "world"},
    }

    executable = deploy.executable(**expected)
    # Run setup so names are properly formatted
    executable.setup()

    # Determine the expected values
    for k in ["name", "description"]:
        expected[k] = expected[k].format(**expected["config"])
    expected["args"] = [arg.format(**expected["config"]) for arg in expected["args"]]
    expected = executableExpected(**expected)

    assert executable.runInBackground == expected.config["runInBackground"]
    assert executable.executeTask == expected.config["enabled"]
    assert executable.logFilename == os.path.join("exec", "logs", "{name}.log".format(name = expected.name))

@pytest.mark.parametrize("pid", [
    [],
    [1234],
], ids = ["No PIDs", "One PID"])
def testGetProcessPID(setupBasicExecutable, pid, mocker):
    """ Test of getting the process PID identified by the executable properties. """
    executable, expected = setupBasicExecutable
    executable.setup()

    # Pre-process the PID input. We don't do it above so it's easier to read here.
    inputPID = "\n".join((str(p) for p in pid)) + "\n"

    # Mock opening the process
    m = mocker.MagicMock(return_value = inputPID)
    mocker.patch("overwatch.base.deploy.subprocess.check_output", m)

    outputPID = executable.getProcessPID()

    assert outputPID == pid

@pytest.mark.parametrize("returnCode", [
    1,
    3,
], ids = ["No process found", "Unknown error"])
def testGetProcessPIDSubprocessFailure(setupBasicExecutable, mocker, returnCode):
    """ Test for subprocess failure when getting the process PID. """
    executable, expected = setupBasicExecutable
    executable.setup()

    # Test getting a process ID. We mock it up.
    m = mocker.MagicMock()
    m.side_effect = subprocess.CalledProcessError(returncode = returnCode, cmd = executable.args)
    mocker.patch("overwatch.base.deploy.subprocess.check_output", m)

    if returnCode == 1:
        outputPID = executable.getProcessPID()
        assert outputPID == []
    else:
        with pytest.raises(subprocess.CalledProcessError) as exceptionInfo:
            outputPID = executable.getProcessPID()

        assert exceptionInfo.value.returncode == returnCode

def testGetProcessPIDFailure(setupBasicExecutable, mocker):
    """ Test failure modes of getting the process PID. """
    pid = [1234, 5678]
    executable, expected = setupBasicExecutable
    executable.setup()

    # Pre-process the PID input. We don't do it above so it's easier to read here.
    inputPID = "\n".join((str(p) for p in pid)) + "\n"

    # Test getting a process ID. We mock it up.
    m = mocker.MagicMock(return_value = inputPID)
    mocker.patch("overwatch.base.deploy.subprocess.check_output", m)

    with pytest.raises(ValueError) as exceptionInfo:
        executable.getProcessPID()
    # We don't need to check the exact message.
    assert "Multiple PIDs" in exceptionInfo.value.args[0]

@pytest.fixture
def setupKillProcess(setupBasicExecutable, mocker):
    """ Setup for tests of killing a process.

    Returns:
        tuple: (executable, expected, mGetProcess, mKill) where executable is an executable object and expected are
            the expected parameters, mGetProcess is the mock for ``executable.getProcessPID()``, and mKill is the mock
            for ``executable.killExistingProcess()``.
    """
    executable, expected = setupBasicExecutable

    # First we return the PID to kill, then we return nothing (as if the kill worked)
    mGetProcessPID = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.executable.getProcessPID", mGetProcessPID)
    # Also need to mock the kill command itself.
    mKill = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.os.kill", mKill)

    # Setup
    executable.setup()

    return executable, expected, mGetProcessPID, mKill

# Intentionally select non-existent PID (above 65535) just in case the mocking doesn't work properly.
@pytest.mark.parametrize("pidsToKill", [
    [],
    [1234567],
    [1234567, 1234568],
], ids = ["No PIDs", "One PID", "Multiple PIDs"])
def testKillingProcess(setupKillProcess, pidsToKill):
    """ Test killing the process identified by the executable. """
    executable, expected, mGetProcess, mKill = setupKillProcess

    mGetProcess.side_effect = [pidsToKill, []]

    # Perform the actual method that we want to test
    nKilled = executable.killExistingProcess()

    # Check the calls
    if len(pidsToKill) == 0:
        mKill.assert_not_called()
    else:
        for pid in pidsToKill:
            if len(pidsToKill) == 1:
                mKill.assert_called_once_with(pid, signal.SIGINT)
            else:
                mKill.assert_any_call(pid, signal.SIGINT)

    # Check that the number of processes
    assert nKilled == len(pidsToKill)

def testFailedKillingProces(setupKillProcess):
    """ Test for the various error modes when killing a process. """
    executable, expected, mGetProcess, mKill = setupKillProcess

    # Setup the PIDs to always return, such that it appears as if the kill didn't work.
    pidsToKill = [1234567]
    mGetProcess.side_effect = [pidsToKill, pidsToKill]

    with pytest.raises(RuntimeError) as exceptionInfo:
        # Call the actual method that we want to test
        executable.killExistingProcess()
    # We don't need to check the exact message.
    assert "found PIDs {PIDs} after killing the processes.".format(PIDs = pidsToKill) in exceptionInfo.value.args[0]

@pytest.fixture
def setupStartProcessWithLog(setupBasicExecutable, mocker):
    """ Setup required for testing startProcessWithLog.

    It mocks:

    - Writing a ConfigParser configuration
    - ``subprocess.Popen``
    - Opening files

    Returns:
        tuple: (mFile, mPopen, mConfigParserWrite) where ``mFile`` is the mock for opening a file, ``mPopen`` is the mock
            for ``subprocess.Popen(...)``, and ``mConfigParserWrite`` is the mock for writing a ``configparser`` config.
    """
    # For standard processes
    # Mock the subprocess command
    mPopen = mocker.MagicMock(return_value = "Fake value")
    mocker.patch("overwatch.base.deploy.subprocess.Popen", mPopen)
    # For supervisor processes
    # Mock write with the config parser
    mConfigParserWrite = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.ConfigParser.write", mConfigParserWrite)
    # Shared by both
    # Mock opening the log or config file
    mFile = mocker.mock_open()
    mocker.patch("overwatch.base.deploy.open", mFile)

    return mFile, mPopen, mConfigParserWrite

def testStandardStartProcessWithLogs(setupStartProcessWithLog, setupBasicExecutable):
    """ Tests for starting a process with logs in the standard manner ("Popen"). """
    # Setup mocks
    mFile, mPopen, mConfigParserWrite = setupStartProcessWithLog
    # Setup executable
    executable, expected = setupBasicExecutable
    executable.setup()

    # Execute
    process = executable.startProcessWithLog()

    # Check that it was called successfully
    mFile.assert_called_once_with(os.path.join("exec", "logs", "{}.log".format(expected.name)), "a")
    mPopen.assert_called_once_with(expected.args, stderr = subprocess.STDOUT, stdout = mFile())

    # No need to actually mock up a subprocess.Popen class object.
    assert process == "Fake value"

def testSupervisorStartProcessWithLogs(setupStartProcessWithLog, setupBasicExecutable):
    """ Tests for starting a process with logs in supervisor. """
    # Setup mocks
    mFile, mPopen, mConfigParserWrite = setupStartProcessWithLog
    # Setup executable
    executable, expected = setupBasicExecutable
    executable.supervisor = True
    executable.setup()

    # Execute
    process = executable.startProcessWithLog()

    mFile.assert_called_once_with("supervisord.conf", "a")
    # We don't check the output itself because that would basically be testing ConfigParser, which isn't our goal.
    mConfigParserWrite.assert_called_once_with(mFile())

    assert process is None

@pytest.mark.parametrize("supervisor, runInBackground", [
    (False, False),
    (False, True),
    (True, False),
], ids = ["Standard process", "Standard process run in background", "Supervisor"])
@pytest.mark.parametrize("executeTask, shortExecutionTime", [
    (False, False),
    (True, False),
    (True, True)
], ids = ["No execute task", "Execute task", "Execute with short executable time"])
@pytest.mark.parametrize("forceRestart", [
    False,
    True,
], ids = ["No force restart", "Force restart"])
@pytest.mark.parametrize("returnProcessPID", [
    False,
    True,
], ids = ["Do not return process PID", "Return process PID"])
def testRunExecutable(setupBasicExecutable, setupStartProcessWithLog, supervisor, runInBackground, executeTask, shortExecutionTime, forceRestart, returnProcessPID, mocker):
    """ Test running an executable from start to finish.

    Note:
        Since this is an integration task, it is quite a bit more complicated than the other tests.
    """
    executable, expected = setupBasicExecutable
    # Set supervisor state first, as everything else effectively depends on this.
    executable.supervisor = supervisor
    executable.runInBackground = runInBackground
    # Set execution state.
    executable.executeTask = executeTask
    executable.shortExecutionTime = shortExecutionTime
    # Force restart.
    executable.config["forceRestart"] = forceRestart

    # Speed use the tests by avoiding actually sleeping.
    mSleep = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.time.sleep", mSleep)
    # Mock all of the relevant class methods
    mGetProcessPID = mocker.MagicMock(return_value = [1234567])
    # Ensure that we hit the branch where we do not force restart and we find no processes.
    if forceRestart is False:
        if returnProcessPID is True:
            # Continue returning a value as normal
            pass
        else:
            mGetProcessPID.return_value = None
            mGetProcessPID.side_effect = [[], [1234567]]
    mocker.patch("overwatch.base.deploy.executable.getProcessPID", mGetProcessPID)
    mKillExistingProcess = mocker.MagicMock(return_value = 1)
    mocker.patch("overwatch.base.deploy.executable.killExistingProcess", mKillExistingProcess)
    # Mocks relevant to startProcessWithLog
    mFile, mPopen, mConfigParserWrite = setupStartProcessWithLog

    # Run the executable to start the actual test
    result = executable.run()

    # We won't launch a process if executeTask is False or if we don't forceRestart
    # (since the mock returns PID values as if the process exists).
    expectedResult = False if (executeTask is False or (forceRestart is False and executeTask is False) or (forceRestart is False and returnProcessPID is True)) else True
    # Check the basic result
    assert result == expectedResult

    # Now check the details
    if result and runInBackground:
        assert executable.args[0] == "nohup"

def testRunExecutableFailure(setupBasicExecutable, setupStartProcessWithLog, mocker):
    """ Test failure of run executable when the process doesn't start. """
    # Ensure that the executable actually executes
    executable, expected = setupBasicExecutable
    executable.executeTask = True

    # Speed use the tests by avoiding actually sleeping.
    mSleep = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.time.sleep", mSleep)
    # Mock all of the relevant class methods
    mGetProcessPID = mocker.MagicMock(return_value = [])
    # Ensure that we hit the branch where we do not force restart and we find no processes.
    mocker.patch("overwatch.base.deploy.executable.getProcessPID", mGetProcessPID)
    mKillExistingProcess = mocker.MagicMock(return_value = 1)
    mocker.patch("overwatch.base.deploy.executable.killExistingProcess", mKillExistingProcess)
    # Mocks relevant to startProcessWithLog
    mFile, mPopen, mConfigParserWrite = setupStartProcessWithLog

    # Run the executable to start the actual test
    with pytest.raises(RuntimeError) as exceptionInfo:
        executable.run()
    assert "Failed to find the executed process" in exceptionInfo.value.args[0]

@pytest.fixture
def setupEnvironment(loggingMixin, mocker):
    """ Setup for testing the environment.

    Note:
        ROOT must be available in your environment!
    """
    # Store a clean environment for cleanup
    cleanEnvironment = copy.deepcopy(os.environ)

    # Setup
    config = {
        "environment": {
            "root": {
                "path": os.environ["ROOTSYS"],
            },
            "zmqReceiver": {
                "enabled": True,
                "path": os.path.join("/opt", "receiver", "bin"),
            },
            "vars": {
                "testVar": "testVal",
                "overwriteVar": "testVal2",
            },
        },
    }
    # Create a value for us to overwrite
    # It should be overwritten during setup()
    os.environ["overwriteVar"] = "overwrite"
    # Ensure that the `ROOTSYS` that is found was actually one that was set and isn't from the existing environment.
    os.environ.pop("ROOTSYS")
    assert "ROOTSYS" not in os.environ
    # Remove the receiver from the path if necessary
    receiverPath = config["environment"]["zmqReceiver"]["path"]
    if receiverPath in os.environ["PATH"]:
        os.environ["PATH"] = os.environ["PATH"].replace(receiverPath, "")

    yield config

    # Cleanup back to the original envrionemnt
    os.environ.clear()
    os.environ = cleanEnvironment

def testEnvironment(loggingMixin, setupEnvironment, mocker):
    """ (Effectively) integration tests for configuring the environment.  """
    config = setupEnvironment
    executable = deploy.environment(config = config)
    executable.setup()

    # Check ROOT setup
    # We will use ROOTSYS being set as a proxy for things working properly.
    assert "ROOTSYS" in os.environ
    assert os.environ["ROOTSYS"] == config["environment"]["root"]["path"]
    # Brief check of the path (but this isn't necessarily so instructive, as ROOT may be already be there).
    assert config["environment"]["root"]["path"] in os.environ["PATH"]

    # Check receiver setup
    receiverPath = os.path.join("/opt", "receiver", "bin")
    assert receiverPath in os.environ["PATH"]

    # Check the environment vars
    for k, v in iteritems(config["environment"]["vars"]):
        assert os.environ[k] == v

@pytest.fixture
def setupSensitiveVariables(setupEnvironment, mocker):
    """ Setup for reading from the environment and writing to file with sensitive variables. """
    # Write example config into the environment
    config = {
        "sshKey": {
            "enabled": False,
            "variableName": "mySSHKey",
            "writeLocation": os.path.join("/my", "ssh", "file"),
        },
        "gridCert": {
            "enabled": False,
            "variableName": "myCert",
            "writeLocation": os.path.join("/my", "cert", "file"),
        },
        "gridKey": {
            "enabled": False,
            "variableName": "myKey",
            "writeLocation": os.path.join("/my", "key", "file"),
        },
    }
    # Setup for the actual str to write to the environment.
    variableToWrite = "myVariableValue"

    # Mock the file to be written.
    mFile = mocker.mock_open()
    mocker.patch("overwatch.base.deploy.open", mFile)
    # Mock whether the file exists. It shouldn't exist so we can test the variable actually being written.
    mPathExists = mocker.MagicMock(return_value = False)
    mocker.patch("overwatch.base.deploy.os.path.exists", mPathExists)
    # Don't create any directories.
    mMakedirs = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.os.makedirs", mMakedirs)
    # Ensure chmod doesn't actually do anything.
    mChmod = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.os.chmod", mChmod)

    return config, variableToWrite, mFile, mPathExists, mMakedirs, mChmod

@pytest.mark.parametrize("name, func", [
    ("sshKey", deploy.environment.writeSSHKeyFromVariableToFile),
    ("gridCert", deploy.environment.writeGridCertFromVariableToFile),
    ("gridKey", deploy.environment.writeGridKeyFromVariableToFile),
], ids = ["SSH Key", "Grid certficiate", "Grid key"])
@pytest.mark.parametrize("varEnabled", [
    None,
    False,
    True,
], ids = ["No config", "Disabled", "Enabled"])
def testSensitiveVarFromEnvironment(name, func, varEnabled, setupSensitiveVariables, mocker):
    """ Test writing an SSH key from an environment variable to a file. """
    # Setup
    config, variableToWrite, mFile, mPathExists, mMakedirs, mChmod = setupSensitiveVariables
    # Enable the task
    config[name]["enabled"] = varEnabled
    # Specify the variable to retrieve
    nameOfVarWrittenToEnviornment = config[name]["variableName"]
    os.environ[nameOfVarWrittenToEnviornment] = variableToWrite
    # Remove the config entirely to test no configuration.
    if varEnabled is None:
        del config[name]

    # Setup the environment
    executable = deploy.environment(config = config)
    result = func(executable)

    if varEnabled is None or varEnabled is False:
        # Since the configuration isn't enabled, nothing should be done.
        assert result is False
    else:
        assert result is True
        expectedWriteLocation = config[name]["writeLocation"]
        # Check that the write was called with the proper value.
        mFile.assert_called_once_with(expectedWriteLocation, "w")
        mFile().write.assert_called_once_with(variableToWrite)

        if name == "sshKey":
            # By writing out the calls explicitly, we can specify the order.
            mChmod.assert_has_calls([mocker.call(expectedWriteLocation, stat.S_IRUSR | stat.S_IWUSR),
                                     mocker.call(os.path.dirname(expectedWriteLocation), stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)])
        elif name == "gridCert":
            mChmod.assert_not_called()
        elif name == "gridKey":
            mChmod.assert_called_once_with(expectedWriteLocation, stat.S_IRUSR)

    # Cleanup so it doesn't interfere with other tests.
    del os.environ[nameOfVarWrittenToEnviornment]

def testEmptySensitiveVariableFailure(setupSensitiveVariables):
    """ Test the check for an empty sensitive variable. """
    # Setup
    config, variableToWrite, mFile, mPathExists, mMakedirs, mChmod = setupSensitiveVariables
    # We just randomly select one of the options in the config. They will all be the same.
    name = "sshKey"
    # Specify the variable to retrieve
    os.environ[config[name]["variableName"]] = ""

    with pytest.raises(ValueError) as exceptionInfo:
        # This is a static method, so we don't need an executable object.
        deploy.environment.retrieveSensitiveVariable(name = name, config = config[name])
    assert exceptionInfo.value.args[0] == "The environment variable {variableName} was empty!".format(variableName = config[name]["variableName"])

    # Cleanup so it doesn't interfere with other tests.
    del os.environ[config[name]["variableName"]]

def testWriteFailureDueToExistingSensitiveFile(setupSensitiveVariables):
    """ Test that the sensitive variable won't overwrite an existing file (as desired). """
    # Setup
    config, variableToWrite, mFile, mPathExists, mMakedirs, mChmod = setupSensitiveVariables
    # We want it to think that the file already exists.
    mPathExists.return_value = True
    # We just randomly select one of the options in the config. They will all be the same.
    name = "sshKey"
    # Enable the task. It doesn't matter here, but done for consistency.
    config[name]["enabled"] = True

    with pytest.raises(IOError) as exceptionInfo:
        # This is a static method, so we don't need an executable object.
        deploy.environment.writeInfoToSensitiveFile(sensitiveVariable = "myVariableValue", defaultWriteLocation = "defaultWriteLocation", config = config[name])
    assert exceptionInfo.value.args[0] == 'File at "{writeLocation}" already exists and will not be overwritten!'.format(writeLocation = config[name]["writeLocation"])

@pytest.mark.parametrize("name, func, expectedWriteLocation", [
    ("sshKey", deploy.environment.writeSSHKeyFromVariableToFile, "~/.ssh/id_rsa"),
    ("gridCert", deploy.environment.writeGridCertFromVariableToFile, "~/.globus/usercert.pem"),
    ("gridKey", deploy.environment.writeGridKeyFromVariableToFile, "~/.globus/userkey.pem"),
], ids = ["SSH Key", "Grid Certficiate", "Grid key"])
def testWriteSensitiveParameterDefaults(setupSensitiveVariables, name, func, expectedWriteLocation):
    """ Test the defaults for writing sensitive parameters. """
    # Setup
    config, variableToWrite, mFile, mPathExists, mMakedirs, mChmod = setupSensitiveVariables
    expectedWriteLocation = os.path.expanduser(os.path.expandvars(expectedWriteLocation))
    # Setup the default task
    config[name]["enabled"] = True
    os.environ[name] = variableToWrite
    # Remove the configuration values so that we get the defaults
    del config[name]["writeLocation"]
    del config[name]["variableName"]

    # Setup the environment
    executable = deploy.environment(config = config)
    result = func(executable)

    # Check that the write was called with the proper value.
    assert result is True
    mFile.assert_called_once_with(expectedWriteLocation, "w")
    mFile().write.assert_called_once_with(variableToWrite)

@pytest.mark.parametrize("receiverPathEnabled", [
    None,
    False,
    True,
], ids = ["No config", "Receiver path disabled", "Receiver path enabled"])
def testSetupReceiverPath(receiverPathEnabled, setupEnvironment):
    """ Test setting up the receiver. """
    config = setupEnvironment["environment"]
    config["zmqReceiver"]["enabled"] = receiverPathEnabled
    receiverPath = config["zmqReceiver"]["path"]
    # Check that we are setup as expected.
    assert receiverPath == "/opt/receiver/bin"
    if receiverPathEnabled is None:
        config.pop("zmqReceiver")
    # Explicitly don't fully setup the environment - just run the receiver path setup
    executable = deploy.environment(config = config)
    # Useful in case it fails.
    logger.debug("PATH: {PATH}".format(PATH = os.environ["PATH"]))
    executable.setupReceiverPath()

    if receiverPathEnabled:
        assert receiverPath in os.environ["PATH"]
    else:
        assert receiverPath not in os.environ["PATH"]

@pytest.mark.parametrize("rootsysInEnvironment", [
    False,
    True,
], ids = ["ROOTSYS not in environment", "ROOTSYS in environment"])
def testSetupRoot(loggingMixin, rootsysInEnvironment, setupEnvironment):
    """ Test setting up the ROOT variables. """
    config = setupEnvironment["environment"]
    if rootsysInEnvironment:
        # setupEnvironment will restore ROOTSYS, so it's fine for us to mangle it here.
        os.environ["ROOTSYS"] = config["root"]["path"]

    # Explicitly don't setup the environment - just run the ROOT path setup
    executable = deploy.environment(config = config)
    # Useful in case it fails.
    logger.debug("PATH: {PATH}".format(PATH = os.environ["PATH"]))
    environmentConfigured = executable.setupRoot()

    # First check that the function executed as expected.
    assert environmentConfigured != rootsysInEnvironment

    # Now check the ROOTSYS and related values themselves.
    # We will use ROOTSYS being set as a proxy for things working properly.
    assert "ROOTSYS" in os.environ
    assert os.environ["ROOTSYS"] == config["root"]["path"]
    # Brief check of the path (but this isn't necessarily so instructive, as ROOT may be already be there).
    assert config["root"]["path"] in os.environ["PATH"]

def testSupervisorExecutable(loggingMixin, mocker):
    """ Tests for the supervisor executable. """
    executable = deploy.retrieveExecutable("supervisor", config = {})

    # Mock opening the file
    mFile = mocker.mock_open()
    mocker.patch("overwatch.base.deploy.open", mFile)
    # Mock write with the config parser
    mConfigParserWrite = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.ConfigParser.write", mConfigParserWrite)

    executable.setup()

    mFile.assert_called_once_with("supervisord.conf", "w+")
    mConfigParserWrite.assert_called_once_with(mFile())

    with pytest.raises(NotImplementedError) as exceptionInfo:
        executable.run()
    assert exceptionInfo.value.args[0] == "The supervisor executable should be run in multiple steps."

def testZMQReceiver(loggingMixin, mocker):
    """ Tests for the ZMQ receiver and the underlying executables. """
    config = {
        "enabled": True,
        "receiver": "EMC",
        "localPort": 123456,
        "dataPath": "data",
        "select": "",
        "additionalOptions": ["a", "b"],
        "tunnel": {
            "enabled": False,
            "hltPort": 234567,
            "address": "1.2.3.4",
            "port": 22,
            "username": "myUsername",
        },
    }
    executable = deploy.retrieveExecutable("zmqReceiver", config = config)

    # Show files as not existing, so they attempt to make the directory and file
    mPathExists = mocker.MagicMock(return_value = False)
    mocker.patch("overwatch.base.deploy.os.path.exists", mPathExists)
    # Don't actually create the directory
    mMakeDirs = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.os.makedirs", mMakeDirs)
    # Don't actually change the permissions
    mChmod = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.os.chmod", mChmod)
    # Prevent known_hosts from actually running
    mKnownHostsRun = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.sshKnownHosts.run", mKnownHostsRun)
    # Prevent autossh from actually running
    mAutosshRun = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.autossh.run", mAutosshRun)

    executable.setup()
    # We have to step through the setups because we mocker the run() methods
    executable.tunnel.setup()
    executable.tunnel.knownHosts.setup()

    # Check known hosts
    expectedKnownHostsArgs = [
        "ssh-keyscan",
        "-p {port}",
        "-H",
        "{address}",
    ]
    # It is formatted by the tunnel config, so be certain to use that here as an additional check.
    expectedKnownHostsArgs = [a.format(**config["tunnel"]) for a in expectedKnownHostsArgs]
    assert executable.tunnel.knownHosts.args == expectedKnownHostsArgs
    expectedKnownHostsLocation = os.path.expandvars(os.path.join("$HOME", ".ssh", "known_hosts").replace("\n", ""))
    expectedKnownHostsDir = os.path.dirname(expectedKnownHostsLocation)
    # Sanity check
    assert executable.tunnel.knownHosts.configFilename == expectedKnownHostsLocation
    # Check the setup calls
    mPathExists.assert_any_call(expectedKnownHostsLocation)
    mPathExists.assert_any_call(expectedKnownHostsDir)
    mMakeDirs.assert_called_once_with(expectedKnownHostsDir)
    mChmod.assert_called_once_with(expectedKnownHostsDir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

    # Check autossh
    expectedTunnelArgs = [
        "autossh",
        "-L {localPort}:localhost:{hltPort}",
        "-o ServerAliveInterval=30",  # Built-in ssh monitoring option
        "-o ServerAliveCountMax=3",   # Built-in ssh monitoring option
        "-p {port}",
        "-l {username}",
        "{address}",
        "-M 0",                       # Disable autossh built-in monitoring
        "-f",
        "-N",
    ]
    config["tunnel"]["localPort"] = config["localPort"]
    expectedTunnelArgs = [a.format(**config["tunnel"]) for a in expectedTunnelArgs]

    assert executable.tunnel.args == expectedTunnelArgs

    # Check zmqReceiver
    expectedArgs = [
        "zmqReceive",
        "--subsystem={receiver}",
        "--in=REQ>tcp://localhost:{localPort}",
        "--dataPath={dataPath}",
        "--verbose=1",
        "--sleep=60",
        "--timeout=100",
        "--select={select}",
    ]
    expectedArgs = [a.format(**config) for a in expectedArgs]
    expectedArgs.append(config["additionalOptions"])
    assert executable.args == expectedArgs

def testZODB(loggingMixin, mocker):
    """ Test for the ZODB executable. """
    config = {
        "address": "127.0.0.1",
        "port": 12345,
        "databasePath": "data/overwatch.fs",
    }
    executable = deploy.retrieveExecutable("zodb", config = config)

    # Mock folder creation. We want to make it a noop so we don't make a bunch of random empty folders.
    mMakedirs = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.os.makedirs", mMakedirs)
    # Mock opening the file
    mFile = mocker.mock_open()
    mocker.patch("overwatch.base.deploy.open", mFile)
    executable.setup()

    # Determine expected values
    expected = """
    <zeo>
        address {address}:{port}
    </zeo>

    <filestorage>
        path {databasePath}
    </filestorage>
    """
    # Fill in the values.
    expected = expected.format(**config)
    expected = inspect.cleandoc(expected)

    mFile.assert_called_once_with(executable.configFilename, "w")
    mFile().write.assert_called_once_with(expected)

@pytest.fixture
def setupOverwatchExecutable(loggingMixin):
    """ Setup basic Overwatch executable for testing.

    Args:
        None.
    Returns:
        tuple: (overwatchExecutable, expected) where ``overwatchExecutable`` (overwatchExecutable) is the
            created overwatch executable, and ``expected`` (dict) are the expected outputs.
    """
    expected = executableExpected(
        name = "testExecutable",
        description = "Basic executable for testing",
        args = ["exec", "arg1", "arg2"],
        config = {"additionalOptions": {"opt1": {"a", "b"}, "opt2": True}}
    )
    executable = deploy.overwatchExecutable(**expected._asdict())

    yield executable, expected

@pytest.mark.parametrize("existingConfig", [
    {},
    {"existingOption": True},
    {"opt2": False},
], ids = ["Config from scratch", "Appending to non-overlapping values", "Update overlapping values"])
def testWriteCustomOverwatchConfig(setupOverwatchExecutable, existingConfig, mocker):
    """ Test writing a custom Overwtach config. """
    # Basic setup
    executable, expected = setupOverwatchExecutable

    filename = "config.yaml"
    executable.configFilename = filename

    # Determine the expected result
    expectedConfig = existingConfig.copy()
    expectedConfig.update(expected.config["additionalOptions"])

    # Need to encode the existing config with yaml so that we can input a string...
    inputStr = StringIO()
    yaml.dump(existingConfig, inputStr, default_flow_style = False)
    inputStr.seek(0)

    # Mock checking for a file
    mPathExists = mocker.MagicMock(return_value = (existingConfig != {}))
    mocker.patch("overwatch.base.deploy.os.path.exists", mPathExists)
    # Mock opening the file
    mFile = mocker.mock_open(read_data = inputStr.read())
    mocker.patch("overwatch.base.deploy.open", mFile)
    # Mock yaml.dump so we can check what was written.
    # (We can't check the write directly because dump writes many times!)
    mYaml = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.configModule.yaml.dump", mYaml)

    # Perform the actual setup
    executable.setup()

    # Should both read and write from here
    if existingConfig != {}:
        mFile.assert_any_call(filename, "r")
    mFile.assert_called_with(filename, "w")

    # Confirm that we've written the right information
    mYaml.assert_called_once_with(expectedConfig, mFile(), default_flow_style = False)

def testTwoOverwatchExecutablesWithCustomConfigs(loggingMixin):
    """ Test two Overwatch executables writing to the same config. """
    # We just write to a scratch area since it is faster and easier.
    # Otherwise, mocks need to be turned on and off, etc.
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "deployScratch")
    # Ensure that it exists. It won't by default because we don't store any files that are copied there in git.
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = os.path.join(directory, "config.yaml")

    # Processing and web app are selected randomly. Any overwatch executables would be fine.
    processingOptions = {"additionalOptions": {"processing": True}}
    processing = deploy.retrieveExecutable("processing", config = processingOptions)
    processing.configFilename = filename

    webAppOptions = {"uwsgi": {}, "additionalOptions": {"webApp": True}}
    webApp = deploy.retrieveExecutable("webApp", config = webAppOptions)
    webApp.configFilename = filename

    # Write both configurations
    processing.setup()
    webApp.setup()

    expected = processingOptions["additionalOptions"].copy()
    expected.update(webAppOptions["additionalOptions"])

    with open(filename, "r") as f:
        generatedConfig = deploy.configModule.yaml.load(f, Loader = yaml.SafeLoader)

    assert generatedConfig == expected

@pytest.mark.parametrize("executableType, config, expected", [
    ("dataTransfer", {"additionalOptions": {"testVal": True, "dataTransferLocations": {"EOS": "EOSpath", "rsync": "rsyncPath"}}},
     executableExpected(name = "dataTransfer",
                        description = "Overwatch receiver data transfer",
                        args = ["overwatchReceiverDataTransfer"],
                        config = {"testVal": True, "dataTransferLocations": {"EOS": "EOSpath", "rsync": "rsyncPath"}})),
    ("processing", {},
     executableExpected(name = "processing",
                        description = "Overwatch processing",
                        args = ["overwatchProcessing"],
                        config = {})),
    ("webApp", {"uwsgi": {}},
     executableExpected(name = "webApp",
                        description = "Overwatch web app",
                        args = ["overwatchWebApp"],
                        config = {})),
    ("webApp", {"uwsgi": {"enabled": True}},
     executableExpected(name = "webApp",
                        description = "Overwatch web app",
                        args = ["uwsgi", "--yaml", "exec/config/webApp_uwsgi.yaml"],
                        config = {})),
    ("webApp", {"uwsgi": {"enabled": True}, "nginx": {"enabled": True}},
     executableExpected(name = "webApp",
                        description = "Overwatch web app",
                        args = ["uwsgi", "--yaml", "exec/config/webApp_uwsgi.yaml"],
                        config = {})),
    ("dqmReceiver", {"uwsgi": {}},
     executableExpected(name = "dqmReceiver",
                        description = "Overwatch DQM receiver",
                        args = ["overwatchDQMReceiver"],
                        config = {})),
], ids = ["Data transfer", "Processing", "Web App", "Web App - uwsgi", "Web App - uwsgi + nginx", "DQM Receiver"])
def testOverwatchExecutableProperties(loggingMixin, executableType, config, expected, setupStartProcessWithLog, mocker):
    """ Integration test for the setup and properties of Overwatch based executables. """
    executable = deploy.retrieveExecutable(executableType, config = config)

    # Centralized setup for `uwsgi`. Defined here so we don't have to copy it in parametrize.
    uwsgi = False
    if "uwsgi" in executable.config and executable.config["uwsgi"].get("enabled", False):
        uwsgi = True
        executable.config["uwsgi"] = {
            "enabled": True,
            "module": "overwatch.webApp.run",
            "http-socket": "127.0.0.1:8850",
            "additionalOptions": {
                "chdir": "myDir",
            }
        }
    # Centralized setup for `nginx`. Defined here so we don't have to copy it in parametrize.
    nginx = False
    if "nginx" in executable.config and executable.config["nginx"]["enabled"]:
        nginx = True
        executable.config["nginx"] = {
            "enabled": True,
            "webAppName": "webApp",
            "basePath": "exec/config",
            "sitesPath": "sites-enabled",
            "configPath": "conf.d",
        }

    # Mocks relevant to startProcessWithLog
    mFile, mPopen, mConfigParserWrite = setupStartProcessWithLog
    # Mocks for checking the custom config
    mFile = mocker.mock_open()
    mocker.patch("overwatch.base.deploy.open", mFile)
    # Mock yaml.dump so we can check what was written.
    # (We can't check the write directly because dump writes many times!)
    mYaml = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.configModule.yaml.dump", mYaml)
    # Mock running nginx so we don't have to mock all of run()
    mNginxRun = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.nginx.run", mNginxRun)
    # Mock running grid toekn and ssh known hosts so we don't have to mock all of run()
    # These are used by the data transfer module
    mGridTokenProxy = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.gridTokenProxy.run", mGridTokenProxy)
    mKnownHosts = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.sshKnownHosts.run", mKnownHosts)
    # Avoid creating any new directories
    mMakedirs = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.os.makedirs", mMakedirs)

    # Perform task setup.
    executable.setup()
    # Special call to this function so we don't have to mock all of run(). We just want to run setup() to check the config.
    if nginx:
        executable.nginx.setup()

    # Confirm basic properties:
    assert executable.name == expected.name
    assert executable.description == expected.description
    assert executable.args == expected.args

    # Only check for a custom config if we've actually written one.
    if expected.config:
        mYaml.assert_called_once_with(expected.config, mFile(), default_flow_style = False)

    # Check for uwsgi config.
    if uwsgi:
        mFile.assert_any_call(expected.args[2], "w")
        # Effectively copied from the uwsgi config
        expectedConfig = {
            "vacuum": True,
            "stats": ":9002",
            "chdir": "myDir",
            "http-socket": "127.0.0.1:8850",
            "module": "overwatch.webApp.run",
            "callable": "app",
            "lazy-apps": True,
            "processes": 4,
            "threads": 2,
            "cheaper": 2,
            "master": True,
            "master-fifo": "myDir/exec/sockets/wsgiMasterFifo{name}.sock",
        }
        # Format in the variables
        for k, v in iteritems(expectedConfig):
            if isinstance(v, str):
                expectedConfig[k] = v.format(name = "{name}_uwsgi".format(name = expected.name))
        expectedConfig = {"uwsgi": expectedConfig}
        mYaml.assert_any_call(expectedConfig, mFile(), default_flow_style = False)

    # Check for nginx config.
    if nginx:
        expectedMainNginxConfig = """
        server {
            listen 80 default_server;
            # "_" is a wildcard for all possible server names
            server_name _;
            location / {
                include uwsgi_params;
                uwsgi_pass unix:///tmp/sockets/%(name)s.sock;
            }
        }"""

        # Use "%" formatting because the `nginx` config uses curly brackets.
        expectedMainNginxConfig = expectedMainNginxConfig % {"name": executable.config["nginx"]["webAppName"]}
        expectedMainNginxConfig = inspect.cleandoc(expectedMainNginxConfig)

        mFile.assert_any_call(os.path.join("exec", "config", "sites-enabled", "webAppNginx.conf"), "w")
        mFile().write.assert_any_call(expectedMainNginxConfig)

        # We skip the gzip config contents because they're static
        mFile.assert_any_call(os.path.join("exec", "config", "conf.d", "gzip.conf"), "w")

def testUwsgiExecutableRunFailure(loggingMixin):
    """ Minimal test to ensure that the uwsgi executable fails when attempting to execute it directly. """
    # Create the executable. The values don't matter.
    uwsgi = deploy.uwsgi(name = "uwsgi", description = "uwsgi test", args = [], config = {})
    # We intentionally skip setup, since it won't matter, and allows us to avoid needing to mock it.

    # Attempt to run (which should fail).
    with pytest.raises(NotImplementedError) as exceptionInfo:
        uwsgi.run()
    assert exceptionInfo.value.args[0] == "The uwsgi object should not be run directly."

@pytest.mark.parametrize("executablesToEnableFromEnvironment, additionalExecutablesToEnable, expectedEnabledExecutables", [
    ("zodb, processing", [], ["zodb", "processing"]),
    ("zodb,processing", [], ["zodb", "processing"]),
    ("zodb, processing", ["processing"], ["zodb", "processing"]),
], ids = ["Base test", "No spaces in string", "Already enabled executable"])
def testEnableExecutablesFromEnvironmentVariables(loggingMixin, executablesToEnableFromEnvironment, additionalExecutablesToEnable, expectedEnabledExecutables):
    """ Test enabling executables via an environment variable. """
    # Store a clean environment for cleanup
    cleanEnvironment = copy.deepcopy(os.environ)

    # Use the reference config for configuration. Everything is disabled by default, so
    # there should be less to mock. Note that we take advantage of the reference distributed in the source.
    referenceFilename = pkg_resources.resource_filename("overwatch.base", "deployReference.yaml")
    with open(referenceFilename, "r") as f:
        config = deploy.configModule.yaml.load(f, Loader = yaml.SafeLoader)

    # Setup config
    for executable in additionalExecutablesToEnable:
        config["executables"][executable]["enabled"] = True
    # Setup environment
    os.environ["OVERWATCH_EXECUTABLES"] = executablesToEnableFromEnvironment

    # Add the new executables
    config = deploy.enableExecutablesFromEnvironment(config = config)

    # Check which executables are enabled
    enabledExecutables = []
    for name in config["executables"]:
        if config["executables"][name]["enabled"]:
            enabledExecutables.append(name)

    assert set(enabledExecutables) == set(expectedEnabledExecutables)

    # Cleanup
    os.environ.clear()
    os.environ = cleanEnvironment

@pytest.mark.parametrize("enableSupervisor", [
    False,
    True,
], ids = ["Standard execution", "Supervisor"])
@pytest.mark.parametrize("configureFromEnvironment", [
    False,
    True,
], ids = ["Configuration file", "Configuration from environment variable"])
@pytest.mark.parametrize("enabledExecutables", [
    ("zmqReceiver_EMC", "zmqReceiver_TPC", "dqmReceiver", "dataTransfer"),
    ("zodb", "processing"),
    ("zodb", "webApp"),
], ids = ["Receiver", "Processing", "Web app"])
def testStartOverwatch(loggingMixin, enableSupervisor, configureFromEnvironment, enabledExecutables, mocker):
    """ Test for the main driver function. """
    # Store a clean environment for cleanup
    cleanEnvironment = copy.deepcopy(os.environ)

    # Ignore any interfering environment variables
    os.environ.pop("OVERWATCH_EXECUTABLES", None)

    # Use the reference config for configuration. Everything is disabled by default, so
    # there should be less to mock. Note that we take advantage of the reference distributed in the source.
    referenceFilename = pkg_resources.resource_filename("overwatch.base", "deployReference.yaml")
    with open(referenceFilename, "r") as f:
        config = deploy.configModule.yaml.load(f, Loader = yaml.SafeLoader)

    # Turn supervisor on or off depending on the test.
    config["supervisor"] = enableSupervisor
    # Enable selected executables
    for executable in enabledExecutables:
        config["executables"][executable]["enabled"] = True

    # Now write the configuration to the config str.
    # We don't perform this initially on the read because we need to update the configuration before
    # we turn it back into a string.
    configStr = StringIO()
    deploy.configModule.yaml.dump(config, configStr, default_flow_style = False)
    configStr.seek(0)
    # Convert to a standard string
    configStr = configStr.read()

    # Setup config var or file.
    configVar = ""
    configFilename = ""
    mFile = None
    if configureFromEnvironment:
        configVar = "CONFIGURE_KEY"
        os.environ[configVar] = configStr
        # Generally mock opening files. We separate this because we don't want to allow returning data
        # except when necessary. This will help us avoid unexpected results.
        mFile = mocker.mock_open()
    else:
        configFilename = "configFilename.yaml"
        # Need to define here because we can't just set the read_data attribute after creating the object.
        mFile = mocker.mock_open(read_data = configStr)
    mocker.patch("overwatch.base.deploy.open", mFile)

    # To check the supervisor config
    mConfigParserWrite = mocker.MagicMock()
    mocker.patch("overwatch.base.deploy.ConfigParser.write", mConfigParserWrite)
    mPopen = mocker.MagicMock(return_value = "Fake value")
    mocker.patch("overwatch.base.deploy.subprocess.Popen", mPopen)
    # Replace run() by just checking whether the task should execute. That's all we really care about here.
    mocker.patch("overwatch.base.deploy.executable.run", new = lambda self: self.executeTask)

    # Make the actual call. Note that this will run the environment setup (but nearly everything is disabled by default).
    executables = deploy.startOverwatch(configFilename = configFilename, configEnvironmentVariable = configVar)

    # Check the supervisor results
    if enableSupervisor:
        mConfigParserWrite.assert_called_once_with(mFile())
        # Check that supervisorctl was called
        mPopen.assert_called_once_with(["supervisorctl", "update"])

    # Check the execution status of the individual tasks.
    names = []
    for name, executable in iteritems(executables):
        # Each task should be configured to execute.
        assert executable.executeTask is True
        # We keep track of the names so we can ensure that only the selected tasks are executed (ie that no
        # unanticipated tasks were executed). See the block below for the completion of this check.
        names.append(name)

    # Ensure that all tasks that should be executed were actually executed.
    assert set(names) == set(enabledExecutables)

    # Cleanup
    os.environ.clear()
    os.environ = cleanEnvironment

