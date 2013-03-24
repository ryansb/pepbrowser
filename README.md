pepbrowser
====

The pepbrowser is a command line client for reading Python Enhancement
Proposals.

It's written using the urwid library and caches peps in the ~/.cache/pepbrowser
directory. It'll try to read cached PEPs to save latency, but while you read it
will ensure that you're reading the most up-to-date version.

Currently it's in a non-working state (surprise, writing a decent pager is hard).
