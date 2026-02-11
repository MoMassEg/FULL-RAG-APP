from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class Asset(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    id: Optional[ObjectId] = Field(None, alias="_id")
    asset_project_id: ObjectId
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: Optional[int] = Field(default=None, gt=0)
    asset_config: Optional[dict] = Field(default=None)
    asset_pushed_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def get_indexes(cls):
        return [{
            "key": [("asset_project_id", 1)],
            "unique": False,
            "name": "asset_project_id_index_1"
        },
        {
            "key": [("asset_project_id", 1),("asset_name", 1)],
            "unique": True,
            "name": "asset_project_id_asset_name_index_1"
        }
        ]
