import re
import os 
import csv
from datetime import datetime
import json 

from flask import Flask, render_template, request, abort, redirect, url_for, flash
import markdown

from config import SOCIALS, PROJECTS_JSON, NEWSLETTER_FOLDER, CSV_FILE, SUBSCRIBERS_FILE


app = Flask(__name__)
app.secret_key = 'your_secret_key'

def extract_first_image(markdown_content):
    """Extract the first image URL from the Markdown content."""
    image_pattern = r"!\[.*?\]\((.*?)\)"
    match = re.search(image_pattern, markdown_content)
    return match.group(1) if match else None


def load_posts():
    posts = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Parse datetime fields
                row['created_datetime'] = datetime.strptime(row['created_datetime'], '%Y-%m-%d %H:%M:%S')
                row['last_modified_datetime'] = datetime.strptime(row['last_modified_datetime'], '%Y-%m-%d %H:%M:%S')
                
                # Read the post content and extract the first image
                post_path = os.path.join(NEWSLETTER_FOLDER, row['filename'])
                if os.path.exists(post_path):
                    with open(post_path, 'r') as file:
                        markdown_content = file.read()
                        row['image'] = extract_first_image(markdown_content)
                else:
                    row['image'] = None
                
                posts.append(row)
    return posts

def save_subscriber(email):
    with open(SUBSCRIBERS_FILE, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([email, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])


@app.route("/")
def home():
    return render_template("index.html", title="Home")

@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact", socials=SOCIALS)

@app.route("/newsletter", methods=["GET", "POST"])
def newsletter():
    if request.method == "POST":
        email = request.form.get("email")
        if email:
            save_subscriber(email)
            flash("Thank you for subscribing!", "success")
        else:
            flash("Please enter a valid email address.", "error")
        return redirect(url_for("newsletter"))
    
    posts = load_posts()  # Ensure your load_posts function is defined elsewhere
    return render_template("newsletter.html", title="Newsletter", posts=posts)

@app.route("/newsletter/<slug>")
def view_post(slug):
    posts = load_posts()
    post_metadata = next((post for post in posts if post['slug'] == slug), None)
    
    if post_metadata:
        post_path = os.path.join(NEWSLETTER_FOLDER, post_metadata['filename'])
        if os.path.exists(post_path):
            # Load post content
            with open(post_path, 'r') as file:
                markdown_content = file.read()
            html_content = markdown.markdown(markdown_content)

            return render_template(
                "post.html", 
                title=post_metadata['title'],
                content=html_content,
                created=post_metadata['created_datetime'].date(),
                modified=post_metadata['last_modified_datetime'].date(),
                author=post_metadata['author']
            )
    abort(404)


@app.route("/projects")
def projects():
    # Load project data from the JSON file
    with open(PROJECTS_JSON, 'r') as file:
        projects = json.load(file)
    return render_template("projects.html", title="Projects", projects=projects)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", title="404 - Page Not Found"), 404

if __name__ == "__main__":
    app.run(debug=True)
