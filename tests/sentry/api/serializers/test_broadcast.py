import pytest

from sentry.api.serializers.models.broadcast import AdminBroadcastSerializer
from sentry.models.broadcast import Broadcast
from sentry.models.user import User # Keep import for clarity
from sentry.testutils.cases import SerializerTestCase


class AdminBroadcastSerializerTest(SerializerTestCase):
    def test_simple(self):
        # self.user is created by SerializerTestCase and has an email
        user = self.user # Use the user created by the test case

        # Create a broadcast associated with this user using created_by_id=user object
        broadcast_with_creator = Broadcast.objects.create(
            message="Test Broadcast 1", title="Test Title 1", created_by_id=user # Assign the user object directly
        )

        # Instantiate the serializer
        serializer = AdminBroadcastSerializer()

        # Serialize the broadcast object
        # Pass empty attrs and the user object (required by serialize signature)
        result_with_creator = serializer.serialize(broadcast_with_creator, attrs={}, user=user)

        # Assert that the createdBy field equals the user's email
        assert result_with_creator["createdBy"] == user.email

        # Create another broadcast object without a creator using created_by_id=None
        broadcast_without_creator = Broadcast.objects.create(
            message="Test Broadcast 2", title="Test Title 2", created_by_id=None
        )

        # Serialize this second broadcast object
        result_without_creator = serializer.serialize(broadcast_without_creator, attrs={}, user=user)

        # Assert that the createdBy field is None
        assert result_without_creator["createdBy"] is None
