"""curve URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from simple_card.views import home, transactions
from simple_card.api_views import save_card, load, create_card, authorise, reverse, refund, capture

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^transactions/', transactions),
    url(r'^api/save_card/', save_card),
    url(r'^api/load/', load),
    url(r'^api/create_card/', create_card),
    url(r'^api/authorise/', authorise),
    url(r'^api/reverse/', reverse),
    url(r'^api/capture/', capture),
    url(r'^api/refund/', refund),
    url(r'^$', home),
]