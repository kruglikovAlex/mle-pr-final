import logging as logger
import pandas as pd
import pickle
from implicit.als import AlternatingLeastSquares
from scipy import sparse

class Recommendations:

    def __init__(self):

        self._recs = {"personal": None, "default": None}
        self._stats = {
            "request_personal_count": 0,
            "request_default_count": 0,
        }

        self.model_path = "../models/als_model_v1.npz"
        self._model = ''
        self.user_items_matrix_path = "../models/user_items_matrix.npz"
        self._user_items_matrix = ''
        self.load_encoders(
            "../models/user_encoder.pkl",
            "../models/item_encoder.pkl"
        )
    
    def load_encoders(self, user_encoder_path: str, item_encoder_path: str):
        import pickle
        with open(user_encoder_path, "rb") as f:
            self.user_encoder = pickle.load(f)
        with open(item_encoder_path, "rb") as f:
            self.item_encoder = pickle.load(f)
        print("Encoders loaded.")

    def load(self, type, path, **kwargs):
        """
        Загружает рекомендации из файла
        """

        logger.info(f"Loading recommendations, type: {type}")
        self._recs[type] = pd.read_parquet(path, **kwargs)
        if type == "personal":
            self._recs[type] = self._recs[type].set_index("user_id")
        logger.info(f"Loaded")
    
    def load_matrix(self, user_items_matrix_path: str):
        """
        Загружает user_items_matrix
        """
        print(user_items_matrix_path)

        self._user_items_matrix = sparse.load_npz(user_items_matrix_path)
        print('user_items_matrix loaded')

    def load_model(self, model_path: str):
        """
        Загружает als_model
        """
        print(model_path)
        als_model = AlternatingLeastSquares()
        self._model = als_model.load(model_path)
        print('self._model: ', self._model)
    
    def als_predict(self, user_id:str, item_id:str) -> float:
        
        print('user_id:', user_id, 'item_id:', item_id)
        print(self._model)
        # Преобразуем user_id → индекс строки в матрице
        user_index = self.user_encoder.transform([user_id])[0]
        print('user_index:', user_index)
        return self._model.recommend(user_index, self._user_items_matrix[user_index],filter_already_liked_items=False, N=100)
    
    def get(self, user_id: int, k: int=100):
        """
        Возвращает список рекомендаций для пользователя
        """
        try:
            recs = self._recs["personal"].loc[user_id]
            recs = recs["item_id"].to_list()[:k]
            self._stats["request_personal_count"] += 1
        except KeyError:
            recs = self._recs["default"]
            recs = recs["item_id"].to_list()[:k]
            self._stats["request_default_count"] += 1
        except:
            logger.error("No recommendations found")
            recs = []

        return recs

    def stats(self):

        logger.info("Stats for recommendations")
        for name, value in self._stats.items():
            logger.info(f"{name:<30} {value} ") 
