from django.test import TestCase
from django.contrib.auth.models import User
from .models import Workout, Favorite, PublicPost
from django.utils import timezone
from .views import *

import unittest

class TestFavoriteFunctionality(unittest.TestCase):
    def setUp(self):
        User.objects.all().filter(username='test_user_no_favorite').delete()
        User.objects.all().filter(username='test_user_favorite').delete()
        User.objects.create_user('test_user_no_favorite', password='test_password')
        User.objects.create_user('test_user_favorite', password='test_password')

    # testing a user that has not been added to any favorites
    def test_no_add(self):
        f = Favorite.objects.all().filter(user='test_user_no_favorite')
        self.assertEqual(len(f), 0)

    # testing a user that has been added to any favorites
    def test_add(self):
        u = User.objects.all().filter(username='test_user_favorite')
        Favorite.objects.create(user='test_user_no_favorite', current_user=u[0],
                                id='test_user_no_favorite' + '_' + 'test_user_favorite')
        f2 = Favorite.objects.all().filter(user='test_user_no_favorite')
        self.assertEqual(len(f2), 1)

    def tearDown(self):
        User.objects.all().filter(username='test_user_no_favorite').delete()
        User.objects.all().filter(username='test_user_favorite').delete()
        Favorite.objects.all().filter(user='test_user_no_favorite').delete()


# tests Workout functionality -- makes sure new Workout appears as most recent in Workout.objects.all()
class TestRecentWorkoutFunctionality(unittest.TestCase):
    def setUp(self):
        User.objects.all().filter(username='workout_test').delete()
        Workout.objects.all().filter(note='here is my workout').delete()
        User.objects.create_user('workout_test', password='test_password')

    def test_workout(self):
        u = User.objects.all().filter(username='workout_test')
        w = Workout.objects.create(user=u[0], partner_username='m', workout_type='strength', duration="00:30:00",
                                   date=timezone.now(), note='here is my workout')

        self.assertEquals(w, Workout.objects.filter(date__lte=timezone.now()).order_by('-date')[0])

    def tearDown(self):
        User.objects.all().filter(username='workout_test').delete()
        Workout.objects.all().filter(note='here is my workout').delete()


# Tests search functionality by testing Python logic that is similar to how the search bar finds matches
class TestSearchFunctionality(unittest.TestCase):
    def test_match(self):
        users = User.objects.filter(username__startswith='kee')

        self.assertFalse(len(users) == 0)


# Tests to make sure workouts can be created with and without partners
class TestPartnerCreationFunctionality(unittest.TestCase):
    def setUp(self):
        User.objects.all().filter(username='workout_test').delete()
        Workout.objects.all().filter(note='here is my workout').delete()
        User.objects.create_user('workout_test', password='test_password')

    def test_partner(self):
        u = User.objects.all().filter(username='workout_test')

        self.assertTrue(
            Workout.objects.create(user=u[0], partner_username='m', workout_type='strength', duration="00:30:00",
                                   date=timezone.now(), note='here is my workout'))

    def test_no_partner(self):
        v = User.objects.all().filter(username='workout_test')

        self.assertTrue(
            Workout.objects.create(user=v[0], workout_type='strength', duration="00:30:00", date=timezone.now(),
                                   note='here is my workout'))

    def tearDown(self):
        User.objects.all().filter(username='workout_test').delete()
        Workout.objects.all().filter(note='here is my workout').delete()


# replicates Python logic in logWorkout view to ensure that we are correctly cheking that only valid users are added as workout partners
class TestPartnerValidityFunctionality(unittest.TestCase):

    def test_find_valid_partner(self):
        username_list = []
        for elem in User.objects.values('username'):
            username_list.append(elem['username'])

        real_username = 'keerthi'

        self.assertTrue(real_username in username_list)

    def test_find_invalid_username(self):
        username_list = []
        for elem in User.objects.values('username'):
            username_list.append(elem['username'])

        fake_username = 'keerthi_fake_account'

        self.assertFalse(fake_username in username_list)


