import yaml

from gip import logger

LOG = logger.get_logger(__name__)

def parse_requirements_file(path):
    """Parse requirements

    :param requirements_file: path to yamlfile
    :type requirements_file: pathlib.Path

    :rtype: object
    """
    try:
        file_stream = open(path, 'r')
    except OSError as e:
        LOG.exception(e)
    else:
        try:
            return yaml.safe_load(file_stream)
        except yaml.YAMLError as e:
            LOG.exception(e)
        finally:
            file_stream.close()
