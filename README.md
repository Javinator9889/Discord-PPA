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

Please, refer to https://blog.javinator9889.com/discord-ppa-keep-it-up-to-date-on-linux-easily/ for up-to-date instructions:
some things changes and the blog is constantly being updated.

You can browse the repository at the following URL:
https://ppa.javinator9889.com

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
