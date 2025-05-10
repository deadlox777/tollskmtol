#!/usr/bin/env python3
"""
OSINT Phone Investigator - Termux Edition
Fitur:
- Deteksi operator & lokasi nomor
- Pencarian di sosial media
- WhatsApp Auto-Spam Report (Adjustable)
"""

import os
import requests
import phonenumbers
from phonenumbers import carrier, geocoder
import time
from datetime import datetime

# Konfigurasi
MAX_REPORTS = 100  # Maksimal report yang diperbolehkan
DELAY = 2  # Delay antar report (detik)

# Warna untuk output
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
MAGENTA = "\033[1;35m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
RESET = "\033[0m"

def show_banner():
    print(f"""{RED}
   ___  _____  ___   _  _____ _____ 
  / _ \/  ___|/ _ \ | \| |_   _|_   _|
 / /_\ \ `--./ /_\ \| .` | | |   | |  
 |  _  |`--. \  _  || |\  | | |   | |  
 | | | /\__/ / | | || | \ |_| |_  | |  
 \_| |_\____/\_| |_/\_|  \_/\___/  \_/  

{YELLOW}       PHONE OSINT INVESTIGATOR
{MAGENTA}    WhatsApp Custom Spam Reporter
{CYAN}       Termux Edition v4.0{RESET}""")

def validate_number(number):
    try:
        parsed = phonenumbers.parse(number, None)
        return parsed if phonenumbers.is_valid_number(parsed) else None
    except:
        return None

def whatsapp_spam_report(number, count):
    print(f"\n{YELLOW}[!] MEMULAI SPAM REPORT WHATSAPP{RESET}")
    print(f"{CYAN}Jumlah report: {count}{RESET}")
    
    clean_number = number.replace('+', '').replace(' ', '')
    success = 0
    
    for i in range(1, count+1):
        try:
            # Gunakan session untuk maintain connection
            with requests.Session() as s:
                s.headers.update({
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
                })
                
                # URL report WhatsApp
                url = f"https://wa.me/{clean_number}?text=SPAM-REPORT-{i}"
                response = s.get(url, timeout=10)
                
                if response.status_code == 200:
                    print(f"{GREEN}[{i}] Report berhasil ({i}/{count}){RESET}")
                    success += 1
                else:
                    print(f"{RED}[{i}] Gagal (HTTP {response.status_code}){RESET}")
                
                time.sleep(DELAY)  # Delay untuk avoid blocking
                
        except Exception as e:
            print(f"{RED}[X] Error: {str(e)[:50]}...{RESET}")
    
    print(f"\n{YELLOW}=== HASIL ===")
    print(f"{GREEN}Berhasil: {success}/{count}{RESET}")
    print(f"{RED}Gagal: {count-success}/{count}{RESET}")
    return success

def main():
    os.system('clear')
    show_banner()
    
    # Input nomor
    number = input(f"\n{BLUE}Masukkan nomor (contoh: +6281234567890): {RESET}").strip()
    
    if not (parsed := validate_number(number)):
        print(f"{RED}[!] Nomor tidak valid{RESET}")
        return
    
    # Info dasar
    print(f"\n{YELLOW}=== INFORMASI NOMOR ===")
    print(f"{GREEN}Nomor:{RESET} {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
    print(f"{GREEN}Operator:{RESET} {carrier.name_for_number(parsed, 'id') or 'Tidak diketahui'}")
    print(f"{GREEN}Lokasi:{RESET} {geocoder.country_name_for_number(parsed, 'id') or 'Tidak diketahui'}")
    
    # Input jumlah report
    try:
        count = int(input(f"\n{YELLOW}Masukkan jumlah report (1-{MAX_REPORTS}): {RESET}"))
        count = max(1, min(count, MAX_REPORTS))  # Clamping value
    except:
        print(f"{RED}Input tidak valid, menggunakan default 5 report{RESET}")
        count = 5
    
    # Konfirmasi
    confirm = input(f"\n{RED}Anda yakin mau kirim {count} report ke {number}? (y/n): {RESET}")
    if confirm.lower() != 'y':
        print(f"{YELLOW}Dibatalkan{RESET}")
        return
    
    # Eksekusi
    whatsapp_spam_report(number, count)

if __name__ == "__main__":
    main()