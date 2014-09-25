tc-hue
======

Updates a Philips Hue depending on TeamCity build status.

Create a `config.json` file based on the `config_example.json` in the repository. You'll
need to enter TeamCity hostname and credentials as well as the ip/hostname of the Philips Hue
Bridge.

Then simply run `python update_lamps.py` to update the lamps.

Dependencies

* phue
