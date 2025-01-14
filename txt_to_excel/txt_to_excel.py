import pandas as pd
import re
from tabulate import tabulate


def convert_txt_to_excel(txt_fpath: str, excel_fpath: str) -> pd.DataFrame:
    """
    Convert text file to Excel format

    Args:
        txt_fpath (str): 테이블 구조 텍스트 파일 경로
        excel_fpath (str): Excel 파일 저장 경ㅗ
    """
    # Initialize lists to store the data
    table_name = ""
    data = []

    # Read the text file
    with open(txt_fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Process each line
    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Check if line contains table name
        if line.startswith("Table:"):
            table_name = line.split(":")[1].strip()
            continue

        # Skip the header line with column descriptions
        if "Field" in line and "Type" in line and "Null" in line:
            continue

        # Process data lines
        # Match lines that start with a number followed by space
        if re.match(r"^\d+\s", line):
            # Split the line and clean up the values
            parts = [x.strip() for x in line.split()]

            # Extract required information
            col_name = parts[1]
            col_type = parts[2]
            is_pk = "YES" if "PRI" in line else "NO"

            # Add to data list
            data.append(
                {
                    "table_name": table_name,
                    "col_name": col_name,
                    "col_type": col_type,
                    "is_pk": is_pk,
                }
            )

    # Create DataFrame
    df = pd.DataFrame(data)

    # Save to Excel
    df.to_excel(excel_fpath, index=False)
    print(f"Table structure data saved to: {excel_fpath}")

    return df


if __name__ == "__main__":
    txt_fpath = "txt_to_excel/table.txt"
    excel_fpath = "txt_to_excel/table.xlsx"
    df = convert_txt_to_excel(txt_fpath, excel_fpath)
    print(tabulate(df))
