import pandas as pd
from loguru import logger


def export(assignments: pd.DataFrame, exams: pd.DataFrame, file_name: str = "ERROR.xlsx") -> str:
    if assignments.empty and exams.empty:
        logger.error("Could not export data - no assignments or exams were passed!")
        return ""

    if not file_name.endswith(".xlsx"):
        file_name += ".xlsx"

    file_name.replace(".xls", ".xlsx")

    assignments.to_excel(file_name, index=False)

    logger.success("Exported data to spreadsheet!")
    return file_name
