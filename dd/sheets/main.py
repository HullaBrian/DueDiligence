import pandas as pd
from loguru import logger


def export(assignments: pd.DataFrame, exams: pd.DataFrame) -> bool:
    file_name = 'School.xlsx'

    assignments.to_excel(file_name, index=False)

    logger.success("Exported data to spreadsheet!")
    return True
