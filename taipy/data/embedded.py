import json
from typing import Any, Dict, Optional

from taipy.data.data_source import DataSource
from taipy.data.scope import Scope
from taipy.exceptions import MissingRequiredProperty


class EmbeddedDataSource(DataSource):
    __TYPE = "embedded"

    def __init__(
        self, name: str, scope: Scope, id: Optional[str] = None, properties: Dict = {}
    ):
        super().__init__(name, scope, id, data=properties.get("data"))

    @classmethod
    def create(cls, name: str, scope: Scope, data: Any):
        return EmbeddedDataSource(name, scope, None, {"data": data})

    @classmethod
    def type(cls) -> str:
        return cls.__TYPE

    def preview(self):
        print(f"{self.properties.get('data')}", flush=True)

    def get(self, query=None):
        """
        Temporary function interface, will be remove
        """
        return self.properties.get("data")

    def write(self, data):
        """
        Temporary function interface, will be remove
        """
        self.properties["data"] = data

    def to_json(self):
        return json.dumps(
            {
                "name": self.name,
                "type": "embedded",
                "scope": self.scope.name,
                "data": self.data,
            }
        )

    @staticmethod
    def from_json(data_source_dict):
        return EmbeddedDataSource.create(
            name=data_source_dict.get("name"),
            scope=Scope[data_source_dict.get("scope")],
            data=data_source_dict.get("data"),
        )