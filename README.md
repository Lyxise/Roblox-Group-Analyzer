# Roblox-Group-Analyzer
made by lyxise
## Overview
This project is to be used to quickly and easily find NSFW accounts on Roblox to make it easier to report them using the EU / DSA report system and get the accounts moderated. Designed for / on Windows, should run fine on Linux. (Mac not supported yet)
## Dependencies
Simple tool to be used to detect NSFW accounts in roblox groups and organize them into an easily-readable list.
Requires: [Python](https://www.python.org) & [requests](https://pypi.org/project/requests/) library. Install requests with pip using `pip install requests`. Intended to be used on Windows.
## Usage
After downloading the project and the requests library, run the 'Group Analyzer.py' file and enter the Roblox GroupID of a group being used by predators / people advertising illicit content. It will analyze every profile and print when it does so. After the program has finished, navigate to and open the 'output.txt' file. Higher scores = more probability of the account being used for malicious purposes.
## Notes
This system CAN have false positives, however, it is unlikely unless you are using the project on an innocent group (not filled with predators).
Sometimes you may have to wait until the last couple hundred members for accounts to start getting flagged. This is normal.
Deleted accounts can still be flagged. This will be fixed.
## Planned Features
- Morse Code detection & automatic translation
- Removal of deleted accounts from 'output.txt'
- System that sends verified flagged accounts to a webhook
- Detects if avatar is innapropriate via wearing several flagged UGC
