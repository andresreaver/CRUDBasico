import sqlite3

from flask import Blueprint, request, jsonify
from ..database import get_db_connection

users_bp = Blueprint('users', __name__)


# Ruta para leer todos los usuarios (READ)
@users_bp.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return jsonify([{"id": row["id"], "name": row["name"], "email": row["email"]} for row in users]), 200


# Ruta para leer un usuario especifico por Id(READ)
@users_bp.route('/users/int:<user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", [user_id]).fetchone()
    conn.close()
    if user:
        return jsonify({"id": user["id"], "name": user["name"], "email": user["email"]}), 200
    return jsonify({"error": 'user not found'}), 404


# Ruta para crear un nuevo usuario (CREATE)
@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": 'name and/or email required'}), 400

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', [data["name"], data["email"]])
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": 'Email already exists'}), 400
    finally:
        conn.close()

    return jsonify({"message": "User created succesfully"}), 201


# Ruta para actualizar un usuario (UPDATE)
@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", [user_id]).fetchone()

    if not user:
        conn.close()
        return jsonify({"error": 'user not found'}), 404

    conn.execute(
        'UPDATE users SET name = ?, email = ? WHERE id = ?',
        (data.get("name", user["name"]), data.get("email", user["email"]), user_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "User updated succesfully"}), 200


# Ruta para eliminar un usuario (DELETE)
@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id)).fetchone()

    if not user:
        conn.close()
        return jsonify({"error": 'user not found'}), 404

    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "User deleted succesfully"}), 200
