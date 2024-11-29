from google.colab import auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.colab import files

auth.authenticate_user()
service = build('drive', 'v3')

def list_files_in_folder_recursive(folder_id):
    """Mendaftarkan semua file dalam folder dan subfolder secara rekursif, dengan pagination."""
    files = []
    folders = [folder_id]
    
    while folders:
        current_folder_id = folders.pop()
        page_token = None  # Untuk pagination
        while True:
            try:
                response = service.files().list(
                    q=f"'{current_folder_id}' in parents and trashed=false",
                    fields="nextPageToken, files(id, name, mimeType, createdTime, parents)", 
                    pageSize=1000,
                    pageToken=page_token
                ).execute()

                items_in_folder = response.get('files', [])
                
                for item in items_in_folder:
                    if item['mimeType'] == 'application/vnd.google-apps.folder':
                        folders.append(item['id'])
                    else:
                        files.append(item)
                
                page_token = response.get('nextPageToken')
                if not page_token:
                    break
            except HttpError as error:
                print(f"Terjadi kesalahan saat membaca folder {current_folder_id}: {error}")
                break

    return files

def find_duplicate_files(files):
    """Mengelompokkan file dengan nama yang sama sebagai duplikat."""
    duplicates = {}
    for file in files:
        name = file['name']
        if name not in duplicates:
            duplicates[name] = []
        duplicates[name].append(file)
    return {name: files for name, files in duplicates.items() if len(files) > 1}

def remove_file_from_folder(file_id, folder_id):
    """Mengeluarkan file dari folder."""
    try:
        service.files().update(fileId=file_id, removeParents=folder_id).execute()
    except HttpError as error:
        print(f"Gagal mengeluarkan file dengan ID {file_id}: {error}")

def write_output_to_file(output, filename="output.txt"):
    """Menulis hasil output ke file teks."""
    with open(filename, "w") as file:
        file.write(output)
    print(f"Hasil telah disimpan ke file '{filename}'.")

def prompt_for_download(output):
    """Meminta pengguna untuk memilih apakah ingin mengunduh hasil output."""
    while True:
        choice = input("Apakah Anda ingin mengunduh hasil output sebagai file teks? (y/n): ").strip().lower()
        if choice in ["y", "n"]:
            break  # Keluar dari loop jika input valid
    
    if choice == "y":
        filename = "output.txt"
        write_output_to_file(output, filename)
        files.download(filename)  # Mengunduh file ke perangkat pengguna
        print("File teks berhasil diunduh.")
    else:
        print("Tidak ada file yang dibuat.")

def process_duplicates(folder_id):
    """Memproses file duplikat di folder utama dan subfolder."""
    all_files = list_files_in_folder_recursive(folder_id)
    duplicate_files = find_duplicate_files(all_files)
    output = ""  
    
    if duplicate_files:
        output += "==========================\n"
        output += "File duplikat ditemukan dan akan dikeluarkan dari folder, menyisakan satu file (yang terlama):\n"
        output += "==========================\n"
        
        for name, files in duplicate_files.items():
            # Mengurutkan file berdasarkan waktu pembuatan (createdTime), terlama di urutan pertama
            files.sort(key=lambda f: f['createdTime'])
            oldest_file = files[0]
            
            output += f"{name} - {len(files)} file ditemukan:\n"
            for i, file in enumerate(files, start=1):
                output += f"  {i}. Tgl Upload: {file['createdTime']}\n"
            
            output += f"Program akan mempertahankan file 1.\n"
            output += "--------------------------\n"
            
            # Mengeluarkan semua file lainnya
            for file in files[1:]:
                remove_file_from_folder(file['id'], file['parents'][0])
        
        output += "==========================\n"
    else:
        output += "==========================\n"
        output += "Tidak ada file duplikat ditemukan.\n"
        output += "==========================\n"
    
    print(output)
    prompt_for_download(output)

def list_main_and_shortcut_folders_in_my_drive(exclude_folders):
    """Mendaftarkan semua folder utama dan pintasan di My Drive, kecuali folder yang dikecualikan."""
    try:
        results = service.files().list(
            q="(mimeType='application/vnd.google-apps.folder' or mimeType='application/vnd.google-apps.shortcut') "
              "and trashed=false and 'root' in parents",
            fields="files(id, name, mimeType, shortcutDetails)", pageSize=100).execute()
        
        folders = [
            folder for folder in results.get('files', [])
            if folder['name'] not in exclude_folders
        ]
        
        print("Folder utama (dan pintasan) di My Drive Anda:")
        for i, folder in enumerate(folders, start=1):
            print(f"{i}. {folder['name']}")
        return folders
    except HttpError as error:
        print(f'Terjadi kesalahan: {error}')
        return []

# Fungsi utama yang dibungkus dengan penanganan exception
def main_program():
    """Fungsi utama untuk menjalankan program."""
    exclude_folders = ["Colab Notebooks"]
    folders = list_main_and_shortcut_folders_in_my_drive(exclude_folders)
    folder_input = input("\nMasukkan nomor atau nama folder (pintasan) untuk memeriksa file duplikat: ")

    selected_folder = None

    selected_folder = next((f for f in folders if f['name'].lower() == folder_input.lower()), None)

    if not selected_folder and folder_input.isdigit():
        folder_index = int(folder_input) - 1
        if 0 <= folder_index < len(folders):
            selected_folder = folders[folder_index]

    if selected_folder:
        shortcut_target_id = selected_folder['shortcutDetails']['targetId'] if selected_folder['mimeType'] == 'application/vnd.google-apps.shortcut' else selected_folder['id']
        process_duplicates(shortcut_target_id)
    else:
        print("Folder tidak ditemukan. Pastikan nama atau nomor folder yang Anda masukkan benar.")

# Membungkus seluruh program dengan try-except
if __name__ == "__main__":
    try:
        main_program()
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna. Tidak ada error.")  # Pesan sederhana saat dihentikan
    except Exception as e:
        print(f"\nTerjadi error tak terduga: {e}")  # Pesan error untuk kesalahan yang tidak disengaja
