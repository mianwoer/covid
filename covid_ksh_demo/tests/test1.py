import pyecharts.options as opts
from pyecharts.charts import Line


def line_base() -> Line:
    attr = ["10.13", "10.14", "10.15", "10.16", "10.17", "\
    10.18"]
    v1 = [1650, 1700, 1461, 1350, 1100, 1500]
    v2 = [1020, 575, 400, 350, 330, 480]

    c = (
        Line()
            .add_xaxis(attr)
            .add_yaxis("成都fly北京", v1)
            .add_yaxis("成都fly昆明", v2)
            .set_global_opts(title_opts=opts.TitleOpts(title="航班价格折线图"))
    )
    return c


m = line_base()
m.render('line.html')
