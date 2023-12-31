from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Assignment:
    name: str
    id: int
    due_date: datetime

    def __str__(self):
        return f"Assignment {self.name}({self.id}) due at {self.due_date}"


@dataclass(frozen=True, slots=True)
class AssignmentGroup:
    name: str
    id: int
    assignments: list[Assignment]

    def __str__(self):
        return f"Assignment Group | {self.name}({self.id})"


@dataclass(frozen=True, slots=True)
class Course:
    code: str
    name: str
    id: int
    assignment_groups: list[AssignmentGroup]

    def __str__(self):
        out = ""

        out += self.code + " | " + self.name + " | " + str(self.id) + "\n"
        for assignment_group in self.assignment_groups:
            out += "\t" + str(assignment_group) + "\n"
            for assignment in assignment_group.assignments:
                out += "\t\t" + str(assignment) + "\n"

        return out