class TestLevelingUpFunctionality(unittest.TestCase):
    def testLeveling(self):
        points = 0
        temp = levelCalculationHelper(points)
        level = temp[0]
        remainder = temp[1]
        percentage = temp[2]

        self.assertEquals(level, 1)
        self.assertEquals(remainder, 40)
        self.assertEquals(percentage, 0)

    def testLeveling2(self):
        points = 40
        temp = levelCalculationHelper(points)
        level = temp[0]
        remainder = temp[1]
        percentage = temp[2]

        self.assertEquals(level, 2)
        self.assertEquals(remainder, 90)
        self.assertEquals(percentage, 0)

    def testLeveling3(self):
        points = 9280
        temp = levelCalculationHelper(points)
        level = temp[0]
        remainder = temp[1]
        percentage = temp[2]

        self.assertEquals(level, 16)
        self.assertEquals(remainder, 0)
        self.assertEquals(percentage, 0)

    def testLeveling3(self):
        points = 9279
        temp = levelCalculationHelper(points)
        level = temp[0]
        remainder = temp[1]
        percentage = temp[2]

        self.assertEquals(level, 15)
        self.assertEquals(remainder, 1)
        self.assertEquals(percentage, 99)


# class TestCommunityPost(TestCase):
#     def setUp(self) -> None:
#         User.objects.all().filter(username='communityPostTestUser').delete()
#         User.objects.create_user('communityPostTestUser', password='test_password')
#         #login = self.client.login(username = "communityPostTestUser", password = 'test_password')
#     def testPostCreation(self):
#         login = self.client.login(username = "communityPostTestUser", password = 'test_password')
#         testTitle = "Test title"
#         testContent = "Test content"
#         data ={'post_title':testTitle,'post_content':testContent}
#         response = self.client.post(reverse('submitPost'),data,content_type='application/x-www-form-urlencoded')
#         #self.assertContains(response,testTitle,html=True)
#         #self.assertContains(response,testContent,html=True)
#         getPost = PublicPost.objects.filter(user=User.objects.all().filter(username='communityPostTestUser')[0].id)
#         print(getPost)
#         pass
class TestCommunityPost(unittest.TestCase):
    def setUp(self):
        User.objects.all().filter(username='communityPostTestUser').delete()
        User.objects.create_user('communityPostTestUser', password='test_password')
        PublicPost.objects.all().filter(title='delete_TestTitle2').delete()

    def test_postCreation(self):
        u = User.objects.all().filter(username='communityPostTestUser')
        self.assertTrue(
            PublicPost.objects.create(user=u[0], content='TestContent', title='TestTitle', date=timezone.now()))

    def test_postDeletion(self):
        u = User.objects.all().filter(username='communityPostTestUser')
        PublicPost.objects.create(user=u[0], content='TestContent2', title='delete_TestTitle2', date=timezone.now(),
                                  is_highlighted=False)
        PublicPost.objects.all().filter(title='delete_TestTitle2').delete()
        d = PublicPost.objects.all().filter(title='delete_TestTitle2')
        self.assertEqual(len(d), 0)

    def tearDown(self):
        User.objects.all().filter(username='communityPostTestUser').delete()
        PublicPost.objects.all().filter(content='TestContent').delete()


class TestAddPoints(unittest.TestCase):
    def setUp(self):
        User.objects.all().filter(username='pointTestUser').delete()
        User.objects.create_user('pointTestUser', password='test_password')
        u = User.objects.all().filter(username='pointTestUser')
        UserProfile.objects.create(user=u[0], email="test@test.com", firstName="test", lastName="testLast", weight=150,
                                   points=0)

    def test_addPoints(self):
        # print(request.user)
        up = UserProfile.objects.get(email="test@test.com")
        up.points = 0
        up.points += 100
        up.save()
        self.assertEquals(up.points, 100)

    def test_deletePoints(self):
        # print(request.user)
        up = UserProfile.objects.get(email="test@test.com")
        up.points = 0
        up.points += 100
        up.points -= 100
        up.save()
        self.assertEquals(up.points, 0)

    def tearDown(self) -> None:
        u = User.objects.all().filter(username='pointTestUser')
        UserProfile.objects.all().filter(user=u[0]).delete()
        u.delete()


