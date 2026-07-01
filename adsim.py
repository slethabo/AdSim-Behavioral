import argparse
import os
import subprocess
import sys
import webbrowser

# --- CONFIGURATION ---
TARGET_URL = "https://www.google.com"  # Benign payload destination
TASK_NAME = "AdSimBehavioralTask"       # Matches the README Telemetry section

def trigger_payload():
    """Simulates the adware behavior by opening a safe browser tab."""
    print("[*] Triggering benign adware browser event...")
    try:
        webbrowser.open(TARGET_URL)
        print("[+] Success: Browser tab opened safely.")
    except Exception as e:
        print(f"[-] Error triggering payload: {e}")

def install_persistence():
    """Simulates adware persistence using Windows Task Scheduler.
    Registers a repeating callback loop that triggers every 10 minutes.
    """
    print("[*] Installing benign 10-minute persistence mechanism...")
    
    if sys.platform == "win32":
        # Determine if we are running as a raw script or a compiled .exe
        target_path = os.path.abspath(sys.argv[0])
        if target_path.endswith('.py'):
            cmd = f'python "{target_path}" --run'
        else:
            cmd = f'"{target_path}" --run'
            
        # Command to create a scheduled task running every 10 minutes (/mo 10)
        # Forced (/f) to overwrite if it already exists during testing
        schtasks_cmd = f'schtasks /create /tn "{TASK_NAME}" /tr "{cmd}" /sc minute /mo 10 /f'
        
        try:
            result = subprocess.run(schtasks_cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[+] Success: Created Windows Scheduled Task '{TASK_NAME}'")
            else:
                print(f"[-] Failed to register task: {result.stderr.strip()}")
        except Exception as e:
            print(f"[-] Error executing schtasks utility: {e}")
    else:
        print("[-] Simulation Error: 10-minute scheduled tasks are platform-locked to Windows environments.")

def remove_persistence():
    """Completely de-registers the scheduled task, cleaning the host system."""
    print("[*] Initiating automated de-escalation/cleanup routine...")
    
    if sys.platform == "win32":
        schtasks_delete = f'schtasks /delete /tn "{TASK_NAME}" /f'
        try:
            result = subprocess.run(schtasks_delete, shell=True, capture_output=True, text=True)
            if result.returncode == 0 or "not found" in result.stderr.lower():
                print(f"[+] Success: Purged Windows Scheduled Task '{TASK_NAME}' from host system.")
            else:
                print(f"[-] Failed to drop task cleanly: {result.stderr.strip()}")
        except Exception as e:
            print(f"[-] Error removing task: {e}")
    else:
        print("[*] System is clean or non-Windows environment. No action required.")

# --- CORE CLI INTERFACE ---
def main():
    parser = argparse.ArgumentParser(
        description="AdSim-Behavioral: A Windows Adware & Persistence Simulator for Security Testing."
    )
    parser.add_argument("--setup", action="store_true", help="Install 10-min persistence and run the initial payload.")
    parser.add_argument("--run", action="store_true", help="Simulate a standalone adware execution event.")
    parser.add_argument("--cleanup", action="store_true", help="Completely purge simulation artifacts and tasks.")
    
    args = parser.parse_args()

    if args.setup:
        print("[+] Initializing AdSim Behavioral Framework...")
        install_persistence()
        trigger_payload()
    elif args.run:
        trigger_payload()
    elif args.cleanup:
        remove_persistence()
    else:
        # If clicked directly as an executable without flags, default to executing the payload
        trigger_payload()

if __name__ == "__main__":
    main()