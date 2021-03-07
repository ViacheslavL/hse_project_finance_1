
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def build_plot(reports, quotes, headers, output_dir, ticker):
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    years_fmt = mdates.DateFormatter('%Y')

    fig, ax = plt.subplots()
    fig.subplots_adjust(right=0.75)

    quotes_x_data = list(map(lambda x: datetime.strptime(x["date"], '%d-%b-%Y'), quotes))
    quotes_y_data = [x["close"] for x in quotes]
    ax.plot(quotes_x_data, quotes_y_data, "b-", label="Close")

    styles = "r-, g-, c-, m-, y-"
    offset = 1
    for i, h in enumerate(headers):
        reports_plt = ax.twinx()

        reports_x_data = list(map(lambda x: datetime.strptime(x["date"], '%d-%b-%Y'), reports))
        reports_y_data = [x["values"].get(h) for x in reports]

        p, = reports_plt.plot(reports_x_data, reports_y_data, styles[i], label=h)
        reports_plt.set_ylabel(h)
        reports_plt.spines["right"].set_position(("axes", offset))
        offset += 0.2
        reports_plt.spines["right"].set_visible(True)
        reports_plt.yaxis.label.set_color(p.get_color())
        reports_plt.tick_params(axis="y", colors=p.get_color())

    make_patch_spines_invisible(ax)

    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_fmt)
    ax.xaxis.set_minor_locator(months)
    ax.set_ylabel("Close")

    datemin = datetime.strptime(quotes[0]["date"], "%d-%b-%Y")
    datemax = datetime.strptime(quotes[-1]["date"], "%d-%b-%Y")
    ax.set_xlim(datemin, datemax)
    ax.yaxis.label.set_color("blue")
    ax.tick_params(axis="y", colors="blue")

    ax.format_xdata = mdates.DateFormatter('%d-%b-%Y')
    ax.format_ydata = lambda x: x["close"]
    ax.grid(True)

    fig.autofmt_xdate()
    plt.title(ticker)
    plt.savefig(f'{output_dir}/{ticker}.png')
    plt.close(fig)