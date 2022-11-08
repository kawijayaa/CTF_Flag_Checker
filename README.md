# CTF_Flag_Checker

### A mini-infrastructure(?) for creating and checking CTF flags
Built using MongoDB and Python

Example Flag : CTF2022{h3llo_w0rld!!!_6188b9990e}

### Structure
competition_name
- flags
  - chall_name
  - flag_text (only the obfuscated text, e.g. "h3llo_w0rld!!!")
- teams
  - team (team name)
  - flag_checksums (list of checksums by their challenges)
    - chall_name 1
    - checksum 2
    - chall_name 2
    - checksum 2
    - ...
  - ...

### Input JSONs
flags.json
- flags
  - chall_name
  - flag_text (only the obfuscated text, e.g. "hello_world!!!")
  - ...

teams.json
- teams
  - team (team name)
  - ...
