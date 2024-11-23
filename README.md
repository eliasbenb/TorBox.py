# TorBox.py

A Python wrapper for the TorBox API.

## Installation

```bash
pip install torbox # pip install git+https://github.com/eliasbenb/TorBox.py.git # for the bleeding edge version
```

## Supported API endpoints

| Endpoint                             | Supported | Tested |
| ------------------------------------ | --------- | ------ |
| `/api/torrents/createtorrent`        | ✔️         |        |
| `/api/torrents/controltorrent`       | ✔️         |        |
| `/api/torrents/controlqueued`        |           |        |
| `/api/torrents/requestdl`            | ✔️         |        |
| `/api/torrents/mylist`               | ✔️         | ✔️      |
| `/api/torrents/checkcached`          | ✔️         | ✔️      |
| `/api/torrents/storesearch`          | ✔️         |        |
| `/api/torrents/search`               | ❌         | ✔️      |
| `/api/torrents/exportdata`           | ❌         | ✔️      |
| `/api/torrents/torrentinfo`          | ✔️         | ✔️      |
| `/api/torrents/getqueued`            | ✔️         | ✔️      |
| `/api/usenet/createusenetdownload`   | ✔️         |        |
| `/api/usenet/controlusenetdownload`  | ✔️         |        |
| `/api/usenet/requestdl`              | ✔️         |        |
| `/api/usenet/mylist`                 | ✔️         |        |
| `/api/usenet/checkcached`            | ✔️         |        |
| `/api/webdl/createwebdownload`       | ✔️         |        |
| `/api/webdl/controlwebdownload`      | ✔️         |        |
| `/api/notifications/rss`             |           |        |
| `/api/notifications/mynotifications` |           |        |
| `/api/notifications/clear`           |           |        |
| `/api/user/refreshtoken`             |           |        |
| `/api/user/me`                       |           |        |
| `/api/user/addreferral`              |           |        |
| `/api/rss/addrss`                    | ✔️         |        |
| `/api/rss/controlrss`                | ✔️         |        |
| `/api/rss/modifyrss`                 | ✔️         |        |
| `/api/integration/googledrive`       |           |        |
| `/api/integration/dropbox`           |           |        |
| `/api/integration/onedrive`          |           |        |
| `/api/integration/gofile`            |           |        |
| `/api/integration/1fichier`          |           |        |
| `/api/integration/jobs`              |           |        |
| `/api/stats`                         | ✔️         | ✔️      |

## Usage

### Python Library

```python
from torbox import TorBox

# Initialize the TorBox object
torbox = TorBox(api_key="YOUR_API_KEY")

# List torrents
torrents = torbox.torrents.list()

# List all queued torrents
queued_torrents = torbox.torrents.list_queued()

# Create a torrent
torbox.torrents.create(magnet="magnet:?xt=urn:btih:...")
torbox.torrents.create(torrent_file="path/to/file.torrent")
```

### CLI

To use the CLI, run the following for help:

```bash
torbox --help
```

To get help for a specific command, run:

```bash
torbox --api-key=<API_KEY> <COMMAND> --help
```

Commands will follow the following format:

```bash
torbox --api-key=<API_KEY> <OPTIONS> <COMMAND> <COMMAND_OPTIONS>
```

#### Example Usage

```bash
torbox --api-key=<API_KEY> --pretty torrents list_queued
torbox --api-key=<API_KEY> torrents list --bypass_cache
torbox -k <API_KEY> torrents create --magnet="magnet:?xt=urn:btih:..."
torbox -k <API_KEY> torrents create --name="Test Torrent" --torrent_file="path/to/test.torrent"
torbox -k <API_KEY> torrents info --torrent_hash <TORRENT_HASH>
```
