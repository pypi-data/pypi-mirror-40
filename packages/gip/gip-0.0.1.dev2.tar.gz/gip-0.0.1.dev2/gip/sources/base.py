import os
import tarfile
from urllib.parse import urlsplit

from gip import logger

LOG = logger.get_logger(__name__)


class Source():
    """ Superclass which interfaces all the sources """

    def get_archive(self, repo, version):
        raise NotImplementedError

    def extract_archive(self, src, dest, name, remove_src=True):
        """ Extract archive to destination, zip and tar supported """
        if tarfile.is_tarfile(src):
            archive = tarfile.open(src)
            archive.extractall(path=dest)
            if remove_src:
                os.unlink(src)
            if name:
                extracted_folder_name = archive.getmembers()[0].name
                os.rename(
                    src=dest.joinpath(extracted_folder_name),
                    dst=dest.joinpath(name)
                )
        else:
            LOG.warn("Downloaded archive is not a valid archive: {}".format(src))
