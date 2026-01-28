import praw
import pandas as pd
from praw.models import MoreComments

# ----------------------------
# Reddit API Credentials
# ----------------------------
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="YOUR_USER_AGENT"
)

# ----------------------------
# Subreddit Information
# ----------------------------
subreddit = reddit.subreddit("Python")

print("Subreddit Name:", subreddit.display_name)
print("Title:", subreddit.title)
print("Description:", subreddit.description)

# ----------------------------
# Fetch Top Posts of the Month
# ----------------------------
posts = subreddit.top(time_filter="month", limit=10)

posts_data = {
    "Title": [],
    "Post Text": [],
    "ID": [],
    "Score": [],
    "Total Comments": [],
    "Post URL": []
}

for post in posts:
    posts_data["Title"].append(post.title)
    posts_data["Post Text"].append(post.selftext)
    posts_data["ID"].append(post.id)
    posts_data["Score"].append(post.score)
    posts_data["Total Comments"].append(post.num_comments)
    posts_data["Post URL"].append(post.url)

df_posts = pd.DataFrame(posts_data)
print("\nTop Posts:\n", df_posts.head())

# ----------------------------
# Scrape Comments from a Post
# ----------------------------
url = "https://www.reddit.com/r/IAmA/comments/m8n4vt/im_bill_gates_cochair_of_the_bill_and_melinda/"

submission = reddit.submission(url=url)
submission.comments.replace_more(limit=0)

comments = []

for comment in submission.comments:
    if isinstance(comment, MoreComments):
        continue
    comments.append(comment.body)

comments_df = pd.DataFrame(comments, columns=["Comment"])
print("\nTop Comments:\n", comments_df.head())