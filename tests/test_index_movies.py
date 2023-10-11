
def test_movie_search(client):
    response = client.get('/index/movies', query_string={'titleq': ''})
    assert response.status_code == 200, "Successful Title Search"

    response = client.get('/index/movies', query_string={'genreq': ''})
    assert response.status_code == 200, "Successful Title Search"

    response = client.get('/index/movies', query_string={'actorq': ''})
    assert response.status_code == 200, "Successful Title Search"

