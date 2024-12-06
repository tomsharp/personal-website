import os 
import json 

from flask import Flask, render_template, request, abort, redirect, url_for, flash
import markdown

import config
import utils 


app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.context_processor
def inject_global_config():
    """Inject global configuration into all templates."""
    return dict(
        site_title=config.WEBSITE_NAME,
        footer_config=config.FOOTER_CONFIG
    )

@app.route("/")
def home():
    return render_template("index.html", title=config.WEBSITE_NAME)

@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact", socials=config.SOCIALS)

@app.route("/newsletter", methods=["GET", "POST"])
def newsletter():
    if request.method == "POST":
        email = request.form.get("email")
        if email:
            utils.save_subscriber(email, config.SUBSCRIBERS_FILE)
            flash("Thank you for subscribing!", "success")
        else:
            flash("Please enter a valid email address.", "error")
        return redirect(url_for("newsletter"))
    
    posts = utils.load_posts(config.NEWSLETTER_FOLDER, config.POSTS_CSV_FILE) 
    return render_template("newsletter.html", title="Newsletter", posts=posts)

@app.route("/newsletter/<slug>")
def view_post(slug):
    posts = utils.load_posts(config.NEWSLETTER_FOLDER, config.POSTS_CSV_FILE)
    post_metadata = next((post for post in posts if post['slug'] == slug), None)
    
    if post_metadata:
        post_path = os.path.join(config.NEWSLETTER_FOLDER, post_metadata['filename'])
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
    with open(config.PROJECTS_JSON, 'r') as file:
        projects = json.load(file)
    return render_template("projects.html", title="Projects", projects=projects)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", title="404 - Page Not Found"), 404

if __name__ == "__main__":
    app.run(debug=True)
