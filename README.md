tc-hue
======

Updates a Philips Hue depending on TeamCity build status.

Create a `config.json` file based on the `config_example.json` in the repository. You'll
need to enter TeamCity hostname and credentials as well as the ip/hostname of the Philips Hue
Bridge.

Then simply run `python update_lamp.py` to update the lamps.

On the current build server the update script is run as a cron task under builder user from the path:
/home/builder/tc-hue/

Dependencies

* phue
* tweepy
* mock (only if you want to run tests)

Example command for scheduling a task in Windows:

```
schtasks /create /sc minute /mo 1 /tn "Update Build Lamps" /tr C:\Users\volumental\tc-hue\update_lamp.bat 
```

Example crontab line for updating the lamps every 5 minutes
```crontab
*/5     *       *       *       *       /home/pi/tc-hue/update_lamp.sh`
```
