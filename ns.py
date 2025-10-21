import subprocess
import re

def run_nslookup(domain, record_type):
    """Menjalankan perintah nslookup dan mengembalikan hasilnya."""
    try:
        result = subprocess.run(
            ["nslookup", "-type=" + record_type, domain],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"Error saat menjalankan nslookup: {e}"

def analyze_domain(domain):
    print("=" * 60)
    print(f"🔍 DOMAIN DETECTIVE – Analisis untuk: {domain}")
    print("=" * 60)

    # --- A Record ---
    print("\n🌐 [A Record – IP Address]")
    a_output = run_nslookup(domain, "A")
    a_matches = re.findall(r"Address:\s+([\d\.]+)", a_output)
    if a_matches:
        for ip in a_matches:
            print(f"  ✅ IP: {ip}")
        print(f"  📊 Total IP ditemukan: {len(a_matches)}")
    else:
        print("  ❌ Tidak ditemukan A record.")

    # --- MX Record ---
    print("\n📬 [MX Record – Mail Server]")
    mx_output = run_nslookup(domain, "MX")
    mx_matches = re.findall(r"mail exchanger = ([\w\.\-]+)", mx_output)
    if mx_matches:
        for mx in mx_matches:
            print(f"  ✅ Mail Server: {mx}")
        print(f"  📊 Total MX ditemukan: {len(mx_matches)}")
    else:
        print("  ❌ Tidak ditemukan MX record.")

    # --- CNAME Record ---
    print("\n🔗 [CNAME Record – Alias]")
    cname_output = run_nslookup(domain, "CNAME")
    cname_match = re.search(r"canonical name = ([\w\.\-]+)", cname_output)
    if cname_match:
        print(f"  ✅ CNAME: {cname_match.group(1)}")
    else:
        print("  ❌ Tidak ditemukan CNAME record.")

    # --- Analisis Otomatis ---
    print("\n🧠 [Analisis Otomatis]")
    if len(a_matches) > 1:
        print("  💡 Domain memiliki beberapa IP — kemungkinan load balancing.")
    if len(mx_matches) == 0:
        print("  ⚠️ Tidak ada mail server — domain ini mungkin tidak digunakan untuk email.")
    if not cname_match:
        print("  🏠 Domain utama tanpa alias CNAME.")
    else:
        print("  🔁 Domain ini menggunakan alias CNAME.")
    
    print("\n✅ Analisis selesai.\n")

if __name__ == "__main__":
    domain = input("Masukkan nama domain (contoh: google.com): ")
    analyze_domain(domain)
