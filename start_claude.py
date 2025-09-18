import subprocess
import sys

try:
    cmd = "claude --dangerously-skip-permissions"
    subprocess.run(cmd, shell=True, check=True)
except FileNotFoundError:
    print("Error: 'claude' command not found in PATH")
    print("Please make sure Claude Code CLI is installed and added to your system PATH")
    sys.exit(1)
except subprocess.CalledProcessError as e:
    print(f"Error running claude: {e}")
    sys.exit(1)
