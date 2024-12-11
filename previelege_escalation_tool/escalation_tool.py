import os
import psutil
import platform
import grp
import pwd
import subprocess
# import log
import sys

# Local Privilege Escalation Detection Tool
class PrivilegeEscalationDetectionTool:
    def __init__(self):
        self.os_name = platform.system()
        self.logs_to_analyze = ["/var/log/auth.log", "/var/log/secure"]  # Linux log files

    def analyze_user_privileges(self):
        """Analyze the current user's privileges."""
        print("[*] Analyzing User Privileges...")
        user_id = os.getuid()
        groups = os.getgroups()

        if user_id == 0:
            print("[!] User has root privileges.")
        else:
            print("[*] User is not root.")

        print("[*] User belongs to the following groups:")
        for group_id in groups:
            group_name = grp.getgrgid(group_id).gr_name
            print(f"  - {group_name}")

    def check_file_permissions(self, path):
        """Scan critical system files and directories."""
        print("\n[*] Checking File and Directory Permissions...")
        critical_paths = ["/etc/passwd", "/etc/shadow", "/etc/sudoers"]
        for critical_path in critical_paths:
            try:
                stat = os.stat(critical_path)
                if stat.st_mode & 0o777 != 0o644:  # Permissions not secure
                    print(f"[!] Insecure permissions on {critical_path}")
            except FileNotFoundError:
                print(f"[!] {critical_path} not found.")

    def analyze_processes(self):
        """Monitor running processes for suspicious or unauthorized elevated privileges."""
        print("\n[*] Analyzing Processes...")
        for proc in psutil.process_iter(attrs=["pid", "name", "username", "uids"]):
            try:
                uid = proc.info["uids"].real
                if uid == 0 and proc.info["username"] != "root":
                    print(f"[!] Suspicious process with elevated privileges: {proc.info}")
            except psutil.AccessDenied:
                pass

    def analyze_registry(self):
        """Check system registry for unauthorized modifications (Windows only)."""
        if self.os_name != "Windows":
            print("\n[*] Registry Analysis is not supported on this OS.")
            return

        print("\n[*] Analyzing Registry...")
        try:
            reg_keys = [
                r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                r"HKLM\SYSTEM\CurrentControlSet\Services"
            ]
            for key in reg_keys:
                result = subprocess.check_output(["reg", "query", key], shell=True)
                print(f"[!] Registry Key Found: {result.decode()}")
        except Exception as e:
            print(f"[!] Error analyzing registry: {e}")

    def analyze_logs(self):
        """Analyze system logs for privilege escalation attempts."""
        print("\n[*] Analyzing System Logs...")
        for log_file in self.logs_to_analyze:
            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        if "sudo" in line or "permission denied" in line.lower():
                            print(f"[!] Suspicious log entry: {line.strip()}")
            else:
                print(f"[!] Log file not found: {log_file}")

    def run(self):
        """Run the tool."""
        print("=== Local Privilege Escalation Detection Tool ===\n")
        self.analyze_user_privileges()
        self.check_file_permissions("/")
        self.analyze_processes()
        self.analyze_registry()
        self.analyze_logs()


if __name__ == "__main__":
    try:
        tool = PrivilegeEscalationDetectionTool()
        tool.run()
    except KeyboardInterrupt:
        print("\n[!] Exiting...")