from pydantic import BaseModel, Field, model_validator
from typing import Any
import json
from .paths import PROJECT_DIR, Path


class GameConfig(BaseModel):
    highscore_filename: str = Field(default=PROJECT_DIR / "scores.json")
    level: list[str] = Field(
        min_length=1,
        default=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        )
    lives: int = Field(gt=0, default=3)
    pacgum: int = Field(gt=4, default=42)
    points_per_pacgum: int = Field(ge=0, default=10)
    points_per_super_pacgum: int = Field(ge=0, default=50)
    points_per_ghost: int = Field(ge=0, default=200)
    width: int = Field(gt=5, le=40, default=15)
    height: int = Field(gt=5, le=40, default=15)
    seed: int = Field(ge=0, default=42)
    level_max_time: int = Field(
        gt=0,
        description="Max time per level, in seconds",
        default=90
        )

    model_config = {"extra": "ignore"}

    def __init__(self, config_file_path: str | None = None) -> None:
        if config_file_path:
            data = self._read_file(config_file_path)
            super().__init__(**data)
        else:
            super().__init__()

    @staticmethod
    def _read_file(config_file_path: Path) -> Any:
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
                if (line.startswith("#") or line.startswith("//") or
                   (line.startswith("/*") and "*/" in line)):
                    continue
                elif line.startswith("/*") and "*/" not in line:
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

        if not isinstance(json_data, dict):
            print("Config error: the file must contain a JSON object { ... }")
            print("Using default configuration")
            json_data = {}
        return json_data

    @model_validator(mode="after")
    def _check_config(self) -> "GameConfig":
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
