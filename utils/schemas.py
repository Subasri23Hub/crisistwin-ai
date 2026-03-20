from typing import List
from pydantic import BaseModel, Field, ValidationError


class CrisisAnalysis(BaseModel):
    executive_summary: str = Field(default="")
    crisis_type: str = Field(default="")
    severity: str = Field(default="")
    stakeholders: List[str] = Field(default_factory=list)
    top_risks: List[str] = Field(default_factory=list)
    immediate_actions: List[str] = Field(default_factory=list)
    response_24h: List[str] = Field(default_factory=list)
    response_7d: List[str] = Field(default_factory=list)
    response_30d: List[str] = Field(default_factory=list)
    communication_draft: str = Field(default="")
    recovery_strategy: List[str] = Field(default_factory=list)
    evidence_used: List[str] = Field(default_factory=list)
    confidence: str = Field(default="")

    @classmethod
    def safe_parse(cls, data: dict):
        try:
            return cls(**data)
        except ValidationError:
            normalized = {}
            for field_name in cls.model_fields:
                value = data.get(field_name)
                expected = cls.model_fields[field_name].annotation
                if expected == str:
                    normalized[field_name] = "" if value is None else str(value)
                else:
                    if isinstance(value, list):
                        normalized[field_name] = [str(v) for v in value]
                    elif value is None or value == "":
                        normalized[field_name] = []
                    else:
                        normalized[field_name] = [str(value)]
            return cls(**normalized)
