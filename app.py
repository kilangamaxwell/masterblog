"""
A simple Flask application for managing blog posts.

Routes:
- `/`: Displays the list of blog posts.
- `/add`: Allows adding a new blog post.
- `/delete/<int:post_id>`: Deletes a specific blog post.
- `/update/<int:post_id>`: Allows updating a specific blog post.

"""

from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

file_path = 'blog_posts.json'


def fetch_post_by_id(id):
    """
    Fetches a blog post from the JSON file based on the given post ID.

    Args:
        id (int): The ID of the blog post.

    Returns:
        dict: The blog post dictionary if found, otherwise returns "Not Found".

    """
    with open(file_path, 'r') as json_file:
        posts = json.load(json_file)
    for post in posts:
        if post['id'] == id:
            return post
    return "Not Found"


def fetch_posts():
    """
    Fetches all blog posts from the JSON file.

    Returns:
        list: A list of blog post dictionaries.

    """
    with open(file_path, 'r') as json_file:
        posts = json.load(json_file)
    return posts


@app.route('/')
def index():
    """
    Displays the list of blog posts on the home page.

    Returns:
        str: The rendered HTML template.

    """
    posts = fetch_posts()
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handles adding a new blog post.

    Returns:
        str: The rendered HTML template or a redirect response.

    """
    posts = fetch_posts()
    if request.method == 'POST':
        # Get the form data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Assign unique id
        new_id = len(posts) + 1
        for existing_post in posts:
            if new_id in existing_post.values():
                new_id += 1

        # Create a new blog post dictionary
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        # Append the new post to the blog list
        posts.append(new_post)

        # Save the updated blog list to the JSON file
        with open(file_path, 'w') as json_file:
            json.dump(posts, json_file)

        # Redirect to the home page
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
    Handles deleting a specific blog post.

    Args:
        post_id (int): The ID of the blog post to be deleted.

    Returns:
        str: A redirect response or an error message if the post is not found.

    """
    posts = fetch_posts()
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            with open(file_path, 'w') as json_file:
                json.dump(posts, json_file)
            return redirect(url_for('index'))
    return 'Post not found'


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Handles updating a specific blog post.

    Args:
        post_id (int): The ID of the blog post to be updated.

    Returns:
        str: The rendered HTML template or a redirect response.

    """
    post = fetch_post_by_id(post_id)
    posts = fetch_posts()
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        for index, blog in enumerate(posts):
            if post['id'] == blog['id']:
                posts[index]['author'] = author
                posts[index]['title'] = title
                posts[index]['content'] = content
        # Save the updated blog list to the JSON file
        with open(file_path, 'w') as json_file:
            json.dump(posts, json_file)

        # Redirect to the home page
        return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run()
