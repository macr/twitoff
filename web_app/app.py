from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy, request
from flask_migrate import Migrate
import datetime
import os
from sqlalchemy.sql import func
from .models import db, Tweet, User
from flask import jsonify
from .tweets import add_or_update_user
from .predict import predict_user
def create_app():
    """
    App factory function
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/api/users', methods=['GET', 'POST'])
    def list_users():
        if request.method == 'POST':
            username = request.json
            add_or_update_user(username)
        users = User.query.all()
        users = [{'username': u.username, 'id': str(u.id)}
                 for u in users]
        return jsonify(users)

    @app.route('/api/user/<user_id>', methods=['GET', 'POST'])
    def user_tweets(user_id):
        user = User.query.filter_by(id=user_id).first()
        tweets = [t.text for t in user.tweets]
        userObject = {'username': user.username, 'tweets': tweets}
        return jsonify(userObject)

    @app.route('/api/predict/<user1>/<user2>')
    def predict(user1, user2):
        tweet = request.args.get('tweet')
        winner = predict_user(user1, user2, tweet)
        return jsonify(winner.username)

    return app