import os
import re
import pandas
try:
    from . import data
except ImportError:
    import data


def create_xlsx():
    files = []
    csvregex = re.compile("data-([0-9]{4})([0-9]{2})([0-9]{2}).csv")
    for entry in os.listdir(data.xdg_data_dir()):
        if not csvregex.fullmatch(entry):
            continue
        files = files + [os.path.join(data.xdg_data_dir(), entry)]
    dataframe = pandas.concat([pandas.read_csv(
        f, header=None,
        parse_dates=[3],
        names=["KG", "KoppaID", "CollectorID", "Date"]) for f in files],
                              ignore_index=True)

    # Yes, am iterating pandas dataframes. It works for now :|
    summersum = pandas.DataFrame(columns=['CollectorID', 'KG'])
    summersum = summersum.astype({'CollectorID': int, 'KG': float})
    max_collector = dataframe["CollectorID"].max()
    for col_num in range(1, max_collector+1):
        temp = dataframe.copy()
        temp = temp.query('(CollectorID == ' + str(col_num) + ')')
        if temp.empty:
            continue
        else:
            summersum = summersum.append(
                {
                    'CollectorID': col_num,
                    'KG': temp["KG"].sum()
                },
                ignore_index=True)
    pandas.to_numeric(summersum['CollectorID'], downcast='integer')

    location = os.path.join(data.xdg_data_dir(), "mansikanpoiminta.xlsx")

    writer = pandas.ExcelWriter(location, engine="xlsxwriter")
    summersum.to_excel(writer, sheet_name="Summer sum", index=False)

    workbook = writer.book
    worksheet = writer.sheets['Summer sum']

    # Must escape g in format so that excel doesnt reject it
    kilogram_format = workbook.add_format(
        {"num_format": "0.00k\g"})  # noqa: W605

    workbook.close()
