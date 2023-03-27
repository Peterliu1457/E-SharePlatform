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

# Publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Subscriber
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

# 發布一條訊息
message = b"Apply Successful!"
future = publisher.publish(topic_path, message)
message_id = future.result()

# 編輯已發布訊息內容
data = b"Edited message."
ack_id = message_id.split("/")[-1]

# 獲取訂閱的詳細資訊，包括 ack_ids 和過期時間
subscription_path = "projects/peterproject-364114/subscriptions/my-subscription"
print(subscription_path)
request = GetSubscriptionRequest(subscription=subscription_path)
subscription_details = subscriber.get_subscription(request=request)

subscription_details = subscriber.get_subscription(subscription_path)
for received_ack_id, expiration_time in subscription_details.ack_deadline_seconds.items():
    print(f"Ack ID: {received_ack_id}, Expiration Time: {expiration_time}")
    print(subscription_details)
