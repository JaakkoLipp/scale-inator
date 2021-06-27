from datetime import date
import csv
import os
import re
import xlsxwriter
try:
    from . import data
except ImportError:
    import data


COLLECTOR_AMOUNT = 100  # hard coded for now


def create_xlsx():
    workbook = xlsxwriter.Workbook(
        "test1.xlsx",
        {'constant_memory': True})

    summer_data = workbook.add_worksheet("Summer data")
    day_data = workbook.add_worksheet("Day data")
    raw_data = workbook.add_worksheet("Raw data")

    # Must escape g in format so that excel doesnt reject it
    kilogram_format = workbook.add_format(
        {"num_format": "0.00k\g"})  # noqa: W605

    summer_data.write(0, 0, "Summer sum")
    summer_data.write(0, 1, "Collector ID")

    for collectorID in range(1, COLLECTOR_AMOUNT):
        summer_data.write_formula(
            collectorID,
            0,
            (
                (
                    "=SUMPRODUCT(" +
                    "'Raw data'!C:C=B{}," +
                    "'Raw data'!A:A)"
                ).format(collectorID+1)),
            kilogram_format
        )
        summer_data.write_number(collectorID, 1, collectorID)

    day_data.write(0, 0, "Day sum")
    day_data.write(0, 1, "Collector ID")
    day_data.write(0, 2, "Day")

    dates = []
    csvregex = re.compile("data-([0-9]{4})([0-9]{2})([0-9]{2}).csv")
    for entry in os.listdir(data.xdg_data_dir()):
        match = csvregex.fullmatch(entry)
        dates = dates + [date(
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)))]
    re.purge()
    dayformat = workbook.add_format(
        {"num_format": "dd.m.yyyy"})

    row_num = 1
    for day in dates:
        for collectorID in range(1, COLLECTOR_AMOUNT):
            real_row = row_num + 1
            day_data.write_formula(
                row_num,
                0,
                (
                    (
                        "=SUMPRODUCT(" +
                        "'Raw data'!C:C=B{}," +
                        "'Raw data'!D:D=C{}," +
                        "'Raw data'!A:A)"
                    ).format(real_row, real_row)),
                kilogram_format
            )
            day_data.write_number(row_num, 1, collectorID)
            day_data.write_datetime(row_num, 2, day, dayformat)
            row_num += 1

    dayregex = re.compile("([0-9]{2})\.([0-9]{2})\.([0-9]{4})")  # noqa: W605
    row_num = 1
    for entry in os.listdir(data.xdg_data_dir()):
        if not csvregex.fullmatch(entry):
            continue
        csvfile = open(os.path.join(data.xdg_data_dir(), entry), "rt")
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            match = dayregex.fullmatch(row[3])
            day = date(
                int(match.group(3)),
                int(match.group(2)),
                int(match.group(1)))
            raw_data.write_number(
                row_num,
                0,
                float(row[0])
            )
            raw_data.write_number(
                row_num,
                1,
                int(row[1])
            )
            raw_data.write_number(
                row_num,
                2,
                int(row[2])
            )
            raw_data.write_datetime(
                row_num,
                3,
                day,
                dayformat
            )
            row_num += 1

        csvfile.close()
    workbook.close()


if __name__ == "__main__":
    create_xlsx()
