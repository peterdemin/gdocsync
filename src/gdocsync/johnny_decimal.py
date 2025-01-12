import glob
import os
from dataclasses import dataclass

from .regexes import RE_JOHNNY_DECIMAL, RE_PUNCT


@dataclass
class JohnnyDecimal:
    SLUG_DELIMITER = "-"

    category: str
    index: str
    name: str

    @classmethod
    def parse(cls, name: str) -> "JohnnyDecimal":
        match_obj = RE_JOHNNY_DECIMAL.match(name)
        if match_obj is None:
            raise ValueError(f"{name} does not follow Johnny Decimal notation.")
        groups = match_obj.groups()
        return cls(
            category=groups[0],
            index=groups[1],
            name=groups[2],
        )

    @staticmethod
    def is_valid(name: str) -> bool:
        return bool(RE_JOHNNY_DECIMAL.match(name))

    def fit_path(self, base_dir: str) -> str:
        parent_dir_expr = os.path.join(base_dir, f"{self.category}*")
        parent_dir_candidates = glob.glob(parent_dir_expr)
        if len(parent_dir_candidates) == 1:
            parent_dir = parent_dir_candidates[0]
            return os.path.join(parent_dir, self.file_name)
        full_pattern = os.path.join(parent_dir_expr, self.file_name)
        raise ValueError(
            f"Could not find unambiguous fit for {full_pattern}. "
            f"Candidates: {parent_dir_candidates}"
        )

    @property
    def file_name(self) -> str:
        return f"{self.index}{self.SLUG_DELIMITER}{self.slug}"

    @property
    def slug(self) -> str:
        return RE_PUNCT.sub(self.SLUG_DELIMITER, self.name).lower()

    @property
    def full_index(self) -> str:
        return f"{self.category}.{self.index}"
