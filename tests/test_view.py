try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse
from fixtures import *  # NOQA

def test_base(app):
    url = reverse('index')
    response = app.get(url)
    assert response.status_code == 200
