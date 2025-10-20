import numpy as np
import pandas as pd
import scipy
import sklearn.preprocessing
import pickle
from scipy import sparse
from implicit.als import AlternatingLeastSquares

# загрузка данных, если нужно
events = pd.read_parquet("../data/e-comerce/events.parquet")
items = pd.read_parquet("../data/e-comerce/items.parquet")

items = items.rename(columns={'itemid':'item_id'})

# Для ALS нужна разреженная матрица пользователь × товар × сила взаимодействия.
# Силу взаимодействия можно задать как:
# - просмотр → 1 балл
# - добавление в корзину → 3 балла
# - покупка → 5 баллов
interaction_weights = {"view": 1, "addtocart": 3, "transaction": 5}

events["weight"] = events["event"].map(interaction_weights)

user_view_interactions = (
    events.groupby(["user_id", "item_id"])["weight"]
    .sum()
    .reset_index()
)

# кодируем
user_encoder = sklearn.preprocessing.LabelEncoder()
item_encoder = sklearn.preprocessing.LabelEncoder()

user_view_interactions["user_id_enc"] = user_encoder.fit_transform(user_view_interactions["user_id"])
user_view_interactions["item_id_enc"] = item_encoder.fit_transform(user_view_interactions["item_id"])

# Сохраняем user_encoder
with open("./services/models/user_encoder.pkl", "wb") as f:
    pickle.dump(user_encoder, f)

# Сохраняем item_encoder
with open("./services/models/item_encoder.pkl", "wb") as f:
    pickle.dump(item_encoder, f)

# Получаем разреженную матрицу для ALS 
rows = user_view_interactions["user_id_enc"].values
cols = user_view_interactions["item_id_enc"].values
data = user_view_interactions["weight"].values #user_view_interactions["viewcount"].values

user_item_csr = scipy.sparse.csr_matrix((data, (rows, cols)))

# Сохранение
sparse.save_npz("./services/models/user_items_matrix.npz", user_item_csr)

# Имея подготовленную матрицу взаимодействий, перейдём к третьему шагу — создадим ALS-модель.
# Для примера возьмём количество латентных факторов для матриц $P, Q$, равным 50. 
als_model_v1 = AlternatingLeastSquares(factors=50, iterations=50, regularization=0.05, random_state=0)
als_model_v1.fit(user_item_csr) 

# сохраняем модель
als_model_v1.save("../models/als_model_v1.npz")

# сохраняем маппинги
with open("../models/mappings_v1.pkl", "wb") as f:
    pickle.dump({"rows": rows,"cols": cols, "data":data}, f)