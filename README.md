```
Repeat a command

Usage: repeat.exe [OPTIONS] <CMD>

Arguments:
  <CMD>  The command to run

Options:
  -q, --quiet                Do not print to console
  -d, --direct               Do not use shell
  -n, --attempts <ATTEMPTS>  Maximum number of times to repeat
  -b, --no-break             Passthrough Ctrl+Break
  -0, --till-success         Repeat the command until it succeeds
  -1, --till-failure         Repeat the command until it fails
  -h, --help                 Print help information
```
