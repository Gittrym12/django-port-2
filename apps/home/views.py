from django import template
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Formmodel, ProsedurM, GalleryKegiatanm, Visitor, DataPoint, JadwalBusM, menuKantinM, Announcement
from .forms import FormmodelForm, FormProsedur, GalleryKegiatanForm, DataPointF, JadwalBusF, menuKantinF, AnnouncementForm
from django.contrib.sessions.models import Session
from django.utils import timezone
from datetime import datetime, timedelta
import pandas as pd
import json
import os
import glob
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def get_date_range():
    # Mendapatkan tanggal hari ini
    today = datetime.now().date()
    # Menghitung tanggal kemarin
    yesterday = today - timedelta(days=1)
    # Mendapatkan tanggal awal bulan ini
    this_month_start = datetime(today.year, today.month, 1).date()
    # Mendapatkan tanggal awal tahun ini
    this_year_start = datetime(today.year, 1, 1).date()
    return today, yesterday, this_month_start, this_year_start

def index(request):
    # Memanggil fungsi untuk mendapatkan rentang tanggal
    today, yesterday, this_month_start, this_year_start = get_date_range()

    # Menghitung jumlah pengunjung hari ini
    today_count = Visitor.objects.filter(timestamp__date=today).count()

    # Menghitung jumlah pengunjung kemarin
    yesterday_count = Visitor.objects.filter(timestamp__date=yesterday).count()

    # Menghitung jumlah pengunjung bulan ini
    this_month_count = Visitor.objects.filter(timestamp__date__gte=this_month_start).count()

    # Menghitung jumlah pengunjung tahun ini
    this_year_count = Visitor.objects.filter(timestamp__date__gte=this_year_start).count()

    # Menghitung jumlah total pengunjung
    total_hits_count = Visitor.objects.all().count()

    # Menghitung jumlah pengguna online saat ini
    online_users = Session.objects.filter(expire_date__gte=timezone.now()).count()

    # Membuat konteks (context) untuk template
    context = {
        "segment": "index",
        'today_count': today_count,
        'yesterday_count': yesterday_count,
        'this_month_count': this_month_count,
        'this_year_count': this_year_count,
        'total_hits_count': total_hits_count,
        'online_users': online_users,
    }
    
    # Render template "home/index.html" dengan konteks yang telah dibuat
    return render(request, "home/index.html", context)



# @login_required(login_url="/login/")
def pages(request):
    context = {}  # Membuat kamus kosong untuk menyimpan data konteks.

    try:
        load_template = request.path.split("/")[-1]  # Mendapatkan bagian terakhir dari URL yang diminta.

        if load_template == "admin":
            # Jika bagian terakhir dari URL adalah "admin", alihkan pengguna ke halaman admin.
            return HttpResponseRedirect(reverse("admin:index"))

        context["segment"] = load_template  # Simpan bagian terakhir dari URL dalam konteks dengan kunci "segment".

        # Muat template yang sesuai berdasarkan bagian terakhir dari URL.
        html_template = loader.get_template("home/" + load_template)

        # Kembalikan hasil rendering template dengan menggunakan konteks yang telah disiapkan.
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        # Tangani jika template yang diminta tidak ditemukan. Kembalikan halaman 404.
        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        # Tangani kesalahan lain yang tidak terduga. Kembalikan halaman 500.
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))



##################################################### FORM METHODS #####################################################
# Fungsi untuk menampilkan daftar formulir
def form_list(request):
    forms = Formmodel.objects.all()
    return render(request, "home/form_list.html", {"forms": forms})

# Fungsi untuk menampilkan daftar formulir dalam area admin
def form_list_admin(request):
    forms = Formmodel.objects.all()
    return render(request, "home/admin/form_list.html", {"forms": forms})

# Fungsi untuk membuat formulir baru atau menampilkan formulir kosong
def form_create(request):
    if request.method == "POST":
        form = FormmodelForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()  # Menyimpan formulir untuk mendapatkan instance dengan file yang diunggah
            # Lakukan operasi tambahan jika diperlukan
            return redirect("form_list")  # Redirect ke URL 'form_list' menggunakan pola URL yang dinamai
    else:
        form = FormmodelForm()
    return render(request, "home/admin/form_create.html", {"form": form})

