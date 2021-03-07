from plot_builder import build_plot
from report_data_extractor import ReportDataExtractor
from quotes_data_extractor import QuotesDataExtractor
import os


headers = ["Total Revenue", "Total Operating Expense", "Interest Expense"]
data_dir = "./data"
output_dir = "./output"

with open("input.txt") as f:
    for ticker in f.read().splitlines():
        print (f"Processing {ticker} ")
        report_data = ReportDataExtractor(f"./data/{ticker}.xlsx", headers).get_json_data()
        quotes_file = ""
        for f in os.listdir(data_dir):
            if f.startswith(f"{ticker} Price History"):
                quotes_file = f
                break
        if not f:
            print("No quotes found for {ticker}")
            continue

        quotes_data = QuotesDataExtractor(f"{data_dir}/{quotes_file}").get_json_data()

        print(report_data)
        print(quotes_data)

        # Removing all quotes, that, is earlier than first report
        if report_data and quotes_data:
            first_report_date = report_data[0]

        build_plot(report_data, quotes_data, headers, output_dir, ticker)

print("Done!")