import sys
import subprocess

if len(sys.argv) < 2:
    print("Usage: task make-migration -- 'your message here'")
    sys.exit(1)

message = sys.argv[1]
subprocess.run(["alembic", "revision", "--autogenerate", "-m", message])
