 tc-hue [![Build Status](https://travis-ci.com/Volumental/tc-hue.svg?branch=master)](https://travis-ci.com/Volumental/tc-hue)
========

Updates a Philips Hue depending on TeamCity build status.

The machine running this code needs to be on the same network as the Phillips Hue Bridge.

Then simply run `./update_lamp.sh` to update the lamps. The first time you run it, it will ask you to press the button on the Phillips Hue Bridge.

Dependencies
* phue
* mock (only if you want to run tests)

## Raspberry PI
To setup a raspberry pi, just
* Install Rapian as per normal
* Change the default password - Remember to update in 1password as well.
* Update the hostname to `build-lamp` by editing `/etc/hostname` (and `/etc/hosts`).
* Enable ssh server.
* Install git `apt install git`

## git push setup
To make it easy to push code to the raspberry use a git bare repo

1. Create a directory `mkdir tc-hue.git`
2. Create the bare repo `cd tc-hue.git && git init --bare`
3. Put the following in `hooks/post-receive`

    #!/bin/bash
    DIR=/home/pi/tc-hue
    mkdir -p "$DIR"
    GIT_WORK_TREE="$DIR" git checkout -f master

    cd "$DIR/"
    ./deploy.sh

4. Make it executable `chmod +x hooks/post-receive`
5. Create the target directory `mkdir /home/pi/tc-hue`
5. Back at your dev machine git remote add build-lamp pi@build-lamp.local.:tc-hue.git
6. Push code `git push build-lamp`

## Crontab setup
To make the update script run e.g. every 5th minute, run `crontab -e` and put in an entry like so
/5 * * * * /tc-hue/update_lamp.sh >/dev/null 2>&1

## Windows setup
Some old documentation for setting up scheduled execution on windows.

    schtasks /create /sc minute /mo 1 /tn "Update Build Lamps" /tr C:\Users\volumental\tc-hue\update_lamp.bat 

# The server
There is a small flask server to make it easier to trigger the updating

1. Copy `build-lamp.service` to `/etc/sytemd/system`.
2. `chown root:root /etc/sytemd/system/build-lamp.service`
3. `sudo systemctl enable build-lamp.service`
4. `sudo service build-lamp start`

Go to `http://build-lamp.local.:5000/`
