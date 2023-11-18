from django.urls import path, re_path
from apps.home import views
from django.conf import settings
from django.conf.urls.static import static
from .views import AnnouncementListView, AnnouncementCreateView, AnnouncementUpdateView, AnnouncementDeleteView, AturanListView, AturanCreateView, AturanUpdateView, AturanDeleteView, AturanDownloadView


# Define URL patterns for your Django application

urlpatterns = [
    # Home page
    path("", views.index, name="home"),

    # Form related views
    path("home/form_list/", views.form_list, name="form_list"),
    path("home/form_list_admin/", views.form_list_admin, name="form_list_admin"),
    path("home/create/", views.form_create, name="form_create"),
    path("download/<int:form_id>/", views.download_file, name="download_file"),
    path("home/update/<int:pk>/", views.form_update, name="form_update"),
    path("home/delete/<int:pk>/", views.form_delete, name="form_delete"),

    # "Prosedur" related views
    path("home/list_prosedur/", views.form_prosedur, name="form_list_prosedur"),
    path("home/list_prosedur_admin/", views.form_prosedur_admin, name="form_list_prosedur_admin"),
    path("home/create_prosedur/", views.form_create_prosedur, name="form_create_prosedur"),
    path("download/prosedur<int:form_id>/", views.download_file_prosedur, name="download_file_prosedur"),
    path("home/update_prosedur/<int:pk>/", views.form_update_prosedur, name="form_update_prosedur"),
    path("home/delete_prosedur/<int:pk>/", views.form_delete_prosedur, name="form_delete_prosedur"),
    
    # Gallery related views
    path('home/gallery_list_admin/', views.gallery_list_admin, name='gallery_list_admin'),
    path("home/kegiatan/", views.gallery_list, name="gallery_list"),
    path("home/create_kegiatan/", views.create_gallery_kegiatan, name="create_gallery_kegiatan"),
    path("home/update_kegiatan/<int:pk>/", views.update_gallery_kegiatan, name="update_gallery_kegiatan"),
    path("home/delete_kegiatan/<int:pk>/", views.delete_gallery_kegiatan, name="delete_gallery_kegiatan"),

    # Kehadiran related views
    path('home/datakehadiran_create/', views.create_data_kehadiran, name='create_datakehadiran'),
    path('home/datakehadiran_read/', views.read_data_kehadiran, name='read_datakehadiran'),
    path('home/datakehadiran_update/<int:pk>/', views.update_data_kehadiran, name='update_datakehadiran'),
    path('home/datakehadiran_delete/<int:pk>/', views.delete_data_kehadiran, name='delete_datakehadiran'),

    # Jadwal Bus views
    path("home/jadwal-bus/", views.jadwal_bus, name="jadwal_bus_list"),
    path("home/jadwal-bus-admin/", views.jadwal_bus_admin, name="jadwal_bus_admin"),
    path("home/jadwal-bus/create/", views.jadwal_bus_create, name="jadwal_bus_create"),
    path("home/jadwal-bus/update/<int:pk>/", views.jadwal_bus_update, name="jadwal_bus_update"),
    path("home/jadwal-bus/delete/<int:pk>/", views.jadwal_bus_delete, name="jadwal_bus_delete"),

    # Menu Kantin views
    path("home/menu_list/", views.menu_list, name="menu_list"),
    path("home/menuKantin/", views.menuKantin, name="menuKantin"),
    path("home/create_menuKantin/", views.upload_file, name="create_menuKantin"),
    path("home/delete_menuKantin/<int:file_id>/", views.delete_file, name="delete_menuKantin"),
    path("home/delete_menu/<int:pk>/", views.delete_menu, name="delete_menu"),
 
    path('pengumuman/download/<int:pengumuman_id>/', views.download_file_pengumuman, name='download_file_pengumuman'),
    path('pengumuman/list/', AnnouncementListView.as_view(), name='announcement_list'),
    path('pengumuman/create/', AnnouncementCreateView.as_view(), name='announcement_create'),
    path('pengumuman/update/<int:pk>/', AnnouncementUpdateView.as_view(), name='announcement_update'),
    path('pengumuman/delete/<int:pk>/', AnnouncementDeleteView.as_view(), name='announcement_delete'),
    
    # aturan views
    path('home/aturan/', AturanListView.as_view(), name='aturan_list'),
    path('home/aturan/create/', AturanCreateView.as_view(), name='aturan_create'),
    path('home/aturan/<int:pk>/edit/', AturanUpdateView.as_view(), name='aturan_edit'),
    path('home/aturan/<int:pk>/delete/', AturanDeleteView.as_view(), name='aturan_delete'),
    path('aturan/<int:pk>/download/', AturanDownloadView.as_view(), name='aturan_download'),




    # Other views
    path("home/aturan/", views.aturanViews, name="aturan"),
    path("home/kontak/", views.kontak, name="kontak"),
    path("home/timKami/", views.timKami, name="timKami"),
    path("home/visiYpmi/", views.visiYpmi, name="visiYpmi"),
    path("home/pengumumanHRD/", views.pengumumanHRD, name="pengumumanHRD"),
    path("home/jadwalTraining/", views.jadwalTraining, name="jadwalTraining"),
    path("home/jadwalBusJemputan/", views.jadwalBusJemputan, name="jadwalBusJemputan"),
    path("home/satgasPPKS/", views.satgasPPKS, name="satgasPPKS"),
    path("home/pkb/", views.pkb, name="pkb"),
    path("home/dataUlangTahun/", views.dataUlangTahun, name="dataUlangTahun"),
    path("home/dataKehadiranTerbaik/", views.dataKehadiranTerbaik, name="dataKehadiranTerbaik"),
    path("home/struktur_organisasi/", views.strukturOrganisasi, name="struktur_organisasi"),

    # Matches any html file
    re_path(r"^.*\.*", views.pages, name="pages"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)