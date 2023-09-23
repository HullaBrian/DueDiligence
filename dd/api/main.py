import json
import re

import canvasapi.course
import requests
from canvasapi import Canvas
from loguru import logger

from dd.api.model import Course
from dd.api.model import AssignmentGroup
from dd.api.model import Assignment
from dd.environment import get_token

API_URL = "https://utsa.instructure.com"
API_KEY = get_token()


def get_courses(user_id: int = 0, token: str = "") -> list[Course]:
    """
    Entrypoint for api interactions
    :param token:
    :param user_id:
    :return:
    """
    if user_id == 0:
        user_id = get_user_id(token)
    if user_id == -1:
        return []
    assert user_id > 0, "Invalid user id passed. Use dd.api.main.get_user_id() to retrieve user id"

    viable_courses: list[Course] = []

    canvas = Canvas(API_URL, token)
    user = canvas.get_user(user_id)
    courses = user.get_courses()

    for course in courses:
        course_rep: str = ""

        try:
            course_rep += str(course)
        except AttributeError as e:
            logger.error(f"A course does not have 1 or more attributes: course_code, name, or id. Exception: {e}")
            continue

        if not course_rep:
            continue
        logger.success(f"Found course: {course_rep}")

        course.name = re.sub(r"((\w{1,}[-]){3})\w{1,} \d{4}-", "", course.name, 0)  # Normalize course name

        assignment_groups: list[AssignmentGroup] = []
        try:
            assignment_groups = _build_assignment_groups(course)
        except Exception as e:
            logger.error(f"Could not build assignment groups for course '{course.name}': {e}")
            continue

        viable_courses.append(
            Course(
                course.course_code,
                course.name,
                course.id,
                assignment_groups
            )
        )

    return viable_courses


def _build_assignment_groups(course: canvasapi.course.Course) -> list[AssignmentGroup]:
    assignment_groups = course.get_assignment_groups()

    built_assignment_groups: list[AssignmentGroup] = []
    for a_group in assignment_groups:
        built_assignment_groups.append(AssignmentGroup(a_group.name, a_group.id, _build_assignments(course)))

    return built_assignment_groups


def _build_assignments(course: canvasapi.course.Course) -> list[Assignment]:
    assignments: list[Assignment] = []
    for assignment in course.get_assignments():
        try:
            try:
                _ = assignment.due_at_date
            except AttributeError:
                _ = None
            assignments.append(Assignment(assignment.name, assignment.id, _))
        except AttributeError as e:
            logger.info(f"Assignment '{assignment}' for course '{course.name}' doesn't have a required attribute! {e}")
    return assignments


def get_user_id(token: str = "") -> int:
    """
    function to retrieve the user id needed to get

    :return: canvas user id for specified student
    """
    url = f"{API_URL}/api/v1/courses"

    payload = {}
    headers = {
        'Authorization': f'Bearer {get_token() if token == "" else token}',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = json.loads(response.text)

    try:
        return int(response_json[0]["enrollments"][0]["user_id"])
    except KeyError:
        logger.error("Could not retrieve user id!")
        return -1