# Fungsi untuk mengunduh file yang terkait dengan formulir
def download_file(request, form_id):
    form_instance = Formmodel.objects.get(id=form_id)
    file_path = form_instance.file_upload.path
    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = "attachment; filename=" + form_instance.file_upload.name
        return response

# Fungsi untuk mengupdate formulir yang ada
def form_update(request, pk):
    form = Formmodel.objects.get(pk=pk)
    if request.method == "POST":
        form = FormmodelForm(request.POST, request.FILES, instance=form)
        if form.is_valid():
            form.save()
            return redirect("form_list")
    else:
        form = FormmodelForm(instance=form)
    return render(request, "home/admin/form_update.html", {"form": form})

# Fungsi untuk menghapus formulir yang ada
def form_delete(request, pk):
    form = Formmodel.objects.get(pk=pk)
    if request.method == "POST":
        form.delete()
        return redirect("form_list")
    return render(request, "home/admin/form_delete.html", {"form": form})

##################################################### END FORM METHODS #####################################################



##################################################### PROSEDUR METHODS #####################################################
# @login_required(login_url="/login/")
# Menampilkan daftar prosedur
def form_prosedur(request):
    forms = ProsedurM.objects.all()
    return render(request, "home/form_list_prosedur.html", {"forms": forms})

# Menampilkan daftar prosedur dalam area admin
def form_prosedur_admin(request):
    forms = ProsedurM.objects.all()
    return render(request, "home/admin/form_list_prosedur.html", {"forms": forms})

# Mengunduh file terkait dengan prosedur
def download_file_prosedur(request, form_id):
    form_instance = ProsedurM.objects.get(id=form_id)
    file_path = form_instance.file_upload_prosedur.path
    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = "attachment; filename=" + form_instance.file_upload_prosedur.name
        return response

