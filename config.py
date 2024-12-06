# general
WEBSITE_NAME = "Your Name"
YEAR = 2024

# paths
PROJECTS_FOLDER = "projects"
PROJECTS_JSON = f"{PROJECTS_FOLDER}/projects.json"
NEWSLETTER_FOLDER = "newsletter"
POSTS_CSV_FILE = f"{NEWSLETTER_FOLDER}/posts.csv"
SUBSCRIBERS_FILE = f"{NEWSLETTER_FOLDER}/subscribers.csv"

# socials
SOCIALS = {
    "twitter": "yourusername",
    "github": "yourgithubusername",
    "medium": "yourmediumusername",
    "email": "youremail@example.com",
    "linkedin": "yourlinkedinusername"
}

# foooter
FOOTER_CONFIG = {
    "name":WEBSITE_NAME,
    "year": YEAR,
    "social_links": {
        "GitHub": f"https://github.com/{SOCIALS['github']}",
        "Twitter": f"https://twitter.com/{SOCIALS['twitter']}",
        "LinkedIn": f"https://linkedin.com/in/{SOCIALS['linkedin']}"
    }
}
