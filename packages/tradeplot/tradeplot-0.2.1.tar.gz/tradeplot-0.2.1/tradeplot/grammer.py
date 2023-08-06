from copy import deepcopy


class Base:
    __slots__ = ()

    def keys(self):
        return self.__slots__

    def __getitem__(self, key):
        return getattr(self, key)

    def __gen_container(self):
        return ', '.join(['{}={!r}'.format(k, v) for k, v in {**self}.items()])

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.__gen_container())


class PlotKind(Base):
    __slots__ = ('kind', 'columns', 'grid', 'config')

    def __init__(self, kind='kline', columns=['open', 'close', 'high', 'low'], grid=0, config={}):
        self.kind = kind
        self.columns = columns
        self.grid = grid
        self.config = config


class PlotGrammer(Base):
    def __init__(self, grids={0: 100, }, **kwargs):
        self.__slots__ = tuple([k for k in kwargs] + ['grids'])
        self._grids = grids
        self.calculate()
        [setattr(self, k, v) for k, v in kwargs.items()]

    def calculate(self, fig_height=800):
        grids = deepcopy(self._grids)
        assert sum(grids.values()) == 100, 'Grids sum must 100%'
        rescale = (100 - (60 / fig_height) * 100 * 2) / 100
        top_fit = (60 / fig_height) * 100
        top, bottom = (0, 0)
        for grid, val in list(grids.items()):
            grids.update({grid: dict(top=(top + bottom) * rescale + top_fit + 2 if (top + bottom) else 0,
                                     bottom=(100 - (bottom + val)) * rescale + top_fit + 2 if (100 - (bottom + val)) else 0)})
            bottom += val
        self.grids = grids

    def __gen_container(self):
        return ',\n    '.join(['{}={!r}'.format(k, v) for k, v in {**self}.items()])

    def __repr__(self):
        return '{}(\n    {}\n)'.format(self.__class__.__name__, self.__gen_container())
