from flask import Blueprint, send_file, jsonify
from celery_tasks.tasks import export_category, export_professional
from flask_security import auth_required, roles_required
from celery.result import AsyncResult


celery_tasks_bp = Blueprint('celery_tasks_bp', __name__)



@celery_tasks_bp.route('/create_prof',methods=['GET'])
@auth_required('token')
@roles_required('admin')
def create_prof():
    task = export_professional.delay()
    return jsonify({"prof_task_id": task.id, "status": "Processing"}), 200




@celery_tasks_bp.route('/send_prof/<task_id>')
@auth_required('token')
@roles_required('admin')
def prof_status(task_id):

    task_result = export_professional.AsyncResult(task_id)

    if task_result.successful():
        file_name = task_result.result  # The returned CSV filename
        file_path = f'celery_tasks/downloads/{file_name}'

        # Ensure the file exists before sending
        try:
            return send_file(file_path, as_attachment=True)
        except FileNotFoundError:
            return jsonify({"error": "File not found. The task may have failed or file was deleted."}), 404

    elif task_result.failed():
        return jsonify({"task_id": task_id, "status": "Failed", "error": str(task_result.info)}), 500

    else:
        return jsonify({"task_id": task_id, "status": task_result.status}), 202



@celery_tasks_bp.route('/cat')   
def get_csv():
    cat = export_category.delay()
    return {"cat_task_id":cat.id}

@celery_tasks_bp.route('/cat_status/<task_id>')
def cat_status(task_id):
    cat = export_category.AsyncResult(task_id)
    if cat.ready():
        return send_file(f'celery_tasks/downloads/{cat.get()}', as_attachment=False)
    else:
        return {"Task status": cat.status}
