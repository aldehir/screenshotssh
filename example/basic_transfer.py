#!/usr/bin/env python
from __future__ import print_function

import sys

from screenshotssh import transfer

def progress(sent, total):
    percent = 100.0 * (float(sent) / float(total))
    print("Sent {0} B / {1} B ({2})".format(sent, total, percent))

agent = transfer.TransferAgent()

agent.connect("localhost", private_key_file="~/.ssh/id_ecdsa.pub")
print("Transfering {0}".format(sys.argv[1]))
agent.transfer(sys.argv[1], "screenshots", callback=progress)
agent.close()
