Initial implementation in Python. This was re-written in Rust due to performance reasons

```
usage: repeat.exe [-h] [-b] [-q] [-0] [-1] [-n ATTEMPTS] [-d] CMD

Repeat a command

positional arguments:
  CMD                   The command to run

options:
  -h, --help            show this help message and exit
  -b, --no-break        Passthrough Ctrl+Break
  -q, --quiet           Do not print to console
  -0, --till-success    Repeat the command until it succeeds
  -1, --till-failure    Repeat the command until it fails
  -n ATTEMPTS, --attempts ATTEMPTS
                        Maximum number of times to repeat
  -d, --direct          Do not use shell
```

---

To compile, run `uv run freeze.py`
