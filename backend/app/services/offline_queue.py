import json
import os

class OfflineQueueManager:
    def __init__(self, queue_dir="offline_data"):
        self.queue_dir = queue_dir
        if not os.path.exists(self.queue_dir):
            os.makedirs(self.queue_dir, exist_ok=True)

    def save_offline_request(self, request_id: str, data: dict):
        """
        Saves an offline request to the local queue.
        """
        filepath = os.path.join(self.queue_dir, f"{request_id}.json")
        with open(filepath, 'w') as f:
            json.dump(data, f)
        return {"status": "saved", "request_id": request_id}

    def sync_queued_requests(self, sync_callback):
        """
        Syncs queued offline requests by calling the provided callback for each.
        """
        synced = []
        failed = []

        if not os.path.exists(self.queue_dir):
            return {"synced": synced, "failed": failed}

        for filename in os.listdir(self.queue_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self.queue_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    
                    # Attempt to sync using the callback
                    success = sync_callback(data)
                    
                    if success:
                        synced.append(filename)
                        os.remove(filepath)
                    else:
                        failed.append(filename)
                except Exception as e:
                    failed.append(filename)
                    print(f"Failed to sync {filename}: {e}")

        return {"synced": synced, "failed": failed}
