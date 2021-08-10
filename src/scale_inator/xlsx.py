from numpy import float32, uint8
import os
import re
import pandas
try:
    from . import data
except ImportError:
    import data


def create_xlsx():
    '''
    Create xlsx from csv files.
    '''

    csv_files = []
    csvregex = re.compile("data-([0-9]{4})([0-9]{2})([0-9]{2}).csv")

    for entry in os.listdir(data.xdg_data_dir()):
        if not csvregex.fullmatch(entry):
            continue
        csv_files = csv_files + [os.path.join(data.xdg_data_dir(), entry)]

    try:
        csv_combined = pandas.concat(
            [
                pandas.read_csv(
                    file,
                    header=None,
                    parse_dates=[3],
                    dtype={
                        "KG": float32,
                        "KoppaID": uint8,
                        "CollectorID": uint8
                    },
                    names=["KG", "KoppaID", "CollectorID", "Date"]
                ) for file in csv_files
            ],
            ignore_index=True
        )
    except ValueError:
        raise ValueError("CSV column has incorrect data")

    summersum = pandas.DataFrame(columns=["Kerääjä ID", "Paino"])
    summersum = summersum.astype({"Kerääjä ID": uint8, "Paino": float32})

    for id in csv_combined["CollectorID"].unique():
        summersum = summersum.append(
            pandas.DataFrame(
                [
                    {
                        "Kerääjä ID": id,
                        "Paino": csv_combined.where(
                            csv_combined["CollectorID"] == id
                        )["KG"].sum()
                    }
                ]
            ).astype(
                {
                    "Kerääjä ID": uint8,
                    "Paino": float32
                }
            ),
            ignore_index=True
        )

    location = os.path.join(data.xdg_data_dir(), "mansikanpoiminta.xlsx")

    writer = pandas.ExcelWriter(location, engine="xlsxwriter")
    summersum.to_excel(
        writer,
        sheet_name="Koko kesän kerätty määrä",
        index=False
    )

    workbook = writer.book
    worksheet = writer.sheets["Koko kesän kerätty määrä"]

    # Must escape g in format so that excel doesnt reject it
    kilogram_format = workbook.add_format(
        {
            "num_format": "0.00k\g"  # noqa: W605
        }
    )

    worksheet.set_column("A:A", len("Kerääjä ID"))
    worksheet.set_column("B:B", 10, kilogram_format)  # arbitary width

    workbook.close()