# Membuat prosedur baru atau menampilkan formulir kosong untuk prosedur
def form_create_prosedur(request):
    if request.method == "POST":
        form = FormProsedur(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()  # Menyimpan formulir untuk mendapatkan instance dengan file yang diunggah
            # Lakukan operasi tambahan jika diperlukan
            return redirect("form_list_prosedur")  # Redirect ke URL 'form_list_prosedur' menggunakan pola URL yang dinamai
    else:
        form = FormProsedur()
    return render(request, "home/admin/form_create_prosedur.html", {"form": form})

# Mengupdate prosedur yang ada
def form_update_prosedur(request, pk):
    form = ProsedurM.objects.get(pk=pk)
    if request.method == "POST":
        form = FormProsedur(request.POST, request.FILES, instance=form)
        if form.is_valid():
            form.save()
            return redirect("form_list_prosedur")
    else:
        form = FormProsedur(instance=form)
    return render(request, "home/admin/form_update_prosedur.html", {"form": form})

# Menghapus prosedur yang ada
def form_delete_prosedur(request, pk):
    form = ProsedurM.objects.get(pk=pk)
    if request.method == "POST":
        form.delete()
        return redirect("form_list_prosedur")
    return render(request, "home/admin/form_delete_prosedur.html", {"form": form})

##################################################### END PROSEDUR METHODS #####################################################


##################################################### DATA ULANG TAHUN #####################################################
def dataUlangTahun(request):
    # Path ke file CSV yang berisi data ulang tahun karyawan
    csv_file_path = 'core/media/YPMI-Employee.csv'

    # Membaca data dari file CSV menggunakan pandas
    df = pd.read_csv(csv_file_path, delimiter=';')

    # Mendapatkan tanggal hari ini dalam format 'mm/dd'
    today_date = datetime.now().strftime('%m/%d')

    # Mengambil data yang cocok dengan tanggal ulang tahun hari ini
    filtered_data = df[df['Date'] == today_date]

    # Mengonversi data yang sesuai menjadi bentuk yang lebih mudah digunakan dalam template
    data = [{'NIK': row['NIK'], 'Name': row['NAME'], 'Section': row['SECTION'], 'Occupation': row['OCCUPATION']} for _, row in filtered_data.iterrows()]

    # Merender template 'dataUlangTahun.html' dengan data yang telah disiapkan
    return render(request, 'home/informasi/dataUlangTahuncopy.html', {'data': data})

##################################################### END DATA UALNG TAHUN #####################################################


##################################################### MENU KANTIN #####################################################
def upload_file(request):
    if request.method == 'POST':
        form = menuKantinF(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menuKantin')
    else:
        form = menuKantinF()
    return render(request, 'home/admin/create_menukantin.html', {'form': form})

def menu_list(request):
    menu_items = menuKantinM.objects.all()
    return render(request, 'home/admin/menu_list.html', {"menu_items": menu_items})

from django.shortcuts import render
import pandas as pd
from datetime import datetime, timedelta

def get_most_recent_csv_file():
    # Implement your logic to get the most recent CSV file path
    pass

def menuKantin(request):
    # Get the path to the most recently uploaded CSV file in the 'core/media' directory
    csv_file_path = get_most_recent_csv_file()

    if csv_file_path:
        # Read the CSV file
        df = pd.read_csv(csv_file_path, delimiter=';')

        # Convert the 'Date' column to a datetime object with the correct format
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

        # Get today's date and format it as 'dd/mm/yy' to filter the data
        today_date = datetime.now().strftime('%d/%m/%y')

        # Get tomorrow's date and format it as 'dd/mm/yy' to filter the data
        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%y')

        # Filter the data based on today's date
        today_data = df[df['Date'].dt.strftime('%d/%m/%y') == today_date]

        # Filter the data based on tomorrow's date
        tomorrow_data = df[df['Date'].dt.strftime('%d/%m/%y') == tomorrow_date]

        # Apply linebreaksbr filter to each field in today's data
        today_data_list = []
        for _, row in today_data.iterrows():
            today_data_list.append({
                'Date': row['Date'].strftime('%d/%m/%Y'),
                'Pilihan': row['PILIHAN'].replace(',', '<br>'),
                'Breakfast': row['BREAKFAST'].replace(',', '<br>'),
                'Shift3': row['SHIFT 3'].replace(',', '<br>'),
                'Shift1': row['SHIFT 1'].replace(',', '<br>'),
                'Shift2': row['SHIFT 2'].replace(',', '<br>')
            })

        # Apply linebreaksbr filter to each field in tomorrow's data
        tomorrow_data_list = []
        for _, row in tomorrow_data.iterrows():
            tomorrow_data_list.append({
                'Date': row['Date'].strftime('%d/%m/%Y'),
                'Pilihan': row['PILIHAN'].replace(',', '<br>'),
                'Breakfast': row['BREAKFAST'].replace(',', '<br>'),
                'Shift3': row['SHIFT 3'].replace(',', '<br>'),
                'Shift1': row['SHIFT 1'].replace(',', '<br>'),
                'Shift2': row['SHIFT 2'].replace(',', '<br>')
            })

        return render(request, 'home/informasi/menuKantin.html', {'today_data': today_data_list, 'tomorrow_data': tomorrow_data_list})
    else:
        # Handle the case where no CSV file is found
        return render(request, 'no_data.html')



def get_most_recent_csv_file():
    # Get a list of CSV files in the 'core/media' directory and subdirectories
    csv_files = glob.glob('core/media/**/*.csv', recursive=True)
    
    # Sort the list of files by modification time (most recent first)
    csv_files.sort(key=os.path.getmtime, reverse=True)

    # Check if any CSV files were found
    if csv_files:
        # Return the path to the most recently modified CSV file
        return csv_files[0]
    else:
        return None
    
def delete_file(request, file_id):
    try:
        # Retrieve the uploaded file by its ID
        uploaded_file = menuKantinM.objects.get(id=file_id)
        file_path = uploaded_file.file.path

        # Delete the file from the file system
        if os.path.exists(file_path):
            os.remove(file_path)

        # Delete the file from the database
        uploaded_file.delete()

        return redirect('menu_list')  # Redirect to the menu list page after successful deletion
    except menuKantinM.DoesNotExist:
        return redirect('error')  # Handle the case where the file doesn't exist
    
def delete_menu(request, pk):
    menu_items = get_object_or_404(menuKantinM, pk=pk)
    if request.method == 'POST':
        menu_items.delete()
        return redirect('menu_list')  # Redirect to the admin list view
    return render(request, 'home/admin/kegiatan_delete.html', {'menu_items': menu_items})




''''
def menuKantin(request):
    csv_file_path = 'core/media/kantin.csv'
    df = pd.read_csv(csv_file_path, delimiter=';')

    # Convert the 'Date' column to a datetime object with the correct format
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

    # Get today's date and format it as 'dd/mm/yy' to filter the data
    today_date = datetime.now().strftime('%d/%m/%y')

    # Filter the data based on today's date
    filtered_data = df[df['Date'].dt.strftime('%d/%m/%y') == today_date]

    # Create a list of dictionaries containing the data
    data = [{'Date': row['Date'].strftime('%d/%m/%Y'),
             'Pilihan': row['PILIHAN'],
             'Breakfast': row['BREAKFAST'],
             'Shift3': row['SHIFT 3'],
             'Shift1': row['SHIFT 1'],
             'Shift2': row['SHIFT 2']} for _, row in filtered_data.iterrows()]

    return render(request, 'home/informasi/menuKantin.html', {'data': data})'''
##################################################### END MENU KANTIN #####################################################




##################################################### KEGIATAN METHODS #####################################################
def gallery_list(request):
    gallery_items = GalleryKegiatanm.objects.all()
    return render(request, 'home/public_gallery_list.html', {"gallery_items": gallery_items})

# Create view
def create_gallery_kegiatan(request):
    if request.method == 'POST':
        form = GalleryKegiatanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery_list')
    else:
        form = GalleryKegiatanForm()
    return render(request, 'home/admin/kegiatan_create.html', {'form': form})

# Read (List) view for admin
def gallery_list_admin(request):
    gallery_items = GalleryKegiatanm.objects.all()
    return render(request, 'home/admin/kegiatanYpmi.html', {"gallery_items": gallery_items})

# Update view
def update_gallery_kegiatan(request, pk):
    gallery_item = get_object_or_404(GalleryKegiatanm, pk=pk)
    if request.method == 'POST':
        form = GalleryKegiatanForm(request.POST, request.FILES, instance=gallery_item)
        if form.is_valid():
            form.save()
            return redirect('gallery_list_admin')  # Redirect to the admin list view
    else:
        form = GalleryKegiatanForm(instance=gallery_item)
    return render(request, 'home/admin/kegiatan_update.html', {'form': form, 'gallery_item': gallery_item})

# Delete view
def delete_gallery_kegiatan(request, pk):
    gallery_item = get_object_or_404(GalleryKegiatanm, pk=pk)
    if request.method == 'POST':
        gallery_item.delete()
        return redirect('gallery_list_admin')  # Redirect to the admin list view
    return render(request, 'home/admin/kegiatan_delete.html', {'gallery_item': gallery_item})
##################################################### END KEGIATAN METHODS #####################################################


##################################################### CHART METHODS #####################################################
def chart_data_admin(request):
    data_points = DataPoint.objects.all()
    
    # Convert data to a format suitable for Chart.js (e.g., JSON)
    chart_data = {
        'labels': [str(dp.bulan) for dp in data_points],
        'indexs': [dp.indexs for dp in data_points],
    }
    
    return render(request, 'home/admin/indexsKehadiran.html', {'chart_data': json.dumps(chart_data, default=str), 'data_points': data_points})


def chart_data(request):
    data_points = DataPoint.objects.all()
    # Convert data to a format suitable for Chart.js (e.g., JSON)
    data = {
        'labels': [str(dp.bulan) for dp in data_points],
        'indexs': [dp.indexs for dp in data_points],
    }
    return render(request, 'home/informasi/indexsKehadiran.html', {'data': json.dumps(data)})

def create_attendance(request):
    if request.method == 'POST':
        form = DataPointF(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chart_data')  # Redirect to the list view after creating
    else:
        form = DataPointF()
    
    return render(request, 'home/admin/indexsKehadiran_create.html', {'form': form})

def update_attendance(request, pk):
    data_point = get_object_or_404(DataPoint, pk=pk)
    
    if request.method == 'POST':
        form = DataPointF(request.POST, instance=data_point)
        if form.is_valid():
            form.save()
            return redirect('chart_data')  # Redirect back to the list view after updating
    else:
        form = DataPointF(instance=data_point)
    return render(request, 'home/admin/indexsKehadiran_update.html', {'form': form, 'chart_data': data_point})

def delete_attendance(request, pk):
    # Get the DataPoint object to delete or raise a 404 error if it doesn't exist
    chart_data = get_object_or_404(DataPoint, pk=pk)

    if request.method == 'POST':
        # If it's a POST request, delete the object
        chart_data.delete()
        return redirect('chart_data')  # Redirect to the list view after deleting
    else:
        return render(request, 'home/admin/indexsKehadiran_delete.html', {'chart_data': chart_data})
##################################################### END CHART METHHODS #####################################################




##################################################### JADWAL BUS   #####################################################
def jadwal_bus(request):
    forms = JadwalBusM.objects.all()
    return render(request, "home/informasi/jadwalBusJemputan.html", {"forms": forms})


def jadwal_bus_admin(request):
    forms = JadwalBusM.objects.all()
    return render(request, "home/admin/jadwalBus.html", {"forms": forms})

def jadwal_bus_create(request):
    if request.method == "POST":
        form = JadwalBusF(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            # Perform any additional operations if needed
            return redirect("jadwal_bus_list")  # Use the correct URL name
    else:
        form = JadwalBusF()
    return render(request, "home/admin/jadwalBus_create.html", {"form": form})

def jadwal_bus_update(request, pk):
    form = get_object_or_404(JadwalBusM, pk=pk)
    if request.method == "POST":
        form = JadwalBusF(request.POST, request.FILES, instance=form)
        if form.is_valid():
            form.save()
            return redirect("jadwal_bus_list")  # Use the correct URL name
    return render(request, "home/admin/jadwalBus_update.html", {"form": form})

def jadwal_bus_delete(request, pk):
    form = get_object_or_404(JadwalBusM, pk=pk)
    if request.method == "POST":
        form.delete()
        return redirect("jadwal_bus_list")  # Use the correct URL name
    return render(request, "home/admin/jadwalBus_delete.html", {"form": form})

##################################################### END JADWAL BUS #####################################################



##################################################### PENGUMUMAN METHODS #####################################################
# @login_required(login_url="/login/")
from django import forms

class AnnouncementFilterForm(forms.Form):
    q = forms.CharField(required=False)
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'home/informasi/pengumumanList.html'
    context_object_name = 'pengumumans'
    form_class = AnnouncementFilterForm

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            pengumumans = Announcement.objects.all()

            query = form.cleaned_data.get('q')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            if query:
                pengumumans = pengumumans.filter(Q(nama_pengumuman__icontains=query))

            if start_date:
                pengumumans = pengumumans.filter(tanggal_upload__gte=start_date)

            if end_date:
                pengumumans = pengumumans.filter(tanggal_upload__lte=end_date)

            return pengumumans
        else:
            # Print or log form errors
            print(form.errors)
            return Announcement.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(self.request.GET)
        return context


class AnnouncementCreateView(CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'home/admin/pengumuman_create.html'
    success_url = reverse_lazy('announcement_list')

    def form_valid(self, form):
        # Customize form validation behavior here
        form.instance.catThn = form.cleaned_data['catThn']
        return super().form_valid(form)

class AnnouncementUpdateView(UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'home/admin/pengumuman_update.html'
    success_url = reverse_lazy('announcement_list')

class AnnouncementDeleteView(DeleteView):
    model = Announcement
    template_name = 'home/admin/pengumuman_delete.html'
    success_url = reverse_lazy('announcement_list')

def download_file_pengumuman(request, announcement_id):
    announcement_instance = get_object_or_404(Announcement, id=announcement_id)
    file_path = announcement_instance.file_pengumuman.path

    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = "attachment; filename=" + announcement_instance.file_pengumuman.name
        return response

'''
def pengumuman_list(request):
    query = request.GET.get("q")
    filter_by = request.GET.get("filter_by")
    date_filter = request.GET.get("date_filter")

    # Initial queryset
    pengumumans = PengumumanYpmiM.objects.all()

    # Apply search filter
    if query:
        pengumumans = pengumumans.filter(Q(no_pengumuman__icontains=query) | Q(nama_pengumuman__icontains=query))

    # Apply date filter
    if date_filter:
        pengumumans = pengumumans.filter(tanggal_upload=date_filter)

    return render(request, "home/informasi/pengumumanList.html", {"pengumumans": pengumumans, "query": query, "filter_by": filter_by, "date_filter": date_filter})

def pengumuman_admin(request):
    pengumumans = PengumumanYpmiM.objects.all()
    return render(request, "home/admin/pengumuman_admin.html", {"pengumumans": pengumumans})

def download_file_pengumuman(request, pengumuman_id):
    pengumuman_instance = PengumumanYpmiM.objects.get(id=pengumuman_id)
    file_path = pengumuman_instance.file_pengumuman.path
    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = "attachment; filename=" + pengumuman_instance.file_pengumuman.name
        return response


def pengumuman_create(request):
    if request.method == "POST":
        form = PengumumanYpmiF(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return redirect("pengumuman_list")
    else:
        form = PengumumanYpmiF()
    return render(request, "home/admin/pengumuman_create.html", {"form": form})


def pengumuman_update(request, pk):
    pengumuman = PengumumanYpmiM.objects.get(pk=pk)
    if request.method == "POST":
        form = PengumumanYpmiF(request.POST, request.FILES, instance=pengumuman)
        if form.is_valid():
            form.save()
            return redirect("pengumuman_list")
    else:
        form = PengumumanYpmiF(instance=pengumuman)
    return render(request, "home/admin/pengumuman_update.html", {"form": form})



def pengumuman_delete(request, pk):
    pengumuman = get_object_or_404(PengumumanYpmiM, pk=pk)

    if request.method == "POST":
        # Delete the file associated with the pengumuman
        file_path = pengumuman.file_pengumuman.path

        if os.path.exists(file_path):
            os.remove(file_path)

        # Delete the pengumuman from the database
        pengumuman.delete()

        return redirect("pengumuman_list")

    return render(request, "home/admin/pengumuman_delete.html", {"pengumuman": pengumuman})
'''


##################################################### END PENGUMUMAN METHODS #####################################################

def aturanViews(request):
    return render(request, "home/aturan.html")


def data_tables(request):
    return render(request, "home/tables.html")

def icon_tables(request):
    return render(request, "home/icon.html")

def timKami(request):
    return render(request, "home/timKami.html")

def kontak(request):
    return render(request, "home/kontakv.html")

def visiYpmi(request):
    return render(request, "home/visiypmi.html")

def pengumumanHRD(request):
    return render(request, "home/informasi/pengumumanHRD.html")

def jadwalTraining(request):
    return render(request, "home/informasi/jadwalTraining.html")

def jadwalBusJemputan(request):
    return render(request, "home/informasi/jadwalBusJemputan.html")



def satgasPPKS(request):
    return render(request, "home/informasi/satgasPPKS.html")

def pkb(request):
    return render(request, "home/informasi/pkb.html")



def dataKehadiranTerbaik(request):
    return render(request, "home/informasi/dataKehadiranTerbaik.html")

def strukturOrganisasi(request):
    return render(request, "home/informasi/struktur-organisasi.html")
















