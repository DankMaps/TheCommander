# File: app.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Updated commands list with new commands
commands = [
    {"command": "free -h", "description": "Display free and used memory in human-readable format."},
    {"command": "free", "description": "Display free and used memory in the system."},
    {"command": "vmstat", "description": "Report virtual memory statistics."},
    {"command": "pmap", "description": "Report memory map of a Process."},
    {"command": "cat /proc/meminfo", "description": "Access detailed memory information."},
    {"command": "grep (with /proc/meminfo)", "description": "Filter specific memory details."},
    {"command": "ps aux --sort=-%mem | head -n 10", "description": "Identify which Process is consuming the most memory."},
    {"command": "top", "description": "Display real-time system summary including memory usage."},
    {"command": "ps", "description": "Report a snapshot of current Processes (includes memory info)."},
    {"command": "htop", "description": "Interactive Processes viewer (requires installation)."},
    {"command": "ps aux", "description": "Display all running Processes."},
    {"command": "lsof", "description": "List open files."},
    {"command": "kill PID", "description": "Terminate a Process by PID."},
    {"command": "killall Processname", "description": "Terminate all Processes by name."},
    {"command": "pkill Processname", "description": "Send signals to Processes by name."},
    {"command": "pgrep Processname", "description": "Get the PID of a Process by name."},
    {"command": "nice -n priority command", "description": "Run a command with a specified priority."},
    {"command": "renice priority PID", "description": "Change the priority of a running Process."},
    {"command": "bg", "description": "Move a Process to the background."},
    {"command": "fg", "description": "Bring a background Process to the foreground."},
    {"command": "strace -p PID", "description": "Trace system calls and signals for a running Process."},
    {"command": "ls", "description": "List directory contents."},
    {"command": "cp source destination", "description": "Copy files or directories."},
    {"command": "mv source destination", "description": "Move or rename files and directories."},
    {"command": "rm file", "description": "Remove files."},
    {"command": "rm -r directory", "description": "Remove directories recursively."},
    {"command": "chmod permissions file", "description": "Change file permissions."},
    {"command": "chown user:group file", "description": "Change file owner and group."},
    {"command": "find /path -name filename", "description": "Find files by name."},
    {"command": "df -h", "description": "Display disk space usage."},
    {"command": "du -sh /path", "description": "Display the size of a directory or file."},
    {"command": "touch filename", "description": "Create an empty file or update file timestamps."},
    {"command": "ln -s target linkname", "description": "Create a symbolic link."},
    {"command": "cat file", "description": "Display the contents of a file."},
    {"command": "less file", "description": "View file contents one page at a time."},
    {"command": "head -n N file", "description": "Display the first N lines of a file."},
    {"command": "tail -n N file", "description": "Display the last N lines of a file."},
    {"command": "grep 'pattern' file", "description": "Search for a pattern in a file."},
    {"command": "tar -cvf archive.tar files", "description": "Create a tar archive."},
    {"command": "tar -xvf archive.tar", "description": "Extract a tar archive."},
    {"command": "gzip file", "description": "Compress files with gzip."},
    {"command": "gunzip file.gz", "description": "Decompress gzip files."},
    {"command": "zip -r archive.zip folder", "description": "Compress files into a zip archive."},
    {"command": "unzip archive.zip", "description": "Extract a zip archive."},
    {"command": "rsync -av source destination", "description": "Synchronize files and directories between two locations."},
    {"command": "adduser username", "description": "Create a new user."},
    {"command": "deluser username", "description": "Remove a user account."},
    {"command": "usermod -aG group username", "description": "Add a user to a group."},
    {"command": "passwd username", "description": "Change user password."},
    {"command": "whoami", "description": "Display the current user."},
    {"command": "id username", "description": "Display user ID and group ID information."},
    {"command": "groups username", "description": "Show group memberships for a user."},
    {"command": "su username", "description": "Switch to another user account."},
    {"command": "chage -l username", "description": "Display password aging information."},
    {"command": "last", "description": "Show the last login of users."},
    {"command": "w", "description": "Display who is logged in and their activity."},
    {"command": "userdel -r username", "description": "Delete a user and their home directory."},
    {"command": "sudo visudo", "description": "Edit the sudoers file to manage user permissions."},
    {"command": "ifconfig", "description": "Display or configure network interfaces (deprecated, use ip instead)."},
    {"command": "ip a", "description": "Show all IP addresses and network interfaces."},
    {"command": "ip link set interface up/down", "description": "Enable/disable a network interface."},
    {"command": "ping hostname", "description": "Send ICMP echo requests to test network connectivity."},
    {"command": "netstat -tulnp", "description": "Display active network connections."},
    {"command": "ss -tuln", "description": "Display active connections (preferred over netstat)."},
    {"command": "traceroute hostname", "description": "Display the path packets take to a network host."},
    {"command": "nslookup hostname", "description": "Query DNS to find IP addresses."},
    {"command": "dig hostname", "description": "DNS lookup (advanced query)."},
    {"command": "hostnamectl", "description": "Set or display the system hostname."},
    {"command": "ufw enable/disable", "description": "Enable/disable uncomplicated firewall."},
    {"command": "ufw allow/deny port", "description": "Allow/deny a specific port through the firewall."},
    {"command": "scp source destination", "description": "Securely copy files between hosts."},
    {"command": "ssh user@hostname", "description": "Log into a remote server using SSH."},
    {"command": "iptables -L", "description": "List current iptables firewall rules."},
    {"command": "nmcli device status", "description": "Display network status using NetworkManager."},
    {"command": "curl -O URL", "description": "Download a file from a URL."},
    {"command": "wget URL", "description": "Download files from the web."},
    {"command": "apt update", "description": "Update the list of available packages."},
    {"command": "apt upgrade", "description": "Upgrade all installed packages."},
    {"command": "apt install package", "description": "Install a new package."},
    {"command": "apt remove package", "description": "Remove a package."},
    {"command": "apt autoremove", "description": "Remove unnecessary packages."},
    {"command": "dpkg -i package.deb", "description": "Install a package from a .deb file."},
    {"command": "dpkg -l", "description": "List all installed packages."},
    {"command": "snap install package", "description": "Install a package using Snap."},
    {"command": "snap list", "description": "List installed Snap packages."},
    {"command": "snap remove package", "description": "Remove a Snap package."}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "").lower()
    result = [cmd for cmd in commands if query in cmd["command"].lower() or query in cmd["description"].lower()]
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
