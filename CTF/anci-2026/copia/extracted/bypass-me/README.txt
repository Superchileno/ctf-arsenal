Bypass me
=========

We imaged a decommissioned LIMBO archive node before it went to the shredder.
It is the retrieval client (limbo-arc.py) plus its block catalog.

Public blocks 1-4 read fine. There is a maintenance block the ops crew keeps
sealed. The client will not hand it over by its public number. The payload it
holds is what we are after.

Run it:  python3 limbo-arc.py --list
