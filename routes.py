from flask import Blueprint, request, jsonify
from models import db, Task, Comment

bp = Blueprint("comments", __name__)

# ---------- TASK ROUTES ----------

@bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Task title is required"}), 400
    task = Task(title=data["title"])
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title}), 201

@bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json()
    task.title = data.get("title", task.title)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title}), 200

@bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    # 🧹 Reorder comments for all remaining tasks
    remaining_tasks = db.session.query(Task).all()
    for t in remaining_tasks:
        comments = Comment.query.filter_by(task_id=t.id).order_by(Comment.comment_number).all()
        for i, c in enumerate(comments, start=1):
            c.comment_number = i
    db.session.commit()

    return jsonify({"message": "Task and its comments deleted, all comment numbers reindexed"}), 200

@bp.route("/tasks", methods=["GET"])
def get_all_tasks():
    tasks = db.session.query(Task).all()
    result = [{"id": t.id, "title": t.title} for t in tasks]
    return jsonify(result), 200

# ---------- COMMENT ROUTES ----------

@bp.route("/tasks/<int:task_id>/comments", methods=["POST"])
def create_comment(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Comment text is required"}), 400

    existing_count = Comment.query.filter_by(task_id=task_id).count()
    comment_number = existing_count + 1

    comment = Comment(
        text=data["text"],
        task_id=task_id,
        comment_number=comment_number
    )
    db.session.add(comment)
    db.session.commit()

    return jsonify({
        "id": comment.id,
        "text": comment.text,
        "task_id": comment.task_id,
        "comment_number": comment.comment_number
    }), 201

@bp.route("/tasks/<int:task_id>/comments", methods=["GET"])
def get_comments(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    comments = Comment.query.filter_by(task_id=task_id).order_by(Comment.comment_number).all()
    result = [{
        "id": c.id,
        "comment_number": c.comment_number,
        "text": c.text,
        "task_id": c.task_id,
        "created_at": c.created_at.isoformat()
    } for c in comments]
    return jsonify(result), 200

@bp.route("/tasks/<int:task_id>/comments/<int:comment_number>", methods=["PUT"])
def update_comment(task_id, comment_number):
    comment = Comment.query.filter_by(task_id=task_id, comment_number=comment_number).first()
    if not comment:
        return jsonify({"error": "Comment not found for this task"}), 404

    data = request.get_json()
    comment.text = data.get("text", comment.text)
    db.session.commit()
    return jsonify({
        "id": comment.id,
        "comment_number": comment.comment_number,
        "text": comment.text
    }), 200

@bp.route("/tasks/<int:task_id>/comments/<int:comment_number>", methods=["DELETE"])
def delete_comment(task_id, comment_number):
    comment = Comment.query.filter_by(task_id=task_id, comment_number=comment_number).first()
    if not comment:
        return jsonify({"error": "Comment not found for this task"}), 404

    db.session.delete(comment)
    db.session.commit()

    # 🔁 Reorder remaining comments
    remaining_comments = Comment.query.filter_by(task_id=task_id).order_by(Comment.comment_number).all()
    for i, c in enumerate(remaining_comments, start=1):
        c.comment_number = i
    db.session.commit()

    return jsonify({"message": "Comment deleted and renumbered"}), 200
