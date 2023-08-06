from datetime import timedelta

from django.utils import timezone

from ...users.test import AuthenticatedUserTestCase
from ..api.postingendpoint import PostingInterrupt
from ..api.postingendpoint.floodprotection import FloodProtectionMiddleware

user_acl = {"can_omit_flood_protection": False}


class FloodProtectionMiddlewareTests(AuthenticatedUserTestCase):
    def test_flood_protection_middleware_on_no_posts(self):
        """middleware sets last_posted_on on user"""
        self.user.update_fields = []
        self.assertIsNone(self.user.last_posted_on)

        middleware = FloodProtectionMiddleware(user=self.user, user_acl=user_acl)
        middleware.interrupt_posting(None)

        self.assertIsNotNone(self.user.last_posted_on)

    def test_flood_protection_middleware_old_posts(self):
        """middleware is not interrupting if previous post is old"""
        self.user.update_fields = []

        original_last_posted_on = timezone.now() - timedelta(days=1)
        self.user.last_posted_on = original_last_posted_on

        middleware = FloodProtectionMiddleware(user=self.user, user_acl=user_acl)
        middleware.interrupt_posting(None)

        self.assertTrue(self.user.last_posted_on > original_last_posted_on)

    def test_flood_protection_middleware_on_flood(self):
        """middleware is interrupting flood"""
        self.user.last_posted_on = timezone.now()

        with self.assertRaises(PostingInterrupt):
            middleware = FloodProtectionMiddleware(user=self.user, user_acl=user_acl)
            middleware.interrupt_posting(None)

    def test_flood_permission(self):
        """middleware is respects permission to flood for team members"""
        can_omit_flood_protection_user_acl = {"can_omit_flood_protection": True}
        middleware = FloodProtectionMiddleware(
            user=self.user, user_acl=can_omit_flood_protection_user_acl
        )
        self.assertFalse(middleware.use_this_middleware())
