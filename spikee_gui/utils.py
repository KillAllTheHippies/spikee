import subprocess

def capture_output(func, *args, **kwargs):
    """Decorator to capture stdout/stderr from a function call."""
    # Get the module name from the function's module
    module_name = func.__module__

    # Create a subprocess to run the function
    process = subprocess.Popen(['python', '-c', f'''
import sys
from io import StringIO
from {module_name} import {func.__name__}

sys.stdout = mystdout = StringIO()
sys.stderr = mystderr = StringIO()

try:
    result = {func.__name__}(*{args}, **{kwargs})
    print("---STDOUT---")
    print(mystdout.getvalue())
    print("---STDERR---")
    print(mystderr.getvalue())

except Exception as e:
    print("---STDOUT---")
    print(mystdout.getvalue())
    print("---STDERR---")
    print(mystderr.getvalue())
    print("---EXCEPTION---")
    print(e)
'''], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    stdout, stderr = process.communicate()

    # Extract stdout, stderr, and potential exceptions
    stdout_start = stdout.find("---STDOUT---") + len("---STDOUT---")
    stderr_start = stdout.find("---STDERR---") + len("---STDERR---")
    exception_start = stdout.find("---EXCEPTION---")

    captured_stdout = stdout[stdout_start:stderr_start - len("---STDERR---")].strip()
    captured_stderr = stdout[stderr_start:exception_start if exception_start != -1 else None].strip()
    captured_exception = stdout[exception_start + len("---EXCEPTION---"):].strip() if exception_start != -1 else None

    # Return the captured stdout
    return captured_stdout
