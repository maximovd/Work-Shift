from app import create_app, db
from app.models import Employees, Department, User, WorkShift, ServerStatus

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Department': Department,
        'Employees': Employees,
        'WorkShift': WorkShift,
        'ServerStatus': ServerStatus,
    }