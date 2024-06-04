from multiprocessing import Process
import subprocess

def run_script(script_name):
    subprocess.Popen(["g:/dota2_v2/venv/Scripts/pythonw", f"{script_name}.py"])

if __name__ == "__main__":
    script_names = ["usb", "db_worker", "keyboard_app", "bot"]
    processes = []

    for script_name in script_names:
        processes.append(Process(target=run_script, args=(script_name,)))

    for process in processes:
        process.start()

    for process in processes:
        process.join()
