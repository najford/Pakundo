import os
import time

def ask_storage_permission():
    while True:
        choice = input("\nYou need to grant storage permission for Termux in the Android settings.\nPress 'y' to open settings, 'n' to exit: ").strip().lower()
        if choice == 'y':
            os.system("termux-setup-storage")
            time.sleep(2)
            if os.path.isdir("/storage/emulated/0"):
                print("✅ Storage permission granted.\n")
                return True
            else:
                print("❌ Still no storage access.\n")
        elif choice == 'n':
            print("👋 Exiting tool.")
            exit()
        else:
            print("❗ Invalid choice. Please enter 'y' or 'n'.")

# Usage
if not os.path.isdir("/storage/emulated/0"):
    ask_storage_permission()
