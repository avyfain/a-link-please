import os
import random
from atproto import Client, models
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  

TARGET_HANDLE = 'a-link-please.bsky.social'
SEARCH_QUERY = '"a link please"'

client = Client()
client.login(TARGET_HANDLE, os.getenv('BSKY_PASS'))

def get_last_post_time(handle: str) -> datetime:
    feed = client.app.bsky.feed.get_author_feed({'actor': handle, 'limit': 1})
    if feed.feed:
        return feed.feed[0].post.indexed_at

def search_posts_after(since: datetime, query: str):
    results = client.app.bsky.feed.search_posts({'q': query, 'limit': 10, 'since': since})
    return results.posts

def reply_with_photo(post: models.AppBskyFeedDefs.PostView):
    phrases = [
        'Here you go',
        'A Link coming right up',
        'Done',
        "I know what you're thinking. Zelda was the princess though",
        "I'm not sure if you're asking for a link or a picture of Link, but here you go",
        "Behold: Link, Hero of Time. Not what you meant? Too bad",
        "Sure, here's Link. Hyrule thanks you for your service",
        "You asked for a link. You got a Link",
        "Link summoned. Ganon fears you now",
        "Zelda's boyfriend reporting for duty",
        "You rang? Here's our boy in green",
        "It's dangerous to go alone—take this Link",
        ]

    img = 'img/{}.png'.format(random.choice(range(10)))
    message = '{}, @{}!'.format(random.choice(phrases), post.author.handle)

    # Create a facet to make the handle a link
    handle_start = message.find('@' + post.author.handle)
    handle_end = handle_start + len('@' + post.author.handle)
    facet = models.AppBskyRichtextFacet.Main(
        index=models.AppBskyRichtextFacet.ByteSlice(
            byteStart=handle_start,
            byteEnd=handle_end
        ),
        features=[
            models.AppBskyRichtextFacet.Mention(
                did=post.author.did
            )
        ]
    )

    parent_ref = models.create_strong_ref(models.dot_dict.DotDict({'uri': post.uri, 'cid': post.cid}))
    reply_ref = models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=parent_ref)

    with open(img, 'rb') as f:
        img_bytes = f.read()
        client.send_image(
            text=message,
            image=img_bytes,
            image_alt='Link, from The Legend of Zelda',
            reply_to=reply_ref,
            facets=[facet]
        )

if __name__ == '__main__':
    print("Running job...")
    last_post_time = get_last_post_time(TARGET_HANDLE)
    link_requests = search_posts_after(last_post_time, SEARCH_QUERY)
    for post in link_requests:
        reply_with_photo(post)
