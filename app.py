from flask import Flask, request, jsonify
from datetime import datetime
from model import *
# Initialize Flask app
app = Flask(__name__)

# API endpoints

@app.route('/add_friend', methods=['POST'])
def add_friend():
    data = request.json
    username1 = data.get('username1')
    username2 = data.get('username2')
    try:
        user1 = User.get(User.username == username1)
        user2 = User.get(User.username == username2)
        Friendship.create(user1=user1, user2=user2)
        return jsonify({'message': 'Friend added successfully'})
    except User.DoesNotExist:
        return jsonify({'error': 'User not found'}), 404

@app.route('/remove_friend', methods=['POST'])
def remove_friend():
    data = request.json
    username1 = data.get('username1')
    username2 = data.get('username2')
    try:
        user1 = User.get(User.username == username1)
        user2 = User.get(User.username == username2)
        friendship = Friendship.get((Friendship.user1 == user1) & (Friendship.user2 == user2))
        friendship.delete_instance()
        return jsonify({'message': 'Friend removed successfully'})
    except (User.DoesNotExist, Friendship.DoesNotExist):
        return jsonify({'error': 'User or friendship not found'}), 404

@app.route('/send_post', methods=['POST'])
def send_post():
    data = request.json
    username = data.get('username')
    content = data.get('content')
    try:
        user = User.get(User.username == username)
        Post.create(user=user, content=content)
        return jsonify({'message': 'Post sent successfully'})
    except User.DoesNotExist:
        return jsonify({'error': 'User not found'}), 404

@app.route('/remove_post/<int:post_id>', methods=['DELETE'])
def remove_post(post_id):
    try:
        post = Post.get(Post.id == post_id)
        post.delete_instance()
        return jsonify({'message': 'Post removed successfully'})
    except Post.DoesNotExist:
        return jsonify({'error': 'Post not found'}), 404

@app.route('/like_post', methods=['POST'])
def like_post():
    data = request.json
    username = data.get('username')
    post_id = data.get('post_id')
    try:
        user = User.get(User.username == username)
        post = Post.get(Post.id == post_id)
        Like.create(user=user, post=post)
        return jsonify({'message': 'Post liked successfully'})
    except (User.DoesNotExist, Post.DoesNotExist):
        return jsonify({'error': 'User or post not found'}), 404

@app.route('/remove_like', methods=['POST'])
def remove_like():
    data = request.json
    username = data.get('username')
    post_id = data.get('post_id')
    try:
        user = User.get(User.username == username)
        post = Post.get(Post.id == post_id)
        like = Like.get((Like.user == user) & (Like.post == post))
        like.delete_instance()
        return jsonify({'message': 'Like removed successfully'})
    except (User.DoesNotExist, Post.DoesNotExist, Like.DoesNotExist):
        return jsonify({'error': 'User, post, or like not found'}), 404

@app.route('/fetch_posts', methods=['GET'])
def fetch_posts():
    posts = []
    for post in Post.select():
        post_data = {
            'id': post.id,
            'content': post.content,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'likes_count': post.likes.count(),
            'comments': [{'username': comment.user.username, 'content': comment.content, 'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')} for comment in post.comments]
        }
        posts.append(post_data)
    return jsonify(posts)

if __name__ == '__main__':
    app.run(debug=True)
