from datetime import datetime

import pandas
from loguru import logger
from pandas import DataFrame

from dd.api.main import get_courses
from dd.api.model import Course, Assignment


def _build_assignments(courses: list[Course]) -> tuple[DataFrame, DataFrame]:
    exams: list[str] = []

    assignment_ids: list[int, ...] = []  # For taking out duplicates
    assignments: list[str, ...] = []
    due_dates: list[datetime] = []
    classes: list[str] = []
    for course in courses:
        for assignment_group in course.assignment_groups:
            if "test" in assignment_group.name.lower() or "exam" in assignment_group.name.lower():
                for test in assignment_group.assignments:
                    if True not in [val in test.name.lower() for val in ["assignment",
                                                                         "practice",
                                                                         "quiz",
                                                                         "textbook reading"
                                                                         ]]:
                        exams.append(
                            assignment_group.name + " | " +
                            course.name + " | " +
                            test.name + " | " +
                            str(test.due_date)
                        )
                    elif test.id not in assignment_ids:
                        assignments.append(test.name)
                        due_dates.append(test.due_date)
                        classes.append(course.name)

                        assignment_ids.append(test.id)
                        logger.critical(f"Set formally labled exam '{test.name}' to assignment")

            for assignment in assignment_group.assignments:
                if assignment.id not in assignment_ids:
                    assignments.append(assignment.name)
                    due_dates.append(assignment.due_date)
                    classes.append(course.name)

                    assignment_ids.append(assignment.id)

    data = {
        "!! EXAMS !!": exams
    }
    exams_df: DataFrame = DataFrame(data)

    data = {
        "Done?": ["" for i in range(len(assignments))],  # TODO: Add checkboxes somehow...
        "Assignment": assignments,
        "Due Date": due_dates,
        "Class": classes
    }
    assignments_df: DataFrame = DataFrame(data)
    assignments_df['Due Date'] = pandas.to_datetime(assignments_df['Due Date'])
    assignments_df = assignments_df.sort_values(by="Due Date")

    return assignments_df, exams_df


def _build_exams():
    pass


def build() -> None:
    assignments, exams = _build_assignments(get_courses())
    print(assignments.to_markdown())
    print("*" * 20)
    print(exams.to_markdown())


if __name__ == "__main__":
    build()
