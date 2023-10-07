from src.models.post_model import Post


def test_create_valid_post(auth_client, app):
    post = {
        "title": "My Title",
        "slug": "wood",
        "content": "Some awesome content, dude!!!"
    }
    auth_client.post("/add-post", data=post)
    with app.app_context():
        assert Post.query.count() == 1
        assert Post.query.first().title == post["title"]


def test_show_posts(auth_client, postdb):
    response = auth_client.get("/posts")
    assert postdb.title in response.data.decode("utf=8")
    assert postdb.content in response.data.decode("utf=8")


def test_show_single_post(auth_client, postdb):
    response = auth_client.get("/posts/1")
    assert postdb.title in response.data.decode("utf=8")
    assert postdb.content in response.data.decode("utf=8")


def test_edit_post(auth_client, postdb, app):
    post = {
        "title": "Updated Title",
        "content": "Updated Post Content",
        "slug": postdb.slug
    }
    auth_client.post("/posts/edit/1", data=post)
    with app.app_context():
        p = Post.query.filter_by(id=1).first()
        assert p.title == post["title"]
        assert p.content == post["content"]


def test_delete_post(auth_client, postdb, app):
    auth_client.get("/posts/delete/1")
    with app.app_context():
        assert Post.query.count() == 0


def test_search_post(auth_client, postdb, app):
    response = auth_client.post("/search", data={"searched": "awesome"})
    assert b" <h2>You Searched For: <em>awesome</em></h2>" in response.data
    assert postdb.content in response.data.decode("utf-8")
