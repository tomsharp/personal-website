import os 

from flask import Flask, render_template, request
import markdown

app = Flask(__name__)

NEWSLETTER_FOLDER = "newsletter"

@app.route("/")
def home():
    return render_template("index.html", title="Home")

@app.route("/blog")
def blog():
    return render_template("blog.html", title="Blog")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        print(f"Message from {name} ({email}): {message}")
        return "Thank you for your message!"
    return render_template("contact.html", title="Contact")

# @app.route("/newsletter")
# def newsletter():
#     return render_template("newsletter.html", title="Newsletter")
@app.route("/newsletter")
def newsletter():
    post_files = [
        file for file in os.listdir(NEWSLETTER_FOLDER) if file.endswith('.md')
    ]
    return render_template("newsletter.html", title="Newsletter", post_files=post_files)


@app.route("/newsletter/<filename>")
def view_post(filename):
    # Load the content of the selected Markdown file
    post_path = os.path.join(NEWSLETTER_FOLDER, filename)
    if os.path.exists(post_path) and filename.endswith('.md'):
        with open(post_path, 'r') as file:
            markdown_content = file.read()
        # Convert Markdown to HTML
        html_content = markdown.markdown(markdown_content)
        return render_template("post.html", title=filename, content=html_content)
    else:
        abort(404)  # Return a 404 error if the file doesn't exist

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", title="404 - Page Not Found"), 404

if __name__ == "__main__":
    app.run(debug=True)
