import sqlite3
import urllib.request
import urllib.error
from datetime import datetime

# Create database and table if not exists
def init_db():
    conn = sqlite3.connect('website_checker.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS websites
                 (id INTEGER PRIMARY KEY, url TEXT, status TEXT, safety TEXT, last_checked TEXT)''')
    try:
        c.execute("ALTER TABLE websites ADD COLUMN reason TEXT DEFAULT 'Not checked'")
    except sqlite3.OperationalError:
        pass  # Column already exists
    conn.commit()
    conn.close()

# CREATE: Add a website
def create_website(url):
    conn = sqlite3.connect('website_checker.db')
    c = conn.cursor()
    c.execute("INSERT INTO websites (url, status, safety, last_checked, reason) VALUES (?, ?, ?, ?, ?)",
              (url, 'Not checked', 'Not checked', 'Never', 'Not checked'))
    conn.commit()
    conn.close()
    print(f"Created: {url}")

# READ: Get all websites
def read_websites():
    conn = sqlite3.connect('website_checker.db')
    c = conn.cursor()
    c.execute("SELECT id, url, status, safety, last_checked, reason FROM websites")
    rows = c.fetchall()
    conn.close()
    return rows

# READ: Get a specific website by id
def read_website(wid):
    conn = sqlite3.connect('website_checker.db')
    c = conn.cursor()
    c.execute("SELECT id, url, status, safety, last_checked, reason FROM websites WHERE id = ?", (wid,))
    row = c.fetchone()
    conn.close()
    return row

# UPDATE: Update status
def update_status(wid, status):
    conn = sqlite3.connect('website_checker.db')
    c = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("UPDATE websites SET status = ?, last_checked = ? WHERE id = ?",
              (status, now, wid))
    conn.commit()
    conn.close()
    print(f"Updated status for ID {wid}")

# UPDATE: Update safety
def update_safety(wid, safety, reason=None):
    conn = sqlite3.connect('website_checker.db')
    c = conn.cursor()
    if reason is None:
        c.execute("UPDATE websites SET safety = ? WHERE id = ?", (safety, wid))
    else:
        c.execute("UPDATE websites SET safety = ?, reason = ? WHERE id = ?", (safety, reason, wid))
    conn.commit()
    conn.close()
    print(f"Updated safety for ID {wid}")

# UPDATE: Update reason
def update_reason(wid, reason):
    conn = sqlite3.connect('website_checker.db')
    c = conn.cursor()
    c.execute("UPDATE websites SET reason = ? WHERE id = ?", (reason, wid))
    conn.commit()
    conn.close()
    print(f"Updated reason for ID {wid}")

# DELETE: Delete a website
def delete_website(wid):
    conn = sqlite3.connect('website_checker.db')
    c = conn.cursor()
    c.execute("DELETE FROM websites WHERE id = ?", (wid,))
    conn.commit()
    conn.close()
    print(f"Deleted website with ID {wid}")

# Check if website is up
def check_status(url):
    try:
        response = urllib.request.urlopen(url, timeout=5)
        return 'Up' if response.status == 200 else f'Down ({response.status})'
    except:
        return 'Down (Error)'

# Check if website is safe (basic check: HTTPS)
def check_safety(url):
    if url.startswith('https://'):
        return 'Safe', 'Uses HTTPS'
    else:
        return 'Unsafe', 'Does not use HTTPS'

# Check all websites
def check_all():
    websites = read_websites()
    for wid, url, _, _, _, _ in websites:
        status = check_status(url)
        safety, reason = check_safety(url)
        update_status(wid, status)
        update_safety(wid, safety, reason)
    print("Checked all websites")

# Display all websites
def display_all():
    websites = read_websites()
    for row in websites:
        print(f"ID: {row[0]}, URL: {row[1]}, Status: {row[2]}, Safety: {row[3]}, Reason: {row[5]}, Last Checked: {row[4]}")

# Initialize database
init_db()

if __name__ == "__main__":
    while True:
        print("\nWebsite Checker Menu:")
        print("1. Add a website")
        print("2. View all websites")
        print("3. View a specific website")
        print("4. Update status")
        print("5. Update safety")
        print("6. Update reason")
        print("7. Delete a website")
        print("8. Check all websites")
        print("9. Exit")
        choice = input("Choose an option (1-9): ").strip()

        if choice == '1':
            url = input("Enter the website URL: ").strip()
            if url:
                create_website(url)
            else:
                print("URL cannot be empty.")
        elif choice == '2':
            display_all()
        elif choice == '3':
            try:
                wid = int(input("Enter the website ID: ").strip())
                website = read_website(wid)
                if website:
                    print(f"ID: {website[0]}, URL: {website[1]}, Status: {website[2]}, Safety: {website[3]}, Reason: {website[5]}, Last Checked: {website[4]}")
                else:
                    print("Website not found.")
            except ValueError:
                print("Invalid ID.")
        elif choice == '4':
            try:
                wid = int(input("Enter the website ID: ").strip())
                status = input("Enter new status: ").strip()
                if status:
                    update_status(wid, status)
                else:
                    print("Status cannot be empty.")
            except ValueError:
                print("Invalid ID.")
        elif choice == '5':
            try:
                wid = int(input("Enter the website ID: ").strip())
                safety = input("Enter new safety (Safe/Unsafe): ").strip()
                if safety in ['Safe', 'Unsafe']:
                    update_safety(wid, safety)
                else:
                    print("Safety must be 'Safe' or 'Unsafe'.")
            except ValueError:
                print("Invalid ID.")
        elif choice == '6':
            try:
                wid = int(input("Enter the website ID: ").strip())
                reason = input("Enter new reason: ").strip()
                if reason:
                    update_reason(wid, reason)
                else:
                    print("Reason cannot be empty.")
            except ValueError:
                print("Invalid ID.")
        elif choice == '7':
            try:
                wid = int(input("Enter the website ID: ").strip())
                confirm = input(f"Are you sure you want to delete website ID {wid}? (y/n): ").strip().lower()
                if confirm == 'y':
                    delete_website(wid)
                else:
                    print("Deletion cancelled.")
            except ValueError:
                print("Invalid ID.")
        elif choice == '8':
            check_all()
        elif choice == '9':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select 1-9.")
