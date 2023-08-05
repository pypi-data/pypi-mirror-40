from pyecharts import Line, Bar


def plot_line(df, name, columns=[], colors=[], **kwargs):
    line = Line(name)
    for column in columns:
        line.add(column, df.index.astype(str).tolist(), df[column].tolist(),
                 is_symbol_show=False, is_label_emphasis=False, **kwargs)
    if colors:
        [line._option['series'][i].update(
            dict(itemStyle=dict(color=color))) for i, color in enumerate(colors)]
    return line


def plot_bar(df, name, columns=[], colors=[], pos='10%', **kwargs):
    bar = Bar(name, title_top=pos)
    for column in columns:
        bar.add(column, df.index.astype(str).tolist(), df[column].tolist(),
                is_label_emphasis=False, legend_pos=pos, **kwargs)
    if colors:
        [bar._option['series'][i].update(
            dict(itemStyle=dict(color=color))) for i, color in enumerate(colors)]
    return bar
