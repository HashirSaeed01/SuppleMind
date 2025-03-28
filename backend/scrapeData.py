import praw

# Reddit API Credentials
reddit = praw.Reddit(
    client_id="ZF3EeaEc85XwGxBPfAGsCQ",
    client_secret="_joJVc5Yys3iQqBzb9Jx8PyDDgVzNQ",
    user_agent="SupplementApp/1.0"
)

def fetch_supplement_posts(limit=10):
    """
    Fetches recent posts from r/supplements.
    
    Args:
        limit (int): Number of posts to fetch.
        
    Returns:
        list: A list of dictionaries with post details.
    """
    posts = []
    subreddit = reddit.subreddit("supplements")

    for post in subreddit.hot(limit=limit):  # 'hot' can be changed to 'new', 'top', etc.
        posts.append({
            "title": post.title,
            "body": post.selftext,
            "url": post.url,
            "upvotes": post.score,
            "comments": [comment.body for comment in post.comments if hasattr(comment, "body")]
        })

    return posts

# Example Usage
if __name__ == "__main__":
    data = fetch_supplement_posts(limit=5)
    
    for idx, post in enumerate(data):
        print(f"🔹 Post {idx+1}: {post['title']}")
        print(f"👍 Upvotes: {post['upvotes']}")
        print(f"🔗 URL: {post['url']}")
        print(f"💬 Comments: {post['comments'][:3]}")  # Show first 3 comments
        print("-" * 50)
