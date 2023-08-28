from datetime import datetime

import pandas
from pandas import DataFrame

from dd.api.main import get_courses
from dd.api.model import Course


def _build_assignments(courses: list[Course]) -> DataFrame:
    assignment_ids: list[int, ...] = []  # For taking out duplicates
    assignments: list[str, ...] = []
    due_dates: list[datetime] = []
    classes: list[str] = []
    for course in courses:
        for assignment_group in course.assignment_groups:
            if "test" in assignment_group.name.lower() or "exam" in assignment_group.name.lower():
                continue
            for assignment in assignment_group.assignments:
                if assignment.id not in assignment_ids:
                    assignments.append(assignment.name)
                    due_dates.append(assignment.due_date)
                    classes.append(course.name)

                    assignment_ids.append(assignment.id)

    data = {
        "Done?": ["" for i in range(len(assignments))],  # TODO: Add checkboxes somehow...
        "Assignment": assignments,
        "Due Date": due_dates,
        "Class": classes
    }
    df = DataFrame(data)
    df['Due Date'] = pandas.to_datetime(df['Due Date'])
    df = df.sort_values(by="Due Date")

    return df


def _build_exams():
    pass


def build() -> DataFrame:
    assignments = _build_assignments(get_courses())
    print(assignments.to_markdown())


if __name__ == "__main__":
    build()
