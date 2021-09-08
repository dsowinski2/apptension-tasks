import pytest
import pytest_factoryboy

from users.tests import factories as user_factories
pytest_factoryboy.register(user_factories.UserFactory)