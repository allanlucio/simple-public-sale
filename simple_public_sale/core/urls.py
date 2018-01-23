"""simple_public_sale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path


from core.views import *

urlpatterns = [

    path('', list_all_events, name='list-all-events'),
    re_path('assistir/evento/(?P<group_id>.+)', watch_event, name='watch-event'),
    re_path('gerenciar/evento/(?P<evento_id>[0-9]+)', manage_event, name='manage-event'),
    re_path('gerenciar/arrematadores/(?P<evento_id>[0-9]+)', list_gift_finishers, name='event-finishers'),
    re_path('gerenciar/desfazer/movimento/(?P<movimento_id>.+)', undo_arrematador_lance, name='undo-movement-prenda'),
    re_path('gerenciar/arrematar/prenda/(?P<prenda_id>[0-9]+)/(?P<evento_id>[0-9]+)', arrematar_prenda, name='arrematar-prenda'),
    re_path('gerenciar/arrematar/prenda/desfazer/(?P<prenda_id>[0-9]+)/(?P<evento_id>[0-9]+)', undo_arrematar_prenda, name='desfaz-arrematar-prenda'),
    re_path('gerenciar/doar/prenda/(?P<prenda_id>[0-9]+)', donate_prenda,
            name='donate-prenda'),

]