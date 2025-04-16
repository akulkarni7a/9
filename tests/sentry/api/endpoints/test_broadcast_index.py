from django.urls import reverse

from sentry.models.broadcast import Broadcast, BroadcastSeen
from sentry.testutils.cases import APITestCase
from sentry.testutils.silo import control_silo_test


@control_silo_test
class BroadcastListTest(APITestCase):
    def test_simple(self):
        broadcast1 = Broadcast.objects.create(message="bar", is_active=True)
        Broadcast.objects.create(message="foo", is_active=False)

        self.add_user_permission(user=self.user, permission="broadcasts.admin")
        self.login_as(user=self.user)

        response = self.client.get("/api/0/broadcasts/")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == str(broadcast1.id)

    def test_superuser_with_all(self):
        Broadcast.objects.create(message="bar", is_active=True)
        creator_user = self.create_user(email="creator@example.com")
        broadcast_with_creator = Broadcast.objects.create(
            message="bar", is_active=True, created_by_id=creator_user.id
        )
        broadcast_without_creator = Broadcast.objects.create(
            message="foo", is_active=False, created_by_id=None
        )

        admin_user = self.create_user(email="admin@example.com", is_superuser=True)
        self.add_user_permission(user=admin_user, permission="broadcasts.admin")
        self.login_as(user=admin_user, superuser=True)

        response = self.client.get("/api/0/broadcasts/?show=all")
        assert response.status_code == 200
        assert len(response.data) == 2

        # Sort data by message to ensure consistent order for assertions
        response_data = sorted(response.data, key=lambda x: x["message"])

        # Check broadcast_with_creator ('bar')
        assert response_data[0]["id"] == str(broadcast_with_creator.id)
        assert response_data[0]["createdBy"] == creator_user.email

        # Check broadcast_without_creator ('foo')
        assert response_data[1]["id"] == str(broadcast_without_creator.id)
        assert response_data[1]["createdBy"] is None

        # Re-run queries to ensure filtering still works with the new setup
        response = self.client.get("/api/0/broadcasts/?show=all&query=status:active")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == str(broadcast_with_creator.id)

        response = self.client.get("/api/0/broadcasts/?show=all&query=status:inactive")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == str(broadcast_without_creator.id)

        response = self.client.get("/api/0/broadcasts/?show=all&query=status:zzz")
        assert response.status_code == 200
        assert len(response.data) == 0

        response = self.client.get("/api/0/broadcasts/?show=all&query=foo") # broadcast_without_creator
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == str(broadcast_without_creator.id)

        response = self.client.get("/api/0/broadcasts/?show=all&query=bar") # broadcast_with_creator
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == str(broadcast_with_creator.id)

        response = self.client.get("/api/0/broadcasts/?show=all&query=zzz")
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_basic_user_with_all(self):
        broadcast1 = Broadcast.objects.create(message="bar", is_active=True)
        Broadcast.objects.create(message="foo", is_active=False, created_by_id=self.user)

        self.add_user_permission(user=self.user, permission="broadcasts.admin")
        self.login_as(user=self.user, superuser=False)

        response = self.client.get("/api/0/broadcasts/?show=all")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == str(broadcast1.id)
        assert "createdBy" not in response.data[0]

    def test_organization_filtering(self):
        broadcast1 = Broadcast.objects.create(message="foo", is_active=True)
        broadcast2 = Broadcast.objects.create(message="bar", is_active=True)

        self.add_user_permission(user=self.user, permission="broadcasts.admin")
        self.login_as(user=self.user)

        url = reverse("sentry-api-0-organization-broadcasts", args=[self.organization.slug])

        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 2
        assert str(broadcast1.id) in [str(broadcast["id"]) for broadcast in response.data]
        assert str(broadcast2.id) in [str(broadcast["id"]) for broadcast in response.data]


@control_silo_test
class BroadcastCreateTest(APITestCase):
    def test_basic_user(self):
        self.add_user_permission(user=self.user, permission="broadcasts.admin")
        self.login_as(user=self.user, superuser=False)

        response = self.client.post(
            "/api/0/broadcasts/",
            {
                "title": "bar",
                "message": "foo",
                "link": "http://example.com",
                "cta": "Read More",
                "mediaUrl": "http://example.com/image.png",
                "category": "announcement",
            },
        )

        assert response.status_code == 401

    def test_superuser(self):
        self.add_user_permission(user=self.user, permission="broadcasts.admin")
        self.login_as(user=self.user, superuser=True)

        response = self.client.post(
            "/api/0/broadcasts/",
            {
                "title": "bar",
                "message": "foo",
                "link": "http://example.com",
                "cta": "Read More",
                "mediaUrl": "http://example.com/image.png",
                "category": "announcement",
            },
        )

        assert response.status_code == 200, response.data

        broadcast = Broadcast.objects.get(id=response.data["id"])
        assert broadcast.title == "bar"
        assert broadcast.message == "foo"
        assert broadcast.cta == "Read More"
        assert broadcast.media_url == "http://example.com/image.png"
        assert broadcast.category == "announcement"
        assert broadcast.created_by_id == self.user

    def test_validation(self):
        self.add_user_permission(user=self.user, permission="broadcasts.admin")
        self.login_as(user=self.user, superuser=True)

        response = self.client.post(
            "/api/0/broadcasts/",
            {
                "title": "bar",
                "message": "foo",
                "link": "http://example.com",
                "cta": "Read More",
                "mediaUrl": "this is not a url",
                "category": "announcement",
            },
        )

        assert response.status_code == 400, response.data

        response = self.client.post(
            "/api/0/broadcasts/",
            {
                "title": "bar",
                "message": "foo",
                "link": "http://example.com",
                "cta": "Read More",
                "mediaUrl": "http://example.com/image.png",
                "category": "this is not a category",
            },
        )

        assert response.status_code == 400, response.data

        response = self.client.post(
            "/api/0/broadcasts/",
            {
                "title": "bar",
                "message": "foo",
                "link": "http://example.com",
                "cta": "Read More",
                "mediaUrl": "http://example.com/image.png",
                "category": "announcement",
            },
        )

        assert response.status_code == 200, response.data

        response = self.client.post(
            "/api/0/broadcasts/",
            {
                "title": "bar",
                "message": "foo",
                "link": "http://example.com",
                "cta": "Read More",
            },
        )

        assert response.status_code == 200, response.data

    def test_not_required_cta(self):
        self.add_user_permission(user=self.user, permission="broadcasts.admin")
        self.login_as(user=self.user, superuser=True)

        response = self.client.post(
            "/api/0/broadcasts/",
            {
                "title": "bar",
                "message": "foo",
                "link": "http://example.com",
                "mediaUrl": "http://example.com/image.png",
                "category": "announcement",
            },
        )

        assert response.status_code == 200, response.data


@control_silo_test
class BroadcastUpdateTest(APITestCase):
    def test_simple(self):
        broadcast1 = Broadcast.objects.create(message="bar", is_active=True)
        broadcast2 = Broadcast.objects.create(message="foo", is_active=False)

        self.login_as(user=self.user)
        response = self.client.put("/api/0/broadcasts/", {"hasSeen": "1"})
        assert response.status_code == 200
        assert response.data["hasSeen"]

        assert BroadcastSeen.objects.filter(user=self.user, broadcast=broadcast1).exists()
        assert not BroadcastSeen.objects.filter(user=self.user, broadcast=broadcast2).exists()
