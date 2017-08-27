from __future__ import print_function

import sys
import os
import posixpath
import click
import pyperclip
import time

from contextlib import closing

from .transfer import TransferAgent

if sys.version_info > (3, 0):
    from urllib.parse import urlparse
else:
    from urlparse import urlparse


@click.command()
@click.argument("filepath")
@click.argument("remotepath")
@click.option("--identity", default="~/.ssh/id_rsa")
@click.option("--host-keys", help="host keys to load")
@click.option("--clipboard", metavar="URL",
              help="copy to clickboard with URL prefix")
@click.option("--length", default=7, help="length of randomized file name")
@click.option("--randomize/--no-randomize", default=True,
              help="randomize file name")
def upload(filepath, remotepath, identity, host_keys, clipboard, length,
            randomize):
    key_file = os.path.expandvars(os.path.expanduser(identity))
    user, host, port, dest = parse_remote_path(remotepath)

    agent = TransferAgent()

    if host_keys:
        path = os.path.expandvars(os.path.expanduser(host_keys))
        agent.load_host_keys(path)

    with closing(agent.connect(host, username=user, port=port,
                               private_key_file=key_file)):
        resultpath = agent.transfer(filepath, dest, callback=progress,
                                    randomize=randomize, name_length=length)

    print("Transfered {0} -> {1}".format(filepath, resultpath))

    basename = posixpath.basename(resultpath)

    if clipboard:
        copy_text = clipboard + basename

        try:
            copy_to_clipboard(copy_text)
            print("Copied to clipboard: {0}".format(copy_text))
        except:
            print("Unable to copy to clipboard: {0}".format(copy_text))
            raise


def parse_remote_path(path):
    if not path.startswith("sftp://"):
        path = "sftp://" + path

    parsed = urlparse(path)
    return (parsed.username, parsed.hostname,
            parsed.port or 22, parsed.path[1:])
    

def progress(sent, total):
    percent = 100.0 * (float(sent) / float(total))
    print("Sent {0} B / {1} B ({2})".format(sent, total, percent))


def copy_to_clipboard(text):
    pyperclip.copy(text)


if __name__ == "__main__":
    upload()
