import os
import hashlib

import joblib
import pandas

from dynamite_analyzer_framework import const


def predict_knn_anomaly_detector(input_df: pandas.DataFrame, domain: str, train_fields=(), include_fields=()):
    """
    :param input_df: The input dataframe
    :param domain: The domain (model name)
    :param train_fields: The features (numeric only)
    :param include_fields: The fields to include with the prediction (for correlation)
    :return: A list of predictions with included fields
    """
    feature_group_id = hashlib.md5(str(list(train_fields).sort()).encode()).hexdigest()
    drop_fields = [field for field in input_df.columns if field not in train_fields]
    train_df = input_df.drop(drop_fields, axis=1)
    for column in train_df.columns:
        train_df[column] = train_df[column].fillna(0)

    model_directory = os.path.join(const.DYNAMITE_CONF_ROOT, 'models', 'knn_anomaly_detector', feature_group_id)
    model_pkl_file = os.path.join(model_directory, domain + '.pkl')

    model = joblib.load(model_pkl_file)
    predictions = model.predict(train_df)
    include_fields_lists = []
    for field in include_fields:
        include_fields_lists.append(input_df[field].tolist())
    return zip(predictions, *include_fields_lists)
