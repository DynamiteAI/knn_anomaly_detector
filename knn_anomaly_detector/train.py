import os
import hashlib
import joblib
import pandas
from pyod.models.knn import KNN

from dynamite_analyzer_framework import const


def makedirs(path, exist_ok=True):
    if exist_ok:
        if not os.path.exists(path):
            os.makedirs(path)
    else:
        os.makedirs(path)


def train_knn_anomaly_detector(input_df: pandas.DataFrame, domain: str, train_fields=(),
                               n_neighbors=10, contamination=0.1):
    """
    :param input_df: The input dataframe
    :param domain: The domain (model name)
    :param train_fields: The features (numeric only)
    :param n_neighbors: Number of neighbors to use by default for k neighbors queries.
    :param contamination: The amount of contamination of the data set, i.e. the proportion of outliers in the data set.
                          Used when fitting to define the threshold on the decision function
    :return: A list of predictions with included fields
    """

    feature_group_id = hashlib.md5(str(list(train_fields).sort()).encode()).hexdigest()
    drop_fields = [field for field in input_df.columns if field not in train_fields]
    train_df = input_df.drop(drop_fields, axis=1)
    for column in train_df.columns:
        train_df[column] = train_df[column].fillna(0)
    model_directory = os.path.join(const.DYNAMITE_CONF_ROOT, 'models', 'knn_anomaly_detector', feature_group_id)
    model_pkl_file = os.path.join(model_directory, domain + '.pkl')

    makedirs(model_directory)

    model = KNN(contamination=contamination, n_neighbors=n_neighbors, metric='manhattan')

    joblib.dump(model.fit(train_df), model_pkl_file)
