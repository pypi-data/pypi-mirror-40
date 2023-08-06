from pyecharts import Grid, Overlap
from tradeplot.grammer import PlotKind
from tradeplot.basic import plot_bar, plot_line
from tradeplot.kline import plot_kline
from tradeplot.trading import plot_trades


def trading_plot(df,
                 plot_grammer,
                 figsize=(1200, 800),
                 trades=[],
                 trades_config={}):
    grid = Grid(width=figsize[0], height=figsize[1])
    charts = [Overlap() for g in plot_grammer['grids']]
    plot_grammer.calculate(figsize[1])
    all_dates = df.index.astype(str).tolist()
    for name, plotk in {**plot_grammer}.items():
        if isinstance(plotk, PlotKind):
            if plotk['kind'] == 'kline':
                plot = plot_kline(
                    df,
                    chart_name=name,
                    symbol_name=name,
                    ochl_columns=plotk['columns'],
                    datazoom_share_axis=list(range(len(charts))),
                    **plotk['config'])
            elif plotk['kind'] == 'line':
                plot = plot_line(
                    df, name=name, columns=plotk['columns'], **plotk['config'])
            elif plotk['kind'] == 'bar':
                plot = plot_bar(
                    df,
                    name=name,
                    columns=plotk['columns'],
                    pos="{}%".format(
                        plot_grammer['grids'][plotk['grid']]['top']),
                    **plotk['config'])
            else:
                Exception('Kind: {} not implement.'.format(plotk['kind']))
            charts[plotk['grid']].add(plot)
    if trades:
        es, esline = plot_trades(trades, all_dates, **trades_config)
        charts[0].add(es)
        charts[0].add(esline)
    [
        grid.add(
            charts[g],
            grid_top="{}%".format(vol['top']) if vol['top'] else 60,
            grid_bottom="{}%".format(vol['bottom']) if vol['bottom'] else 60)
        for g, vol in plot_grammer['grids'].items()
    ]
    grid._option.update(axisPointer={'link': {'xAxisIndex': 'all'}})
    return grid
