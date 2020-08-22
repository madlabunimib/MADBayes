from __future__ import annotations

from typing import TYPE_CHECKING

from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from typing import Any, List
    from ..backend import BayesianNetwork


class InferenceSystem(ABC):

    @abstractmethod
    def query(self, variables: List[str], evidence: Any, method: str) -> Any:
        pass
