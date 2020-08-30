from django.test import TestCase
from django.urls import reverse

from .models import Produits, Favoris, categories

from django.contrib.auth.models import User
from .class_search import ClassSearch, lien_nutriscore
from .class_favoris import ClassFavoris

# Create your tests here.

class TestApp(TestCase):
    """ Mise en place des tests """

    def setUp(self):
        """ Mise en place des bases de données """
        test_user1 = User.objects.create_user(
            username="testuser1", password='testtest')
        test_user2 = User.objects.create_user(
            username="testuser2", password='testtest')

        test_user1.save()
        test_user2.save()

        id_produit1 = Produits.objects.create(
            id=1,
            ingredient ="NC",
            url_image_ingredients = "",
            brands_tags = ['test1','test2'],
            grade = 20,
            image_front_url = "NC",
            image_nutrition_url = "NC",
            nova_groups = "NC",
            generic_name_fr = 'Nutella Test produit',
            url_site = "https://testest.com",
            ingredients_text_fr = 'Blbablablabalba test',
            _id = 7895225)
        id_produit2 = Produits.objects.create(
            id=2,
            ingredient ="NC",
            url_image_ingredients = "",
            brands_tags = ['test1','test2'],
            grade = -5,
            image_front_url = "NC",
            image_nutrition_url = "NC",
            nova_groups = "NC",
            generic_name_fr = 'nutella Test 2 produit',
            url_site = "https://testest.com",
            ingredients_text_fr = 'Blbablablabalba test',
            _id = 7895225)
        id_produit3 = Produits.objects.create(
            id=3,
            ingredient ="NC",
            url_image_ingredients = "",
            brands_tags = ['test1','test2'],
            grade = 12,
            image_front_url = "NC",
            image_nutrition_url = "NC",
            nova_groups = "NC",
            generic_name_fr = 'nutella Test 3 produit',
            url_site = "https://testest.com",
            ingredients_text_fr = 'Blbablablabalba test',
            _id = 7895225)
        id_produit4 = Produits.objects.create(
            id=4,
            ingredient ="NC",
            url_image_ingredients = "",
            brands_tags = ['test1','test2'],
            grade = 0,
            image_front_url = "NC",
            image_nutrition_url = "NC",
            nova_groups = "NC",
            generic_name_fr = 'Test produit',
            url_site = "https://testest.com",
            ingredients_text_fr = 'Blbablablabalba test',
            _id = 7895225)

        id_produit1.save()
        id_produit2.save()
        id_produit3.save()
        id_produit4.save()

        #id_produit1 = Produits.objects.get(pk=1)
        #id_produit2 = Produits.objects.get(pk=2)

        test_favoris = Favoris.objects.create(
            user=test_user1,
            produits=id_produit1,
            date_ajout="08/06/2020",
            aff_index=False)
        test_favoris.save()
        test_favoris = Favoris.objects.create(
            user=test_user2,
            produits=id_produit1,
            date_ajout="08/06/2020",
            aff_index=False)
        test_favoris.save()
        test_favoris = Favoris.objects.create(
            user=test_user2,
            produits=id_produit2,
            date_ajout="08/06/2020",
            aff_index=False)
        test_favoris.save()
        test_favoris = Favoris.objects.create(
            user=test_user1,
            produits=id_produit1,
            date_ajout="08/06/2020",
            aff_index=False)
        test_favoris.save()
        test_favoris = Favoris.objects.create(
            user=test_user1,
            produits=id_produit1,
            date_ajout="08/06/2020",
            aff_index=True)
        test_favoris.save()

        test_cat = categories.objects.create(id=1, nom="Test cat 1", nom_iaccents="Test cat 1")
        test_cat.produit.add(id_produit1)
        test_cat.save()

        test_cat = categories.objects.create(id=2, nom="Test cat 2", nom_iaccents="Test cat 2")
        test_cat.produit.add(id_produit1)
        test_cat.save()

        test_cat = categories.objects.create(id=3, nom="Test cat 3", nom_iaccents="Test cat 3")
        test_cat.produit.add(id_produit1)
        test_cat.save()

        test_cat = categories.objects.create(id=4, nom="Gâteau", nom_iaccents="Gateau")
        test_cat.produit.add(id_produit4)
        test_cat.save()


    def test_favoris(self):
        ''' permet de tester les favoris
        allows to test the favorites '''
        self.client.login(username="testuser1", password='testtest')
        response = self.client.get(reverse('login'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')

        check_favoris = self.client.get('/purbeurre/favoris/')

        self.assertEqual(len(check_favoris.context['trouve']), 3)

        liste_favoris = check_favoris.context['trouve']

        x = 0
        for favoris in liste_favoris:
            if favoris['index']:
                x += 1

        self.assertEqual(x, 1)

        favoris_tbl = Favoris.objects.all()

        for item in favoris_tbl:
            item.aff_index = bool(True)
            item.save()

        response = self.client.get(reverse('login'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        check_favoris = self.client.get('/purbeurre/favoris/')
        liste_favoris = check_favoris.context['trouve']

        x = 0
        for favoris in liste_favoris:
            if favoris['index']:
                x += 1

        self.assertEqual(x, 3)

    def test_search(self):
        ''' Permet de tester la recherche
        Lets test research '''
        terme_search = "nutella"
        response = self.client.post(
            '/purbeurre/resultat/' + terme_search + '/', {'search': terme_search})

        if terme_search == "":
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, '/purbeurre/')
        else:
            self.assertEqual(response.status_code, 200)
            if response.context['cherche']['error']:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertNotEqual(len(response.context['trouve']), 0)

    def test_noreponse(self):
        '''permet de test lorsqu'une recherche n'est pas trouvée
        '''
        terme_search = "trucmachin"
        response = self.client.post(
            '/purbeurre/resultat/' + terme_search + '/', {'search': terme_search})

        self.assertEqual(response.status_code, 200)
        if response.context['cherche']['error']:
            self.assertEqual(response.status_code, 200)

    def test_noreponse_goodcat(self):
        '''permet de test lorsqu'une recherche se refère a une catégorie
        '''
        terme_search = "gateau"
        response = self.client.post(
            '/purbeurre/resultat/' + terme_search + '/', {'search': terme_search})

        if terme_search == "":
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, '/purbeurre/')
        else:
            self.assertEqual(response.status_code, 200)
            if response.context['cherche']['error']:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertNotEqual(len(response.context['trouve']), 0)

    def test_index(self):
        ''' test l'index et de l'affichage des favoris
        test index and display favorites '''
        self.client.login(username="testuser1", password='testtest')
        response = self.client.get(reverse('login'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/purbeurre/')
        self.assertNotEqual(len(response.context['trouve']), 0)

    def test_nutrilien(self):
        """ Test unitaire lien nutriscore
        """
        self.assertEqual(lien_nutriscore(12), "assets/img/nutriscore-D.png")
        self.assertEqual(lien_nutriscore(-2), "assets/img/nutriscore-A.png")
        self.assertEqual(lien_nutriscore(20), "assets/img/nutriscore-E.png")

    def test_multi_answer(self):
        ''' Test réponse multiple
        '''
        self.client.login(username="testuser1", password='testtest')
        response = self.client.get(reverse('login'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')

        user_current = response.context['user']
        id_produit = 1

        self.assertTrue(ClassSearch.select_search(id_produit, user_current))

