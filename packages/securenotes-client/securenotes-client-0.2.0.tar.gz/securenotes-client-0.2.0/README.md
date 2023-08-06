# SecureNotes CLI client

[![Documentation Status](https://readthedocs.org/projects/secure-notes-client/badge/?version=latest)](https://secure-notes-client.readthedocs.io/en/latest/?badge=latest)

This is a CLI client for [SecureNotes](https://github.com/crazyscientist/secure-notes).

The client contains a separate API interface that can be used for writing more
elaborate clients with Python.

## Usage

```
    usage: securenotes.py [-h] [-u USERNAME] [-p PASSWORD] [-P PASSPHRASE]
                          [-H HOST] [--debug] [-s] [--raw]
                          {list,note,add,edit,delete,share,revoke,listshare} ...

    Secure Notes

    positional arguments:
      {list,note,add,edit,delete,share,revoke,listshare}
                            Commands. For detailed help on command <command> use:
                            securenotes.py <command> -h
        list                List all notes created by or shared with you
        note                View a note
        add                 Add a new note
        edit                Change an existing note owned by you
        delete              Delete a note owned by you
        share               Share a note with another user
        revoke              Revoke the access of another user to your note
        listshare           List all users the note is shared with

    optional arguments:
      -h, --help            show this help message and exit

    Authentication/Server:
      -u USERNAME, --username USERNAME
                            Username
      -p PASSWORD, --password PASSWORD
                            Password
      -P PASSPHRASE, --passphrase PASSPHRASE
                            Phassphrase for encryption; if omitted, password is
                            used
      -H HOST, --host HOST  URL of server

    More options:
      --debug               Activate debug output
      -s, --save-as-defaults
                            Save generic options to config file
      --raw                 Show unformatted content

```