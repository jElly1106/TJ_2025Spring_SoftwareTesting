from typing import List, Optional, Any
from pydantic import BaseModel, validator

class PlotDetails(BaseModel):
    plotId: str
    plotName: str
    plantId: str
    plantName: str
    plantFeature: str
    plantIconURL: str
    logs: List[Any] = []
    
    @validator('logs', pre=True)
    def validate_logs(cls, v):
        if v is None:
            return []
        return v
    
    class Config:
        extra = 'forbid'