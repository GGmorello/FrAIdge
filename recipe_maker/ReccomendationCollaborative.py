"""import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD

recipe = pd.read_csv("Recipes.csv")
recipe = recipe.loc[:, ['title']]
recipe['recipeId'] = recipe.index

rating = pd.read_csv("rating.csv")
rating.columns = ['userId','recipeId','rating']

data = pd.merge(recipe, rating)
data = data.iloc[:1000000,:]
pivot_table = data.pivot_table(index=["userId"], columns=["title"],values="rating")
pivot_table = pivot_table.fillna(0)

print(pivot_table.head(10))
epsilon = 1e-9
n_latent_factors = 10

# generate item lantent features
item_svd = TruncatedSVD(n_components = n_latent_factors)
item_features = item_svd.fit_transform(pivot_table.transpose()) + epsilon

# generate user latent features
user_svd = TruncatedSVD(n_components = n_latent_factors)
user_features = user_svd.fit_transform(pivot_table) + epsilon
"""

"""from IPython.display import clear_output
import pandas as pd
import tensorflow as tf
import tensorflow_recommenders as tfrs
import tensorflow.keras as keras
from sklearn.model_selection import train_test_split


def df_to_ds(df):
    return {
        "userId": tf.constant(df['userId'].tolist()),
        "recipeId": tf.constant(df['recipeId'].tolist()),
        'rating': tf.constant(df['rating'].tolist())
    }


class RankingModel(keras.Model):

    def __init__(self, user_id, item_id, embedding_size):
        super().__init__()

        # user model
        input = keras.Input(shape=(), dtype=tf.string)
        x = keras.layers.StringLookup(
            vocabulary=user_id, mask_token=None
        )(input)
        output = keras.layers.Embedding(
            input_dim=len(user_id) + 1,
            output_dim=embedding_size,
            name='embedding'
        )(x)
        self.user_model = keras.Model(inputs=input,
                                      outputs=output,
                                      name='user_model')

        # item model
        input = keras.Input(shape=(), dtype=tf.string)
        x = keras.layers.StringLookup(
            vocabulary=item_id, mask_token=None
        )(input)
        output = keras.layers.Embedding(
            input_dim=len(item_id) + 1,
            output_dim=embedding_size,
            name='embedding'
        )(x)
        self.item_model = keras.Model(inputs=input,
                                      outputs=output,
                                      name='item_model')

        # rating model
        concat_shape = self.user_model.layers[-1].output_shape[1] \
                       + self.item_model.layers[-1].output_shape[1]

        input = keras.Input(shape=(concat_shape,))
        x = keras.layers.Dense(256, activation='relu')(input)
        x = keras.layers.Dense(64, activation='relu')(x)
        output = keras.layers.Dense(1)(x)

        self.ratings = keras.Model(
            inputs=input,
            outputs=output,
            name='rating_model'
        )

    def call(self, inputs):
        user_id, item_id = inputs

        user_emb = self.user_model(user_id)
        item_emb = self.item_model(item_id)
        concat = tf.concat([user_emb, item_emb], axis=1)
        prediction = self.ratings(concat)

        return prediction


class GMFModel(tfrs.models.Model):

    def __init__(self, user_id, item_id, embedding_size):
        super().__init__()
        self.ranking_model = RankingModel(user_id,
                                          item_id,
                                          embedding_size)
        self.task = tfrs.tasks.Ranking(
            loss=keras.losses.MeanSquaredError(),
            metrics=[keras.metrics.RootMeanSquaredError()]
        )

    def call(self, features):
        return self.ranking_model(
            (features[0]['user_id'], features[0]['item_id'])
        )

    def compute_loss(self, features, training=False):
        label = features[0]['rating']
        return self.task(labels=label,
                         predictions=self(features))

rating = pd.read_csv('rating.csv')
rating.columns = ['userId','recipeId','rating']
userId = rating['userId']
recipeId = rating['recipeId']
# preprocess
train, test = train_test_split(rating, train_size=.8, random_state=42)
train, test = df_to_ds(train), df_to_ds(test)

# init model
embedding_size = 32
model = GMFModel(userId.astype(str), recipeId.astype(str), embedding_size)
model.compile(
    optimizer=keras.optimizers.Adagrad(learning_rate=.01)
)

# fitting the model
model.fit(train, epochs=3, verbose=0)

# evaluate with the test data
result = model.evaluate(test, return_dict=True, verbose=0)
print("\nEvaluation on the test set:")
display(result)

# extract item embedding
item_emb = model.ranking_model.item_model.layers[-1].get_weights()[0]

item_corr_mat = cosine_similarity(item_emb)

print("\nThe top-k similar movie to item_id 99")
similar_items = top_k_items(name2ind['99'],
                            top_k=10,
                            corr_mat=item_corr_mat,
                            map_name=ind2name)

display(items.loc[items[ITEM_COL].isin(similar_items)])

del item_corr_mat
gc.collect();
"""

import pandas as pd
from surprise import KNNWithMeans
from surprise import Reader
from surprise import Dataset
from surprise import SVD, accuracy
from surprise.model_selection import GridSearchCV
from surprise.model_selection.split import train_test_split

rating = pd.read_csv('rating.csv')
rating.columns = ['userId','recipeId','rating']
reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(rating[["userId", "recipeId", "rating"]][:10000], reader)
train, test = train_test_split(data, test_size=.2, random_state=42)

sim_options = {
    "name": "cosine",
    "user_based": False,  # Compute  similarities between items
}
algo = KNNWithMeans(sim_options=sim_options)
algo.fit(train)

verify = algo.test(test)
pred = algo.predict('0', '0')

print(pred.est)

print(accuracy.rmse(verify))

"""
exit()
sim_options = {
    "name": ["msd", "cosine"],
    "min_support": [6, 7, 8, 9, 10],
    "user_based": [False, True],
}

param_grid = {"sim_options": sim_options}

gs = GridSearchCV(KNNWithMeans, param_grid, measures=["rmse", "mae"], cv=3)
gs.fit(data)

print(gs.best_score["rmse"])
print(gs.best_params["rmse"])

prediction = gs.predict('0', '0')
print(prediction.est)


param_grid = {
    "n_epochs": [5, 10],
    "lr_all": [0.002, 0.005],
    "reg_all": [0.4, 0.6]
}
gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], cv=3)

gs.fit(data)

print(gs.best_score["rmse"])
print(gs.best_params["rmse"])

prediction = gs.predict('0', '0')
print(prediction.est)
"""