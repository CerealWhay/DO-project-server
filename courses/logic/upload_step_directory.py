

def course_step_file_path(obj, filename):
    return f'teachers/{obj.course.teacher}/{obj.course}/{filename}'


def student_answer_file_path(obj, filename):
    return f'students/{obj.student}/{obj.step.course}/{filename}'
