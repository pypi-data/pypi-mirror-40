from pyecharts import Kline


def set_kline_color(kline_series, up_color, down_color,
                    up_board_color, down_board_color):
    kline_series['itemStyle'] = {'color': up_color, 'color0': down_color,
                                'borderColor': up_board_color,
                                'borderColor0': down_board_color}
    return kline_series


def plot_kline(df_ohlc, chart_name='Kline', symbol_name='', size=(800, 400),
               ochl_columns=['open', 'close', 'high', 'low'],
               zoom_percent_range=(90, 100), legend_pos='10%',
               datazoom_share_axis=[0, ], tooltip_bg_color='rgba(50,50,50,0.7)',
               up_color='rgba(255,0,0,0.9)', down_color='rgba(0,255,0,0.9)',
               up_board_color='rgba(255,0,0,0.9)',
               down_board_color='rgba(0,255,0,0.9)'):
    kline = Kline(chart_name, is_animation=False, )
    kline.add(symbol_name, df_ohlc.index.astype(str).tolist(),
              df_ohlc[ochl_columns].values.tolist(),
              datazoom_type='both', is_datazoom_show=True,
              datazoom_range=zoom_percent_range,
              legend_pos=legend_pos,
              datazoom_xaxis_index=datazoom_share_axis)
    kline._option['series'][0] = set_kline_color(kline._option['series'][0], up_color, down_color,
                                                 up_board_color, down_board_color)
    kline._option['tooltip']._config = dict(trigger='axis',
                                            triggerOn='mousemove|click',
                                            axisPointer={'type': 'cross'},
                                            textStyle={'fontSize': 14},
                                            backgroundColor=tooltip_bg_color,
                                            borderColor='#333',
                                            borderWidth=0)
    return kline
