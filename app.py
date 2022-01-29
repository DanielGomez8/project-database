"""
This module contains example code for Flask usage.
Feel free to modify this file in any way.
"""
import json

from auth import auth_token
from db import *
from flask import Flask, Response, request
import uuid
from helper import parse_comments

app = Flask(__name__)
initialize_db()

@app.route("/projects", methods=['POST'])
def create_project():
    # Auth and get user info
    username, user_id = auth_token(request.headers.get("authorization"))
    if not username or not user_id:
        return Response({"message": "Invalid or missing token"}, 401)

    # Verify request body
    project_name = request.json.get("project_name", None)
    if not project_name:
        return Response(json.dumps({"message": "Message must be provided"}), 400, mimetype="application/json")

    # Generate project ID
    project_id = str(uuid.uuid4())

    # Create a new project data
    project = (project_id, user_id, username, project_name)
    insert_project(project)

    # Build response
    response_dict = {
        "project_id": project_id,
        "owner_id": user_id,
        "owner_username": username,
        "project_name": project_name
    }
    return Response(json.dumps(response_dict), status=201, mimetype="application/json")

@app.route("/projects/<project_id>", methods=['GET','DELETE'])
def project(project_id):
    # Auth and get user info
    username, user_id = auth_token(request.headers.get("authorization"))
    if not username or not user_id:
        return Response({"message": "Invalid or missing token"}, 401)

    if not project_id:
        return Response(json.dumps({"message": "Project id must be provided"}), 400, mimetype="application/json")

    if request.method == 'DELETE':
        # Check if project exists in DB
        result = get_project(project_id)
        if not result:
            return Response(json.dumps({"message": "Project not found"}), 404, mimetype="application/json")

        # Check if user owns project
        if user_id != result[1]:
            return Response(json.dumps({"message": "Only project owner can delete project"}), 403, mimetype="application/json")

        # Delete project
        delete_project(project_id)
        return Response(json.dumps({"message":"Project deleted"}), 200, mimetype="application/json")

    if request.method == 'GET':
        # Check if project exists
        result = get_project(project_id)
        if not result:
            return Response(json.dumps({"message": "Project not found"}), 404, mimetype="application/json")

        # Build response
        response_dict = {
            "project_id": result[0],
            "owner_id": result[1],
            "owner_username": result[2],
            "project_name": result[3],
            "comments": parse_comments(get_all_comments(project_id))
        }
        return Response(json.dumps(response_dict), status=200, mimetype="application/json")



@app.route("/projects/<project_id>/comments", methods=['POST'])
def project_comments(project_id):
    # Auth and get user info
    username, user_id = auth_token(request.headers.get("authorization"))
    if not username or not user_id:
        return Response({"message": "Invalid or missing token"}, 401)

    # Verify request body
    comment = request.json.get("message", None)
    if not comment:
        return Response(json.dumps({"message": "Message must be provided"}), 400, mimetype="application/json")

    # Generate comment ID
    comment_id = str(uuid.uuid4())

    # Create a new comment data
    comment_data = (comment_id, project_id, user_id, username, comment)
    insert_comment(comment_data)

    # Build response
    response_dict = {
        "comment_id": comment_id,
        "commenter_id": user_id,
        "commenter_username": username,
        "comment": comment
    }
    return Response(json.dumps(response_dict), status=201, mimetype="application/json")


if __name__ == "__main__":
    app.run()
