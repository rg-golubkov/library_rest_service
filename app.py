import os

from rest_service import create_app

app = create_app()


if __name__ == '__main__':
    app.run(
        host=os.environ.get('FLASK_HOST', default='127.0.0.1'),
        port=os.environ.get('FLASK_PORT', default=5000),
    )