# tests Nutrition log functionality -- makes sure new Nutrition log appears as most recent in Nutrition.objects.all()
class TestRecentNutritionFunctionality(unittest.TestCase):
    def setUp(self):
        User.objects.all().filter(username='nutri_test').delete()
        Nutrition.objects.all().filter(title='breakfast_test').delete()
        User.objects.create_user('nutri_test', password='test_password')

    def test_workout(self):
        u = User.objects.all().filter(username='nutri_test')
        n = Nutrition.objects.create(user=u[0], title='breakfast_test', text='test', date=timezone.now())

        self.assertEquals(n, Nutrition.objects.filter(date__lte=timezone.now()).order_by('-date')[0])

    def tearDown(self):
        User.objects.all().filter(username='nutri_test').delete()
        Nutrition.objects.all().filter(title='breakfast_test').delete()


# tests delete Nutrition log functionality -- makes sure Nutrition log no longer appears in Nutrition.objects.all() after deletion
class TestDeleteNutritionFunctionality(unittest.TestCase):
    def setUp(self):
        User.objects.all().filter(username='delete_nutri_test').delete()
        Nutrition.objects.all().filter(title='delete_breakfast_test').delete()
        User.objects.create_user('delete_nutri_test', password='test_password')

    def test_workout(self):
        u = User.objects.all().filter(username='delete_nutri_test')
        n = Nutrition.objects.create(user=u[0], title='delete_breakfast_test', text='test', date=timezone.now())

        Nutrition.objects.all().filter(title='delete_breakfast_test').delete()
        d = Nutrition.objects.all().filter(title='delete_breakfast_test')
        self.assertEqual(len(d), 0)

    def tearDown(self):
        User.objects.all().filter(username='delete_nutri_test').delete()
        Nutrition.objects.all().filter(title='delete_breakfast_test').delete()


# tests the blog posting system of the recommended workouts
class Basic_Recommended_Model_tests(unittest.TestCase):

    def setUp(self):
        person = User.objects.create_user(username="randomname", password="hello")
        test = Recommended.objects.create(
            title="helloworld",
            slug="helloworld",
            author=person,
            updated_on=timezone.now(),
            content="hello jello",
            created_on=timezone.now(),
            status=1
        )
        test.save()

    def test_reccomended_title_is_correct(self):
        array = Recommended.objects.filter(title="helloworld")
        self.assertEqual((array)[0].title, "helloworld")

    def test_reccomended_slug_is_correct(self):
        array = Recommended.objects.filter(slug="helloworld")
        self.assertEqual((array)[0].slug, "helloworld")

    # check if post is published when we choose publish
    def test_reccomended_status_is_correct(self):
        array = Recommended.objects.filter(status=1)
        self.assertEqual((array)[0].status, 1)

    def test_reccomended_content_is_correct(self):
        array = Recommended.objects.filter(content="hello jello")
        self.assertEqual((array)[0].content, "hello jello")

    def test_reccomended_status_is_not_draft(self):
        array = Recommended.objects.filter(status=1)
        self.assertNotEqual((array)[0].status, 0)

    def tearDown(self):
        User.objects.all().filter(username='randomname').delete()
        Recommended.objects.all().filter(title='helloworld').delete()


# mimics the functionality of othersWorkout.html to verify that private posts do not appear in the list of public posts
class Test_Privacy(unittest.TestCase):

    def setUp(self):
        User.objects.all().filter(username='workout_test').delete()
        User.objects.all().filter(username='workout_test_').delete()
        Workout.objects.all().filter(note='here is my workout').delete()

    # tests default of public
    def test_default(self):
        u = User.objects.create_user('workout_test', password='test_password')
        w = Workout.objects.create(user=u, partner_username='m', workout_type='strength', duration="00:30:00",
                                   date=timezone.now(), note='here is my workout')

        self.assertTrue(w.is_private == False)

    def test_not_default(self):
        u = User.objects.create_user('workout_test', password='test_password')
        w = Workout.objects.create(user=u, partner_username='m', workout_type='strength', duration="00:30:00",
                                   date=timezone.now(), note='here is my workout', is_private=False)
        w.is_private = True
        w.save()
        self.assertTrue(w not in Workout.objects.all().filter(is_private=False))
        self.assertTrue(w.is_private)

    def test_not_default2(self):
        u = User.objects.create_user('workout_test_', password='test_password')
        w = Workout.objects.create(user=u, partner_username='m', workout_type='strength', duration="00:30:00",
                                   date=timezone.now(), note='here is my workout', is_private=False)
        self.assertTrue(w in Workout.objects.all().filter(is_private=False))
        self.assertFalse(w.is_private)

    def tearDown(self):
        User.objects.all().filter(username='workout_test').delete()
        User.objects.all().filter(username='workout_test_').delete()
        Workout.objects.all().filter(note='here is my workout').delete()

