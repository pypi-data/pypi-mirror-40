![evernotezimport](https://git.kotur.org/kotnik/evernotezimport/raw/master/logo.png)

This package takes Evernote notebook export and imports it into Zim directory.

### Installation

Install it just for yourself:

```
pip install --user evernotezimport
```

After that `zimport` command will be ready to help you.

### Usage

Export Notebook from Evernote desktop application (sadly, you can not do this from the web interface). Take that file and tell `zimport` where to expand it, somewhere in Zim directory. For example:

```
zimport --zim /path/to/zim/notebook/root/Everjokes /path/to/evernote/export/notebook.enex
```

### What's missing?

It is rough on the edges. Tags are not supported properly and Evernote HTML is just being stripped leaving you with pure text of your note.

### Developing

It's easy. Clone this repository and:

```
virtualenv .env
source .env/bin/activate
pip install -e .
```

Work on repository directly, and use `zimport` command to test. Thank you.
