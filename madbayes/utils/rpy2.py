from __future__ import annotations

from typing import TYPE_CHECKING

import xarray as xa

if TYPE_CHECKING:
    from typing import Any, List

bnlearn = None
gRain = None
utils = None


def rpy2_init() -> None:
    import rpy2.robjects.packages as rpackages
    from rpy2.robjects.vectors import StrVector
    global bnlearn, gRain, utils
    # Initialize RPY2
    utils = rpackages.importr('utils')
    utils.chooseCRANmirror(ind=1)
    # Install packages
    packages = ('bnlearn', 'gRain')
    packages_to_install = [
        x
        for x in packages
        if not rpackages.isinstalled(x)
    ]
    if len(packages_to_install) > 0:
        utils.install_packages(StrVector(packages_to_install))
    # Import packages
    bnlearn = rpackages.importr('bnlearn')
    gRain = rpackages.importr('gRain')


class BNLearnNetwork():

    def as_bn(self):
        return bnlearn.model2network(self.structure())

    def as_grain(self):
        return bnlearn.as_grain(self._network)

    def mutilated(self, **kwargs) -> 'BNLearnNetwork':
        from rpy2.robjects.vectors import ListVector
        model = type(self)()
        model._network = bnlearn.mutilated(
            self._network,
            ListVector(kwargs)
        )
        return model

    def structure(self):
        return bnlearn.modelstring(self._network)

    @classmethod
    def from_bif(cls, path: str) -> None:
        bn = cls()
        bn._network = bnlearn.read_bif(path)
        return bn


class gRainJunctionTree():

    def __init__(self, model: 'BNLearnNetwork' = None) -> None:
        self._network = model

    def query(self, variables: List[str], evidence: Any, method: str) -> Any:
        from rpy2.robjects.vectors import StrVector
        out = gRain.querygrain(
            self._network.mutilated(**evidence).as_grain(),
            nodes=StrVector(variables),
            type=method,
            result='data.frame'
        )
        return self._format_query_output(method, variables, out)

    def _format_query_output(self, method: str, variables: List[str], out) -> List:
        if method == 'marginal':
            return [
                self._format_query_to_xarray([variable], out[i])
                for i, variable in enumerate(variables)
            ]
        return [self._format_query_to_xarray(variables, out)]

    def _format_query_to_xarray(self, variables: List[str], out) -> xa.DataArray:
        import rpy2.robjects as ro
        from rpy2.robjects import pandas2ri
        from rpy2.robjects.conversion import localconverter
        with localconverter(ro.default_converter + pandas2ri.converter):
            out = ro.conversion.rpy2py(out)
        out = out.set_index(variables).to_xarray()
        out = out.to_array().squeeze(['variable'], drop=True)
        return out

    @classmethod
    def from_bif(cls, path: str) -> None:
        return cls(BNLearnNetwork.from_bif(path))
