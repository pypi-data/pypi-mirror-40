import logging
from queue import Queue
from .PieceManager import PieceManager
from .Torrent import Torrent
from .Client import Client
from .utils import clean_path, read_timestamp, timestamp_is_within_30_days, filenames_present, write_timestamp

def get(at_hash, datastore=None, urls=[], showlogs=False):
    logging.getLogger().setLevel(logging.CRITICAL)
    if showlogs:
        logging.getLogger().setLevel(level=logging.INFO)

    torrent = Torrent(at_hash, datastore)
    torrent.urls = torrent.urls + urls
    path = torrent.datastore + torrent.contents['info']['name']

    # Check timestamp
    timestamp = read_timestamp(at_hash)
    if timestamp_is_within_30_days(timestamp) and filenames_present(torrent):
        return path

    # Check if downloaded and finished
    piece_manager = PieceManager(torrent)
    piece_manager.check_disk_pieces()
    downloaded_amount = piece_manager.check_finished_pieces()
    if float(downloaded_amount) / torrent.total_length == 1.0:
        return path

    # Download it
    Client(torrent, downloaded_amount, piece_manager).start()
    write_timestamp(at_hash)
    return path
