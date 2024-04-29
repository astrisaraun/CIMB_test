import subprocess

def run_shell_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode !=  0:
        print(f"Error: {stderr.decode('utf-8')}")
    else:
        print(f"Output: {stdout.decode('utf-8')}")

if __name__ == "__main__":
    # Mengatur hak akses untuk skrip
    run_shell_command("chmod +x scripts/run_tests.sh")

    # Menjalankan skrip
    run_shell_command("./scripts/run_tests.sh")
