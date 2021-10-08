__all__ = ["ConfigurationManager"]

from .data_manager_configuration import DataManagerConfiguration
from .task_scheduler_configuration import TaskSchedulerConfiguration
from .toml_serializer import TomlSerializer


class ConfigurationManager:
    TASK_SCHEDULER_CONFIGURATION_NODE_NAME = "TASK"
    DATA_MANAGER_CONFIGURATION_NODE_NAME = "DATA_MANAGER"

    serializer = TomlSerializer()
    data_manager_configuration = DataManagerConfiguration()
    task_scheduler_configuration = TaskSchedulerConfiguration()

    @classmethod
    def load(cls, filename):
        """
        Load default configuration and merge it with present configurations in filename
        """
        config = cls.serializer.read(filename)
        cls.data_manager_configuration.update(config.get(cls.DATA_MANAGER_CONFIGURATION_NODE_NAME, {}))
        cls.task_scheduler_configuration.update(config.get(cls.TASK_SCHEDULER_CONFIGURATION_NODE_NAME, {}))

    @classmethod
    def export(cls, filename: str):
        """
        Load the current configuration and write it in the filename passed in parameter

        Note: If the file already exists, it is overwritten
        """
        config = {
            cls.DATA_MANAGER_CONFIGURATION_NODE_NAME: cls.data_manager_configuration.export(),
            cls.TASK_SCHEDULER_CONFIGURATION_NODE_NAME: cls.task_scheduler_configuration.export(),
        }
        cls.serializer.write(config, filename)