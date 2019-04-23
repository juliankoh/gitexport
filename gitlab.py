import os
import tarfile
import shutil
import logging

logger = logging.getLogger('cli')


class ExportDestination:
    def __init__(self, token, user_data_dir):
        self.token = token
        self.user_data_dir = user_data_dir

    def untar_file(self, filepath):
        filename = os.path.basename(filepath)
        repo_name, _ = filename.rsplit('.', 1)
        extraction_dir = os.path.join(
            self.user_data_dir, f'extract__{repo_name}')

        # if extraction dir exists
        # just remove and start over
        if os.path.exists(extraction_dir):
            shutil.rmtree(extraction_dir)
            os.mkdir(extraction_dir)

        tar = tarfile.open(filepath)
        tar.extractall(path=extraction_dir)
        tar.close()
        logger.debug('Extracted to directory '+extraction_dir)


class Gitlab(ExportDestination):
    def export(self, filepath):
        self.untar_file(filepath)
        # next, we do
        # 1. create gitlab repo
        # 2. push to gitlab repo
