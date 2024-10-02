import pandas as pd
import openpyxl
from . import textTranslate


def translate_excel(input_file, source_lang, target_lang):
    # Read the Excel file into a DataFrame
    output_file = "translated_xlsx.xlsx"
    workbook = openpyxl.load_workbook(input_file)
    sheet = workbook.active

# Iterate through each cell in the worksheet
    for row in sheet.iter_rows():
        for cell in row:
            if cell.data_type == 's' and cell.value.strip():  # Check if it's a string and not empty
                # Skip if the cell has a formula
                if cell.data_type == 'f':
                    continue

                # Translate the text
                translated_text = textTranslate.translate_text(cell.value, source_lang, target_lang)

                # Overwrite the original text with the translated text
                cell.value = translated_text

    # Save the updated workbook
    workbook.save(output_file)