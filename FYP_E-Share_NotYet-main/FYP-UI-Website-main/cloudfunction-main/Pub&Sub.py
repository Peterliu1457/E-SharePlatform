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

# 列出訂閱的有效 ack_ids
response = subscriber.list_subscriptions(request={"project": project_path})
for subscription in response:
    if subscription.name == subscription_path:
        if isinstance(subscription, pubsub_v1.types.Subscription):
            for received_ack_id, expiration_time in subscription.ack_deadline_seconds.items():
                print(f"Ack ID: {received_ack_id}, Expiration Time: {expiration_time}")
        break

# 獲取訂閱詳細資訊，包括 ack_ids 和過期時間
subscription = subscriber.get_subscription(subscription_path, ack_ids=True)
for received_ack_id, expiration_time in subscription.ack_deadline_seconds.items():
    print(f"Ack ID: {received_ack_id}, Expiration Time: {expiration_time}")

# 修改 ack_id 的過期時間（如果有效）
received_ack_id = "1234567890"
if received_ack_id in subscription.ack_deadline_seconds:
    response = subscriber.modify_ack_deadline(request={"subscription": subscription_path, "ack_ids": [received_ack_id], "ack_deadline_seconds": 0})
    print("Deadline modified for ack_id:", received_ack_id)
else:
    print("Invalid ack_id:", received_ack_id)

for n in range(1, 10):
    data_str = f"Message number {n}"
    # Data must be a bytestring
    data = data_str.encode("utf-8")
    # 當您發布一條訊息時，客戶端會返回一個 future
    future = publisher.publish(topic_path, data)

print(f"Published messages to {topic_path}.")

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    ack_id = message.ack_id  # 取得 ack_id
    message.ack()
    subscriber.modify_ack_deadline(subscription_path, [ack_id], ack_deadline_seconds=0)

# 使用最大訊息數和最大位元組數創建流程控制實例
flow_control = pubsub_v1.types.FlowControl(max_messages=5, max_bytes=1024)

# 開始使用回調函數和流程控制的訂閱者
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback, flow_control=flow_control)

print("Listening for messages on {}.".format(subscription_path))
NUM_MESSAGES = 3    
