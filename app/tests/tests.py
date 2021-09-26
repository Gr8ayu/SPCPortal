import pytest
from mixer.backend.django import mixer
from app.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_pytest_working():
    assert 2 + 2 == 4


@pytest.mark.django_db
def test_access_user_unauthenticated(client):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    # Use this:
    # client.force_login(user)
    # Or this:
    # client.login(username=username, password=password)
    url = reverse("dashboard")
    response = client.get(url)

    assert response.status_code == 302
    assert "login" in response.url


@pytest.mark.django_db
def test_access_student_dashboard_authenticated(client):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    url = reverse("dashboard")
    response = client.get(url)

    assert response.status_code == 200
    assert "Logout" in str(response.content)
    assert "Name" in str(response.content)


@pytest.mark.django_db
def test_access_faculty_dashboard_authenticated(client):
    username = "user1"
    password = "bar"
    User.objects.create_user(
        username=username, password=password, user_type="TEACHER"
    )
    client.login(username=username, password=password)
    url = reverse("dashboard")
    response = client.get(url)
    assert response.status_code == 200
    assert "Logout" in str(response.content)
    assert "teacher dashboard" in str(response.content)


@pytest.mark.django_db
def test_access_admin_dashboard_authenticated(client):
    username = "user1"
    password = "bar"
    User.objects.create_user(
        username=username, password=password, user_type="ADMIN"
    )

    client.login(username=username, password=password)
    url = reverse("dashboard")
    response = client.get(url)

    assert response.status_code == 200
    assert "Logout" in str(response.content)
    assert "admin dashboard" in str(response.content)


GET_URLS = [
    ("home", {}, 200),
    ("dashboard", {}, 200),
    ("edit_profile", {}, 200),
    ("edit_profile_contact", {}, 405),
    ("edit_profile_education", {}, 405),
    ("edit_profile_details", {}, 405),
    ("offers", {}, 200),
    ("offer_details", {"pk": 1}, 200),
    ("offer_alert", {"pk": 1}, 302),
    ("companies", {}, 200),
    ("company_details", {"pk": 1}, 200),
    ("my_applications", {}, 200),
    ("add_application", {"id": 1}, 302),
]


@pytest.mark.django_db
@pytest.mark.parametrize("url, agruments, status", GET_URLS)
def test_get_urls_authenticated(client, url, agruments, status):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    mixer.cycle(10).blend("app.company")
    mixer.cycle(5).blend("app.offer")

    url = reverse(url, kwargs=agruments)
    response = client.get(url)

    assert response.status_code == status


POST_URLS = [
    ("edit_profile_contact", {}, 302),
    ("edit_profile_education", {}, 302),
    ("edit_profile_details", {}, 302),
]


@pytest.mark.django_db
@pytest.mark.parametrize("url, agruments, status", POST_URLS)
def test_post_urls_authenticated(client, url, agruments, status):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    mixer.cycle(10).blend("app.company")
    mixer.cycle(5).blend("app.offer")

    url = reverse(url, kwargs=agruments)
    response = client.post(url)

    assert response.status_code == status


@pytest.mark.django_db
def test_send_email_update(client):
    username = "user1"
    password = "bar"
    User.objects.create_user(
        username=username, password=password, user_type="ADMIN"
    )
    client.login(username=username, password=password)

    mixer.cycle(10).blend("app.company")
    mixer.cycle(5).blend("app.offer")

    url = reverse("offer_alert", kwargs={"pk": 1})
    response = client.post(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_send_email_update_get(client):
    username = "user1"
    password = "bar"
    User.objects.create_user(
        username=username, password=password, user_type="ADMIN"
    )
    client.login(username=username, password=password)

    mixer.cycle(10).blend("app.company")
    mixer.cycle(5).blend("app.offer")

    url = reverse("offer_alert", kwargs={"pk": 1})
    response = client.get(url)

    assert response.status_code == 200
