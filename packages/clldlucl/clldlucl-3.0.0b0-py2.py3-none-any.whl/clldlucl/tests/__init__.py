from unittest import TestCase

from pyramid.testing import Configurator


class Tests(TestCase):
    def test_includeme(self):
        from clldlucl import includeme

        includeme(Configurator(settings={'sqlalchemy.url': 'sqlite://'}))
