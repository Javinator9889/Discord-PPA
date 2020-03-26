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
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
from logging.handlers import RotatingFileHandler

delay_secs = 900
discord_url = "https://discordapp.com/api/download?platform=linux&format=deb"
discord_pbeta_url = \
    "https://discordapp.com/api/download/ptb?platform=linux&format=deb"
try:
    ppa_path = sys.argv[1]
except IndexError:
    print("You must provide the PPA directory")
    exit(1)
reprepro_cmd = "reprepro -b {0} includedeb %dist% %file%".format(ppa_path)
http = urllib3.PoolManager()

home = str(Path.home())
pid = "{0}/discord-ppa/discord-ppa.pid".format(home)
try:
    os.mkdir("{0}/discord-ppa".format(home))
except FileExistsError:
    pass

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fmt = logging.Formatter(
    "%(process)d - %(asctime)s | [%(levelname)s]: %(message)s"
)

file_handler = RotatingFileHandler("{0}/discord-ppa/discord-ppa.log"
                                   .format(home), "w", maxBytes=2 << 20,
                                   backupCount=2)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(fmt)

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


def download_latest_deb(fp: NamedTemporaryFile, url: str):
    result = http.request("GET", url, redirect=True)
    if result.status == 200:
        logger.info("Downloaded correctly Discord .deb file")
        fp.write(result.data)
    else:
        logger.error("Discord .deb file could not be downloaded - status "
                     "code: {0}".format(result.status))


def update_reprepro(fp: NamedTemporaryFile, dist: str):
    cmd = reprepro_cmd.replace("%dist%", dist)\
                      .replace("%file%", fp.name)\
                      .split()
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0:
        error = err.decode("utf-8")
        logger.error("reprepro ended with an error - ret. code: "
                     "{0} | output: \n{1}".format(proc.returncode,
                                                  error))
    else:
        output = out.decode("utf-8") + "\n" + err.decode("utf-8")
        logger.info("reprepro finished OK | output:\n {0}".format(output))


def run_update_process():
    stable = NamedTemporaryFile(suffix=".deb")
    beta = NamedTemporaryFile(suffix=".deb")
    try:
        download_latest_deb(stable, discord_url)
        update_reprepro(stable, "all")
        download_latest_deb(beta, discord_pbeta_url)
        update_reprepro(beta, "public-beta")
    finally:
        stable.close()
        beta.close()


daemon = Daemonize(app="discord-ppa",
                   pid=pid,
                   action=main,
                   keep_fds=keep_fds,
                   logger=logger)
daemon.start()
