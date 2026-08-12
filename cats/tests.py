"""
Test suite for the cats app.

Covers:
- Model behaviour: defaults, __str__, ordering, unique_together constraints
- View behaviour: permissions (login-required, owner-only), context data,
  AJAX vs non-AJAX responses, and the core interactive features
  (favorite/paw, daily pet, visibility toggle, comment CRUD)

Storage note: the project's default file storage is Cloudinary
(see settings.STORAGES). Tests override this to a local FileSystemStorage
pointing at a temporary directory, so creating a Cat with an image never
makes a real network call during `manage.py test`.
"""

import io
import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Cat, Comment, Reaction, DailyPet
from .views import CATS_PER_SCENE


# ---------- Shared test setup ----------

TEST_MEDIA_ROOT = tempfile.mkdtemp()


def tearDownModule():
    """Runs once after every test in this module has finished."""
    shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)


def make_test_image(name='test-cat.png'):
    """Builds a tiny real PNG in memory so ImageField validation
    (which actually opens the file) passes, without touching disk
    or Cloudinary."""
    from PIL import Image

    buffer = io.BytesIO()
    Image.new('RGB', (10, 10), color='blue').save(buffer, format='PNG')
    buffer.seek(0)
    return SimpleUploadedFile(name, buffer.read(), content_type='image/png')


@override_settings(
    MEDIA_ROOT=TEST_MEDIA_ROOT,
    STORAGES={
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    },
)
class BaseCatTestCase(TestCase):
    """Common fixtures shared by model and view tests."""

    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='pass12345')
        self.other_user = User.objects.create_user(username='rival', password='pass12345')

    def make_cat(self, owner=None, **overrides):
        defaults = {
            'owner': owner or self.owner,
            'name': 'Whiskers',
            'personality': 'Curious and a little dramatic.',
            'coat_color': 'deep_blue',
            'drawing_image': make_test_image(),
            'is_public': True,
        }
        defaults.update(overrides)
        return Cat.objects.create(**defaults)


# ==================== MODEL TESTS ====================

class CatModelTests(BaseCatTestCase):

    def test_str_includes_name_and_owner(self):
        cat = self.make_cat(name='Biscuit')
        self.assertEqual(str(cat), 'Biscuit (by owner)')

    def test_defaults(self):
        cat = self.make_cat()
        self.assertTrue(cat.is_public)
        self.assertEqual(cat.coat_color, 'deep_blue')

    def test_ordering_is_newest_first(self):
        older = self.make_cat(name='Older')
        newer = self.make_cat(name='Newer')
        cats = list(Cat.objects.all())
        self.assertEqual(cats[0], newer)
        self.assertEqual(cats[1], older)


class CommentModelTests(BaseCatTestCase):

    def test_str_and_ordering(self):
        cat = self.make_cat()
        first = Comment.objects.create(cat=cat, author=self.owner, body='First!')
        second = Comment.objects.create(cat=cat, author=self.other_user, body='Second!')

        self.assertEqual(str(first), f'Comment by owner on {cat.name}')
        # Oldest first, unlike Cat which is newest-first
        comments = list(cat.comments.all())
        self.assertEqual(comments[0], first)
        self.assertEqual(comments[1], second)


class ReactionModelTests(BaseCatTestCase):

    def test_str(self):
        cat = self.make_cat()
        reaction = Reaction.objects.create(cat=cat, user=self.other_user)
        self.assertEqual(str(reaction), f'rival reacted to {cat.name}')

    def test_one_reaction_per_user_per_cat(self):
        cat = self.make_cat()
        Reaction.objects.create(cat=cat, user=self.other_user)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Reaction.objects.create(cat=cat, user=self.other_user)


class DailyPetModelTests(BaseCatTestCase):

    def test_str(self):
        cat = self.make_cat()
        today = timezone.localdate()
        pet = DailyPet.objects.create(cat=cat, user=self.other_user, date=today)
        self.assertEqual(str(pet), f'rival petted {cat.name} on {today}')

    def test_one_pet_per_user_per_cat_per_day(self):
        cat = self.make_cat()
        today = timezone.localdate()
        DailyPet.objects.create(cat=cat, user=self.other_user, date=today)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                DailyPet.objects.create(cat=cat, user=self.other_user, date=today)


