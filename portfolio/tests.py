from django.test import TestCase
from django.urls import reverse
from portfolio.models import *
from django.utils import timezone

class PortfolioTest(TestCase):

    # Model tests
    def create_project(self):
        return Project.objects.create(
            title="Test title",
            description="Test description",
            short_description="Short test description",
            technology="Technology",
            image="Image",
            live_url="www.test.com",
            source_url = "www.sourcetest.com",
        )
    def test_project_creation(self):
        project = self.create_project()
        self.assertTrue(isinstance(project, Project))
        self.assertEqual(project.__str__(), "Test title")

    def create_certification(self):
        return Certification.objects.create(
            issuer = "Test issuer",
            name = "Test name",
            short_description = "Short test description",
            description = "Test description",
            issue_date = timezone.now(),
            technology = "Test technology",
            workload = 300,
            image = "Image",
            url = "www.test.com",
        )
    def test_certification_creation(self):
        certification = self.create_certification()
        self.assertTrue(isinstance(certification, Certification))
        self.assertEqual(certification.__str__(), "Test name")



    # View tests
    def test_portfolio_bio_view(self):
        url = reverse("portfolio_bio")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_portfolio_project_list_view(self):
        url = reverse("portfolio_project_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_portfolio_project_detail_view(self):
        self.create_project()
        url = reverse("portfolio_project_detail", kwargs={'pk': 1})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_portfolio_certification_list_view(self):
        certification = self.create_certification()
        url = reverse("portfolio_certification_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn((certification.name).encode(), resp.content)