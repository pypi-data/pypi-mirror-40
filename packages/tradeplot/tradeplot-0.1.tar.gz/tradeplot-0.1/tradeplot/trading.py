import numpy as np
from pyecharts import EffectScatter, Line


def add_efs(es, name, data, color, rotate):
    es.add(name, [], [], symbol_size=15, effect_scale=3,
           effect_period=3, symbol="pin")
    es._option['series'][-1]['data'] = data
    es._option['series'][-1]['symbolRotate'] = rotate
    es._option['series'][-1]['label']['emphasis']._config.update(
        dict(formatter='pl: {@[3]}'))
    es._option['series'][-1]['color'] = color
    return es


def add_pair_efs(es, side, trades, entry_color, cover_coler):
    es = add_efs(es, '{}_entry'.format(side),
                 [[trade[0]['x'], trade[0]['y'], trade[0]['value'], trade[3]]
                     for trade in trades],
                 entry_color, rotate=180 if side == 'long' else 0)
    es = add_efs(es, '{}_cover'.format(side),
                 [[trade[1]['x'], trade[1]['y'], trade[1]['value'], trade[3]]
                     for trade in trades],
                 cover_coler, rotate=0 if side == 'long' else 180)
    return es


def trade_line(name='esline', trades=[], all_dates=[], win_color='rgba(0,255,255,0.8)', loss_color='rgba(255,0,255,0.8)'):
    esline = Line('esline')
    for trade in trades:
        entry_date, cover_date, entry_p, cover_p = trade[0][
            'x'], trade[1]['x'], trade[0]['y'], trade[1]['y']
        entry_index, cover_index = all_dates.index(
            entry_date), all_dates.index(cover_date)
        xs = all_dates[entry_index: cover_index + 1]
        ys = np.linspace(entry_p, cover_p, num=len(xs)).tolist()
        win_loss_point = trade[3]
        color = win_color if win_loss_point > 0 else loss_color
        esline.add(
            f'{entry_date}->{cover_date}: {trade[2]}', [], [], is_symbol_show=False)
        esline._option['series'][-1]['data'] = [[x, y, win_loss_point]
                                                for x, y in zip(xs, ys)]
        esline._option['series'][-1]['lineStyle']['normal']._config.update(
            {'color': color, 'width': 2, 'type': 'dashed'})
        esline._option['series'][-1]['label']['emphasis']._config.update(
            {'formatter': '{@[2]}', 'color': color})
        esline._option['series'][-1].update(clipOverflow=False)
        esline._option['series'][-1]['zlevel'] = 1
    esline._option['legend'][0]['data'] = []
    return esline


def plot_trades(trades, all_dates,
                entry_long_color='rgba(255, 0, 0, 0.75)', cover_long_color='rgba(0, 255, 50, 0.6)',
                entry_short_color='rgba(0, 255, 0, 0.75)', cover_short_color='rgba(255, 0, 50, 0.6)',
                win_color='rgba(0,255,255,0.8)', loss_color='rgba(255,0,255,0.8)'):
    long_trades = [trade for trade in trades if trade[2] == 'long']
    short_trades = [trade for trade in trades if trade[2] == 'short']
    es = EffectScatter()
    es = add_pair_efs(es, 'long', long_trades,
                      entry_long_color, cover_long_color)
    es = add_pair_efs(es, 'short', short_trades,
                      entry_short_color, cover_short_color)
    esline = trade_line(trades=trades, all_dates=all_dates,
                        win_color=win_color, loss_color=loss_color)
    return es, esline
