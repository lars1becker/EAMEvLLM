import statistics
import subprocess
import psutil

memory_usages = []
for _ in range(10):
    process = subprocess.Popen(
        ["python", "./data/void/code/qwen2.5-coder_8_0.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    proc = psutil.Process(process.pid)
    memory_usages.append(proc.memory_info().rss / 1024)
    process.wait()  # Wait for process to complete
    
avg_memory_usage = statistics.mean(memory_usages)
print(f'Average Memory Usage: {avg_memory_usage} KB')