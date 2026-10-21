
from pydantic import BaseModel, Field, model_validator, ValidationError
from pathlib import Path
from typing import Any
import json


class GameConfig(BaseModel):
    level: list[int] = Field(min_length=1)
    lives: int = Field(gt=0)
    pacgum: int = Field(ge=0)
    points_per_pacgum: int = Field(ge=0)
    points_per_super_pacgum: int = Field(ge=0)
    points_per_ghost: int = Field(ge=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    seed: int
    level_max_time: int = Field(gt=0,
                                description="Max time per level, in seconds")

    @staticmethod
    def default_settings() -> dict[str, Any]:
        return {
            "level": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            "lives": "3",
            "pacgum": "42",
            "points_per_pacgum": "10",
            "points_per_super_pacgum": "50",
            "points_per_ghost": "200",
            "width": "30",
            "height": "35",
            "seed": "42",
            "level_max_time": "90",
        }

    @model_validator(mode="after")
    def check_config(self) -> "GameConfig":
        if len(set(self.level)) != len(self.level):
            raise ValueError("level contains duplicates")
        if any(lvl < 1 for lvl in self.level):
            raise ValueError("level numbers must be >= 1")
        if self.pacgum >= self.width * self.height:
            raise ValueError(
                "pacgum count cannot exceed the number of grid cells")
        return self

    @classmethod
    def load(cls: "GameConfig",
             path: str | Path = "config.json") -> "GameConfig":
        path = Path(path)
        try:
            return cls.check_config(path.read_text())
        except (OSError, ValidationError) as err:
            print(
                f"Invalid or missing config ({err}); using default settings.")
            defaults: dict[str, Any] = GameConfig.default_settings()
            path.write_text(json.dumps(defaults, indent=4))
            return cls.model_validate(defaults)
