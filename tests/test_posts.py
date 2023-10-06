from src.models.post_model import Post


def test_create_valid_post(auth_client, app):
    post = {
        "title": "My Title",
        "slug": "wood",
        "content": "Some awesome content, dude!!!"
    }
    response = auth_client.post("/add-post", data=post)
    with app.app_context():
        assert Post.query.count() == 1
        assert Post.query.first().title == post["title"]