class Test_Workout_Logging(unittest.TestCase):
    def setUp(self):
        User.objects.all().filter(username='workout_test').delete()
        User.objects.all().filter(username='workout_test2').delete()
        User.objects.all().filter(username='workout_test3').delete()
        User.objects.all().filter(username='workout_test4').delete()
        User.objects.all().filter(username='workout_test5').delete()
        User.objects.all().filter(username='workout_test6').delete()
        Workout.objects.all().filter(note='here is my workout').delete()
        Workout.objects.all().filter(note='workout test 5 note').delete()
        Workout.objects.all().filter(note='workout test 6 note').delete()

    def test_workout_type(self):
        u = User.objects.create_user('workout_test', password='test_password')
        w = Workout.objects.create(user=u, partner_username='m', workout_type='Bike Ride', duration="00:30:00",
                                   date=timezone.now(), note='here is my workout')
        self.assertEquals(w.workout_type, 'Bike Ride')

    def test_username_too_long(self):
        username_val = "abcdefghiklmnopqrstuvwxyzabcdefghiklmnopqrstuvwxyzabcdefghiklmnopqrstuvwxyzabcdefghiklmnopqrstuvwxyzabcdefghiklmnopqrstuvwxyz" \
                       "abcdefghiklmnopqrstuvwxyzabcdefghiklmnopqrstuvwxyzabcdefghiklmnopqrstuvwxyzabcdefghiklmnopqrstuvwxyzabcdefghiklmnopqrstuvwxyz"
        self.assertTrue(len(username_val) > 200)

    def delete_workout_with_user(self):
        u = User.objects.create_user('workout_test5', password='test_password')
        Workout.objects.create(user=u, partner_username='m', workout_type='Bike Ride', duration="00:30:00", date=timezone.now(),
                                   note='workout test 5 note')
        User.objects.all().filter(username='workout_test5').delete()
        self.assertTrue(len(Workout.objects.all().filter(note='workout test 5 note'))==0)

    def dont_delete_user_with_workout(self):
        u = User.objects.create_user('workout_test6', password='test_password_abcdef56')
        w = Workout.objects.create(user=u, partner_username='m', workout_type='Bike Ride', duration="00:30:00", date=timezone.now(),
                                   note='workout test 6 note')
        Workout.objects.all().filter(note='workout test 6 note').delete()
        self.assertTrue(len(User.objects.all().filter(password='test_password_abcdef56'))!=0)

    @unittest.expectedFailure
    def test_wrong_format_duration(self):
        u = User.objects.create_user('workout_test2', password='test_password')
        self.assertTrue(Workout.objects.create(user=u, partner_username='m', workout_type='Bike Ride', duration='thirty', date = timezone.now(),
                                   note='here is my workout'))

    @unittest.expectedFailure
    def test_wrong_format_date(self):
        u = User.objects.create_user('workout_test3', password='test_password')
        self.assertTrue(
            Workout.objects.create(user=u, partner_username='m', workout_type='Bike Ride', duration="00:30:00",
                                   date=March30,
                                   note='here is my workout'))

    @unittest.expectedFailure
    def test_wrong_format_private(self):
        u = User.objects.create_user('workout_test4', password='test_password')
        self.assertTrue(
            Workout.objects.create(user=u, partner_username='m', workout_type='Bike Ride', duration="00:30:00",
                                   date=timezone.now(),
                                   note='here is my workout', is_private="not private"))

    def tearDown(self):
        User.objects.all().filter(username='workout_test').delete()
        User.objects.all().filter(username='workout_test2').delete()
        User.objects.all().filter(username='workout_test3').delete()
        User.objects.all().filter(username='workout_test4').delete()
        User.objects.all().filter(username='workout_test5').delete()
        User.objects.all().filter(username='workout_test6').delete()
        Workout.objects.all().filter(note='here is my workout').delete()
        Workout.objects.all().filter(note='workout test 5 note').delete()
        Workout.objects.all().filter(note='workout test 6 note').delete()


if __name__ == '__main__':
    unittest.main()
