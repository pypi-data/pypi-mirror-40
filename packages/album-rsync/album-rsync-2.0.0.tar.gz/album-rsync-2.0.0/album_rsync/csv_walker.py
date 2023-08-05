import time
import logging
from rx import Observable
from .walker import Walker
from .root_folder_info import RootFolderInfo
from .utils import unpack

logger = logging.getLogger(__name__)

class CsvWalker(Walker):

    def __init__(self, config, storage):
        self._config = config
        self._storage = storage

    def walk(self):
        start = time.time()

        # Create source stream
        folders = Observable.from_(self._storage.list_folders())
        if self._config.root_files:
            folders = folders.start_with(RootFolderInfo())
        if self._config.list_folders:
            print("Folder")
            if self._config.list_sort:
                folders = folders.to_sorted_list(key_selector=lambda folder: folder.name) \
                    .flat_map(lambda x: x)
            folders.subscribe(on_next=lambda folder: print(folder.name) if folder else '',
                              on_completed=lambda: self._print_summary(time.time() - start))
        else:
            print("Folder, Filename, Checksum")
            # Expand folder stream into file stream
            files = folders.concat_map(lambda folder: Observable.from_((fileinfo, folder) for fileinfo in self._storage.list_files(folder)))
            # Print each file
            if self._config.list_sort:
                files = files.to_sorted_list(key_selector=lambda x: "{} {}".format(x[1].name, x[0].name)) \
                    .flat_map(lambda x: x)
            files.subscribe(on_next=unpack(lambda fileinfo, folder: self._print_file(folder, fileinfo)),
                            on_completed=lambda: self._print_summary(time.time() - start))


    def _print_file(self, folder, fileinfo):
        print(f"{folder.name if folder else ''}, {fileinfo.name}, {fileinfo.checksum}")

    def _print_summary(self, elapsed):
        logger.info(f"\ndone in {round(elapsed, 2)} sec")
