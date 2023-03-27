import os
from concurrent.futures import TimeoutError
from google.api_core import retry
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.types import GetSubscriptionRequest

# 指定服務帳戶密鑰檔案的路徑
key_path = os.path.join(os.getcwd(), "credentials", "peterproject-364114-254f42d07f55.json")

# 設置環境變數
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
project_id = "peterproject-364114"
topic_id = "my-topic"
subscription_id = "my-subscription"
project_path = f"projects/peterproject-364114"
timeout = 5.0  # 設置接收訊息的超時時間
