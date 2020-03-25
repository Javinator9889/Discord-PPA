#                             discord-ppa
#                  Copyright (C) 2020 - Javinator9889
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#                   (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#               GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
import os
import sys
import urllib3
import logging

from pathlib import Path
from sched import scheduler
from time import time, sleep
from daemonize import Daemonize
from tempfile import TemporaryFile
from subprocess import Popen, PIPE

delay_secs = 900
discord_url = "https://discordapp.com/api/download?platform=linux&format=deb"
try:
    ppa_path = sys.argv[1]
except IndexError:
    print("You must provide the PPA directory")
    exit(1)
reprepro_cmd = "reprepro -b {0} includedeb all ".format(ppa_path)
http = urllib3.PoolManager()

home = str(Path.home())
pid = f"{home}/discord-ppa/discord-ppa.pid"
os.mkdir(f"{home}/discord-ppa")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("{0}/discord-ppa/discord-ppa.log"
                                   .format(home), "w")
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
keep_fds = [file_handler.stream.fileno()]


def main():
    sched = scheduler(time, sleep)
    run_update_process()
    try:
        while True:
            sched.enter(delay_secs, 0, run_update_process)
            sched.run()
    except InterruptedError:
        exit(0)


def download_latest_deb(fp: TemporaryFile):
    result = http.request("GET", discord_url, redirect=True)
    if result.status == 200:
        logger.info("Downloaded correctly Discord .deb file")
        fp.write(result.data)
    else:
        logger.error("Discord .deb file could not be downloaded - status "
                     "code: {0}".format(result.status))


def update_reprepro(fp: TemporaryFile):
    file_path = f"/tmp/{fp.name}"
    command = (reprepro_cmd + file_path).split()
    proc = Popen(command, stdout=PIPE, stderr=PIPE)
    proc.communicate()
    if proc.returncode != 0:
        logger.error("reprepro ended with an error - ret. code: "
                     "{0}".format(proc.returncode))
    else:
        logger.info("reprepro finished OK")


def run_update_process():
    fp = TemporaryFile(suffix=".deb")
    try:
        download_latest_deb(fp)
        update_reprepro(fp)
    finally:
        fp.close()


daemon = Daemonize(app="discord-ppa",
                   pid=pid,
                   action=main,
                   keep_fds=keep_fds,
                   logger=logger)
daemon.start()
