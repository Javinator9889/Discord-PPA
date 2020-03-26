# Discord PPA
![Discord brand](https://indiemegabooth.com/wp-cargo/uploads/2018/03/Discord-LogoWordmark-Black.png)

A private package that downloads the latest Discord .deb file available from official website

## Motivation

[Discord](https://discordapp.com/) is a chatting and texting application
whose motivation is to substitute both Skype and TeamSpeak as the desired 
chat application for gamers and general purpose.

Currently, Discord is available for downloading for all platforms but, in
Linux, it is only available for downloading as a raw .deb file or using
the Snap Store, without any official PPA. As some users are against the
Snap Store (due to its limitations, restrictions and policies), this 
repository aims to provide an easy solution for all users who want to have
Discord installed and upgradeable.

## How it works?

On the one hand, Discord is available for downloading from the official
website, using the following URL: 
https://discordapp.com/api/download?platform=linux&format=deb

With that in mind, the file `lookup-server.py` just runs every fifteen
minutes and downloads the latest .deb file provided by that link. Then, 
using the `reprepro` program, the PPA is updated and, if a new version is
available, served to the users.

In that way, the PPA is always up-to-date (with a delay of at most 15
minutes) and the end-user can have the stable installation of Discord
(or beta one) in their computers.

## Installation

Firstly, we need to **import** the GPG repository keys:

```shell script
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 5890E288F7ED6702
```

Then, add the repository to your `sources.list` as follows:

+ For the *stable* version, use the `all` distribution.
+ For the *beta* version, use the `public-beta` distribution.
+ You can use HTTPS if you want.

```shell script
# Stable repository
sudo add-apt-repository "deb [arch=amd64] https://ppa.javinator9889.com/ all main"

# Beta repository
sudo add-apt-repository "deb [arch=amd64] https://ppa.javinator9889.com public-beta main"
```

Finally, update and install Discord:

```shell script
sudo apt update && sudo apt install discord

# If using public beta, install as follows:
sudo apt install discord-ptb
```

You can browse the repository at the following URL:
https://ppa.javinator9889.com

## Upgrading

For upgrading Discord, it is as simple as running the `apt update` and `apt
 upgrade` commands:
 
```shell script
sudo apt update && sudo apt upgrade
```

## Uninstalling Discord and repository

If you would like to remove Discord from your computer and remove the repository
from your `sources.list`, run the following commands:

```shell script
sudo apt remove discord
# If using public beta, uninstall as follows
sudo apt remove discord-ptb

# Remove the repository using the add-apt-repository command
# Keep in mind it must be the same as you added (stable, beta, etc.)
sudo add-apt-repository -r "deb [arch=amd64] https://ppa.javinator9889.com/ all main"

# Finally, remove the key if you want not to trust it anymore
sudo apt-key del 5890E288F7ED6702
```

## License

```
                                Discord PPA
                    Copyright (C) 2020  Javinator9889

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
