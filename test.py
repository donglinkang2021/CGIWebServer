import requests
import threading
import time
from tqdm import tqdm

def perform_request(url):
    try:
        response = requests.get(url)
        # print(f"Response code: {response.status_code}")
        if response.status_code != 200:
            print(f"Request failed: {response.status_code}")
    except Exception as e:
        print(f"Request failed: {e}")

def stress_test(url, num_requests):
    threads = []
    for _ in range(num_requests):
        thread = threading.Thread(target=perform_request, args=(url,))
        threads.append(thread)
        thread.start()
    
    pbar = tqdm(total = num_requests, desc="Stress Testing", dynamic_ncols=True)
    for thread in threads:
        thread.join()
        pbar.update(1)
    pbar.close()

if __name__ == "__main__":
    url = "http://localhost:8888/"
    num_requests_list = [10, 100, 500, 1000]
    cost_time = []
    for num_requests in num_requests_list:
        start_time = time.time()
        stress_test(url, num_requests)
        end_time = time.time()
        cost_time.append(end_time - start_time)

    result = " | ".join([f"{t:.3f}" for t in cost_time]) + " |"
    print(f"Cost time: {result}")

# python main.py --port 8888 --work_dir ./webroot --max_conn 5
# python -m http.server 8888 --cgi -d ./webroot