import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display
import logging

logging.basicConfig(level=logging.DEBUG, filename="test_service.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")

events_store_url = "http://127.0.0.1:8082"
recommendations_url = "http://127.0.0.1:8088"

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

# получение рекомендаций
user_id = 1407515
event_item_ids =  [193218, 452955, 460429, 206783, 395014, 185245]

logging.info(f"Формирование взаимодействия пользователя {user_id} с системой:")
for event_item_id in event_item_ids:
    logging.info(f"- url: {events_store_url}/put, params='user_id':{user_id}, 'item_id':{event_item_id}")
    resp = requests.post(
        events_store_url + "/put", 
        headers=headers, 
        params={"user_id": user_id, "item_id": event_item_id})


params = {"user_id": 1407515, 'k': 10}
logging.info(f"Получение off-line рекомендаций: url-{recommendations_url}/recommendations_offline, params={params}")
resp_offline = requests.post(recommendations_url + "/recommendations_offline", headers=headers, params=params)
logging.info(f"Получение on-line рекомендаций: url-{recommendations_url}/recommendations_online, params={params}")
resp_online = requests.post(recommendations_url + "/recommendations_online", headers=headers, params=params)
logging.info(f"Получение all рекомендаций: url-{recommendations_url}/recommendations, params={params}")
resp_blended = requests.post(recommendations_url + "/recommendations", headers=headers, params=params)

recs_offline = resp_offline.json()["recs"]
recs_online = resp_online.json()["recs"]
recs_blended = resp_blended.json()["recs"]

print(recs_offline)
print(recs_online)
print(recs_blended) 

items = pd.read_parquet('../data/items.parquet')
#items = items.rename(columns={'item_id':'item_id'})

def display_items(item_ids):

    item_columns_to_use = ["item_id","property","value","parentid"]
    
    items_selected = items.query("item_id in @item_ids")[item_columns_to_use]
    #items_selected = items_selected.set_index("item_id").reindex(item_ids)
    items_selected = items_selected.reset_index()
    
    display(items_selected)
    logging.info(f"Вывод: \n{items_selected}")
    
print("Онлайн-события")
logging.info("Онлайн-события")
display_items(event_item_ids)

print("Офлайн-рекомендации")
logging.info("Офлайн-рекомендации")
display_items(recs_offline)

print("Онлайн-рекомендации")
logging.info("Онлайн-рекомендации")
display_items(recs_online)

print("Рекомендации")
logging.info("Рекомендации")
display_items(recs_blended) 