# ==================== VIEW TESTS ====================

class SceneViewTests(BaseCatTestCase):

    def test_only_public_cats_shown(self):
        self.make_cat(name='Visible', is_public=True)
        self.make_cat(name='Hidden', is_public=False)

        response = self.client.get(reverse('scene'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cats/scene.html')
        names = [cat.name for cat in response.context['cats']]
        self.assertIn('Visible', names)
        self.assertNotIn('Hidden', names)

    def test_anonymous_user_gets_empty_interaction_lists(self):
        response = self.client.get(reverse('scene'))
        self.assertEqual(response.context['petted_cat_ids'], [])
        self.assertEqual(response.context['reacted_cat_ids'], [])

    def test_authenticated_user_sees_own_reactions_and_pets(self):
        cat = self.make_cat()
        Reaction.objects.create(cat=cat, user=self.owner)
        DailyPet.objects.create(cat=cat, user=self.owner, date=timezone.localdate())

        self.client.login(username='owner', password='pass12345')
        response = self.client.get(reverse('scene'))

        self.assertIn(cat.pk, response.context['reacted_cat_ids'])
        self.assertIn(cat.pk, response.context['petted_cat_ids'])

    def test_cat_of_the_day_is_the_most_petted(self):
        popular = self.make_cat(name='Popular')
        quiet = self.make_cat(name='Quiet')
        DailyPet.objects.create(cat=popular, user=self.owner, date=timezone.localdate())
        DailyPet.objects.create(cat=popular, user=self.other_user, date=timezone.localdate())
        DailyPet.objects.create(cat=quiet, user=self.owner, date=timezone.localdate())

        response = self.client.get(reverse('scene'))
        self.assertEqual(response.context['cat_of_the_day'], popular)

    def test_scene_cats_are_ordered_newest_first_across_pages(self):
        # Create more cats than one page holds, with names encoding their
        # creation order, so we can assert the exact sequence Paginator
        # sees is deterministic (newest first) rather than DB-default
        # (which becomes undefined once .annotate() is involved without
        # an explicit .order_by()).
        cats_in_creation_order = [
            self.make_cat(name=f'Cat {i}') for i in range(CATS_PER_SCENE + 2)
        ]

        response = self.client.get(reverse('scene'))
        page_one_names = [cat.name for cat in response.context['cats']]

        expected_first_page = [
            cat.name for cat in reversed(cats_in_creation_order)
        ][:CATS_PER_SCENE]

        self.assertEqual(page_one_names, expected_first_page)


class GalleryViewTests(BaseCatTestCase):

    def test_only_public_cats_listed(self):
        self.make_cat(name='Visible', is_public=True)
        self.make_cat(name='Hidden', is_public=False)

        response = self.client.get(reverse('gallery'))

        self.assertEqual(response.status_code, 200)
        names = [cat.name for cat in response.context['cats']]
        self.assertIn('Visible', names)
        self.assertNotIn('Hidden', names)


class MyCatsViewTests(BaseCatTestCase):

    def test_requires_login(self):
        response = self.client.get(reverse('my_cats'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_only_shows_own_cats(self):
        mine = self.make_cat(owner=self.owner, name='Mine')
        self.make_cat(owner=self.other_user, name='TheirsNotMine')

        self.client.login(username='owner', password='pass12345')
        response = self.client.get(reverse('my_cats'))

        cats = list(response.context['cats'])
        self.assertIn(mine, cats)
        self.assertEqual(len(cats), 1)


class CatDetailViewTests(BaseCatTestCase):

    def test_user_has_reacted_flag(self):
        cat = self.make_cat()
        Reaction.objects.create(cat=cat, user=self.owner)

        self.client.login(username='owner', password='pass12345')
        response = self.client.get(reverse('cat_detail', kwargs={'pk': cat.pk}))
        self.assertTrue(response.context['user_has_reacted'])

    def test_anonymous_user_has_reacted_is_false(self):
        cat = self.make_cat()
        response = self.client.get(reverse('cat_detail', kwargs={'pk': cat.pk}))
        self.assertFalse(response.context['user_has_reacted'])


class CatCreateViewTests(BaseCatTestCase):

    def test_requires_login(self):
        response = self.client.get(reverse('cat_create'))
        self.assertEqual(response.status_code, 302)

    def test_creating_a_cat_sets_owner_and_redirects_to_scene(self):
        self.client.login(username='owner', password='pass12345')
        response = self.client.post(reverse('cat_create'), {
            'name': 'New Cat',
            'personality': 'Sleepy',
            'coat_color': 'mint',
            'drawing_image': make_test_image(),
            'is_public': 'on',
        })

        self.assertRedirects(response, reverse('scene'))
        cat = Cat.objects.get(name='New Cat')
        self.assertEqual(cat.owner, self.owner)

    def test_invalid_coat_color_is_rejected(self):
        self.client.login(username='owner', password='pass12345')
        response = self.client.post(reverse('cat_create'), {
            'name': 'Bad Color Cat',
            'personality': 'N/A',
            'coat_color': 'dusty_rose',  # not a valid choice
            'drawing_image': make_test_image(),
        })

        # Validation failure re-renders the form instead of redirecting
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Cat.objects.filter(name='Bad Color Cat').exists())


class CatUpdateDeleteViewTests(BaseCatTestCase):

    def test_owner_can_access_update_form(self):
        cat = self.make_cat()
        self.client.login(username='owner', password='pass12345')
        response = self.client.get(reverse('cat_update', kwargs={'pk': cat.pk}))
        self.assertEqual(response.status_code, 200)

    def test_non_owner_forbidden_from_update(self):
        cat = self.make_cat(owner=self.owner)
        self.client.login(username='rival', password='pass12345')
        response = self.client.get(reverse('cat_update', kwargs={'pk': cat.pk}))
        self.assertEqual(response.status_code, 403)

    def test_non_owner_forbidden_from_delete(self):
        cat = self.make_cat(owner=self.owner)
        self.client.login(username='rival', password='pass12345')
        response = self.client.post(reverse('cat_delete', kwargs={'pk': cat.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Cat.objects.filter(pk=cat.pk).exists())

    def test_owner_can_delete(self):
        cat = self.make_cat(owner=self.owner)
        self.client.login(username='owner', password='pass12345')
        response = self.client.post(reverse('cat_delete', kwargs={'pk': cat.pk}))
        self.assertRedirects(response, reverse('my_cats'))
        self.assertFalse(Cat.objects.filter(pk=cat.pk).exists())


class ToggleVisibilityTests(BaseCatTestCase):

    def test_owner_can_toggle(self):
        cat = self.make_cat(owner=self.owner, is_public=True)
        self.client.login(username='owner', password='pass12345')
        self.client.post(reverse('cat_toggle_visibility', kwargs={'pk': cat.pk}))
        cat.refresh_from_db()
        self.assertFalse(cat.is_public)

    def test_non_owner_gets_404_not_error_page(self):
        # toggle_visibility filters by owner=request.user in get_object_or_404,
        # so a non-owner should get a 404, never silently succeed
        cat = self.make_cat(owner=self.owner)
        self.client.login(username='rival', password='pass12345')
        response = self.client.post(reverse('cat_toggle_visibility', kwargs={'pk': cat.pk}))
        self.assertEqual(response.status_code, 404)


class CommentTests(BaseCatTestCase):

    def test_add_comment_requires_login(self):
        cat = self.make_cat()
        response = self.client.post(reverse('comment_create', kwargs={'pk': cat.pk}), {
            'body': 'Cute cat!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.exists())

    def test_add_comment_creates_and_redirects(self):
        cat = self.make_cat()
        self.client.login(username='rival', password='pass12345')
        response = self.client.post(reverse('comment_create', kwargs={'pk': cat.pk}), {
            'body': 'Cute cat!',
        })
        self.assertRedirects(response, reverse('cat_detail', kwargs={'pk': cat.pk}))
        self.assertTrue(Comment.objects.filter(cat=cat, body='Cute cat!').exists())

    def test_blank_comment_is_not_created(self):
        cat = self.make_cat()
        self.client.login(username='rival', password='pass12345')
        self.client.post(reverse('comment_create', kwargs={'pk': cat.pk}), {'body': '   '})
        self.assertFalse(Comment.objects.exists())

    def test_only_author_can_edit_comment(self):
        cat = self.make_cat()
        comment = Comment.objects.create(cat=cat, author=self.owner, body='Mine')

        self.client.login(username='rival', password='pass12345')
        response = self.client.get(reverse('comment_update', kwargs={'pk': comment.pk}))
        self.assertEqual(response.status_code, 403)

    def test_only_author_can_delete_comment(self):
        cat = self.make_cat()
        comment = Comment.objects.create(cat=cat, author=self.owner, body='Mine')

        self.client.login(username='rival', password='pass12345')
        response = self.client.post(reverse('comment_delete', kwargs={'pk': comment.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Comment.objects.filter(pk=comment.pk).exists())


class ToggleReactionTests(BaseCatTestCase):

    def test_requires_login(self):
        cat = self.make_cat()
        response = self.client.post(reverse('cat_react', kwargs={'pk': cat.pk}))
        self.assertEqual(response.status_code, 302)

    def test_first_click_adds_reaction_ajax(self):
        cat = self.make_cat()
        self.client.login(username='rival', password='pass12345')
        response = self.client.post(
            reverse('cat_react', kwargs={'pk': cat.pk}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['reacted'])
        self.assertEqual(data['count'], 1)

    def test_second_click_removes_reaction(self):
        cat = self.make_cat()
        Reaction.objects.create(cat=cat, user=self.other_user)

        self.client.login(username='rival', password='pass12345')
        response = self.client.post(
            reverse('cat_react', kwargs={'pk': cat.pk}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = response.json()
        self.assertFalse(data['reacted'])
        self.assertEqual(data['count'], 0)

    def test_non_ajax_request_redirects_to_detail(self):
        cat = self.make_cat()
        self.client.login(username='rival', password='pass12345')
        response = self.client.post(reverse('cat_react', kwargs={'pk': cat.pk}))
        self.assertRedirects(response, reverse('cat_detail', kwargs={'pk': cat.pk}))


class PetCatTests(BaseCatTestCase):

    def test_requires_login(self):
        cat = self.make_cat()
        response = self.client.post(reverse('cat_pet', kwargs={'pk': cat.pk}))
        self.assertEqual(response.status_code, 302)

    def test_first_pet_today_ajax(self):
        cat = self.make_cat()
        self.client.login(username='rival', password='pass12345')
        response = self.client.post(
            reverse('cat_pet', kwargs={'pk': cat.pk}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = response.json()
        self.assertTrue(data['petted_today'])
        self.assertFalse(data['already_petted'])
        self.assertEqual(data['today_count'], 1)

    def test_repeat_pet_same_day_is_flagged_already_petted(self):
        cat = self.make_cat()
        self.client.login(username='rival', password='pass12345')
        self.client.post(
            reverse('cat_pet', kwargs={'pk': cat.pk}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        response = self.client.post(
            reverse('cat_pet', kwargs={'pk': cat.pk}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = response.json()
        self.assertTrue(data['already_petted'])
        # Still only one DailyPet row exists thanks to unique_together
        self.assertEqual(DailyPet.objects.filter(cat=cat, user=self.other_user).count(), 1)


class SignUpViewTests(BaseCatTestCase):

    def test_signup_page_loads(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_creates_user(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newcatlover',
            'password1': 'a-very-secure-pw-93',
            'password2': 'a-very-secure-pw-93',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newcatlover').exists())