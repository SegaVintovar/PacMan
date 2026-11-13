
from pydantic import BaseModel, Field, model_validator, ValidationError
from pathlib import Path
from typing import Any
import json


# read the file, then text.splitlines()
# loop through lines, strip them and exclude that starts with "#" or "//" or /* */


class GameConfig(BaseModel):
    highscore_filename: str = Field(min_length=5, default="scores.json")
    level: list[int] = Field(
        min_length=1,
        default=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        )
    lives: int = Field(gt=0, default=3)
    pacgum: int = Field(ge=0, default=42)
    points_per_pacgum: int = Field(ge=0, default=10)
    points_per_super_pacgum: int = Field(ge=0, default=50)
    points_per_ghost: int = Field(ge=0, default=200)
    width: int = Field(gt=0, default=15)
    height: int = Field(gt=0, default=15)
    seed: int = Field(ge=0, default=42)
    level_max_time: int = Field(
        gt=0,
        description="Max time per level, in seconds",
        default=90
        )

    model_config = {"extra": "ignore"}

    def __init__(self, config_file_path: str) -> None:
        data = self._read_file(config_file_path)
        super().__init__(**data)

    @staticmethod
    def _read_file(config_file_path: str) -> Any:
        data = ""
        multiline_comment = False
        try:
            with open(config_file_path, "r") as file:
                data_lines = file.read().splitlines(keepends=True)
        except Exception as e:
            print(f"Could not read config file: {str(e)}")
            data_lines = []
        for line in data_lines:
            line = line.strip()
            if not multiline_comment:
                if line.startswith("#") or line.startswith("//"):
                    continue
                elif line.startswith("/*"):
                    # then we are looking for endwith("*/")
                    multiline_comment = True
                    continue
                else:
                    data += line + "\n"
            else:
                if line.endswith("*/"):
                    multiline_comment = False
        try:
            json_data = json.loads(data)
        except (OSError, ValueError) as e:
            print("\nJSON file load error:", str(e))
            print("\nFalling back to the default values")
            json_data = {}
        return json_data

    @staticmethod
    def default_settings() -> dict[str, Any]:
        return {
            "highscore_filename": "scores.json",
            "level": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
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
        if not self.highscore_filename.endswith(".json"):
            raise ValueError("highscore file has to be JSON format")
        if len(set(self.level)) != len(self.level):
            raise ValueError("level contains duplicates")
        if not self.level:
            raise ValueError("there has to be at least one level")
        if self.pacgum >= self.width * self.height:
            raise ValueError(
                "pacgum count cannot exceed the number of grid cells")
        if self.width < 10:
            raise ValueError("map width needs to be at least 10")
        if self.height < 10:
            raise ValueError("map height needs to be at least 10")
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
