import subprocess
import time

proc = subprocess.Popen(
    ["git", "credential-manager", "github", "login", "--device"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

# Read lines
start = time.time()
while time.time() - start < 10:
    line = proc.stdout.readline()
    if line:
        print(line, end="")
        if "https://github.com/login/device" in line or "code" in line.lower():
            break
    time.sleep(0.5)

print("\nProcess state:", proc.poll())
