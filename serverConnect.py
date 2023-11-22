from flask import Flask, jsonify
import os
import logging

class ServerManage:
    def __init__(self, app: Flask):
        self.app = app

    def setup(self):
        # 환경 변수와 로깅 설정
        self._configure_environment()
        self._configure_logging()

        # 데이터베이스 설정
        self._configure_database()

        # 에러 핸들링
        self._configure_error_handlers()

    def _configure_environment(self):
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')

    def _configure_logging(self):
        logging.basicConfig(level=logging.INFO)

    def _configure_database(self):
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'database.db')
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def _configure_error_handlers(self):
        @self.app.errorhandler(400)
        def bad_request(e):
            return jsonify({"error": "Bad request"}), 400

        @self.app.errorhandler(401)
        def unauthorized(e):
            return jsonify({"error": "Unauthorized"}), 401

        @self.app.errorhandler(403)
        def forbidden(e):
            return jsonify({"error": "Forbidden"}), 403

        @self.app.errorhandler(404)
        def page_not_found(e):
            return jsonify({"error": "Page not found"}), 404

        @self.app.errorhandler(405)
        def method_not_allowed(e):
            return jsonify({"error": "Method not allowed"}), 405

        @self.app.errorhandler(500)
        def internal_server_error(e):
            return jsonify({"error": "Internal server error"}), 500
