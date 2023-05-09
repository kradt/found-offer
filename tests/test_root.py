def test_user_auto_search(client, confirmed_user, auto_search):
    with client:
        response = client.post(
            "/auto-search",
            data={"title": auto_search["title"], "city": auto_search["city"], "salary": auto_search["salary"]},
            follow_redirects=True
        )
        assert response.request.path == "/me"
        assert response.status_code == 200

        search_pattern = confirmed_user.auto_search[0]
        assert search_pattern.title == auto_search["title"]
        assert search_pattern.city == auto_search["city"]
        assert search_pattern.salary == auto_search["salary"]


