from urllib.parse import urlencode

from django.urls import reverse

list_link = reverse("misago:admin:users:accounts:index")


def test_view_redirects_if_redirected_flag_is_not_present_in_querystring(admin_client):
    response = admin_client.get(list_link)
    assert response.status_code == 302


def test_view_sets_redirect_flag_in_redirect_url(admin_client):
    response = admin_client.get(list_link)
    assert response.status_code == 302
    assert "redirected=1" in response["location"]


def test_view_checks_only_redirect_flag_presence_and_not_value(admin_client):
    response = admin_client.get(list_link + "?redirected")
    assert response.status_code == 200


def test_view_preserves_rest_of_querystring_in_redirect_url(admin_client):
    response = admin_client.get(list_link + "?username=test")
    assert response.status_code == 302
    assert "redirected=1" in response["location"]
    assert "username=test" in response["location"]


def test_unicode_is_preserved_in_redirect_querystring(admin_client):
    response = admin_client.get(list_link + "?username=łóć")
    assert response.status_code == 302
    assert urlencode({"username": "łóć"}) in response["location"]


def test_view_is_not_redirecting_if_flag_is_set_in_querystring(admin_client):
    response = admin_client.get("%s?redirected=1" % list_link)
    assert response.status_code == 200
