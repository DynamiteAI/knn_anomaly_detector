import typing

import pandas
from dynamite_analyzer_framework import analyzers
from dynamite_analyzer_framework.inputs import Input
from dynamite_analyzer_framework.outputs import Message, Output

from knn_anomaly_detector import train, predict

KNNAnomalyDetectorAnalyzerClassType = typing.TypeVar('KNNAnomalyDetectorAnalyzerClassType')


class KNNAnomalyDetectorAnalyzer(analyzers.Analyzer):

    def __init__(self, input_inst: Input, output_inst: Output, load_model=True, domain='main',
                 train_fields=('duration', 'orig_bytes', 'id.resp_p', 'resp_bytes', 'orig_ip_bytes', 'resp_pkts',
                               'resp_ip_bytes'),
                 include_fields=('uid', 'community_id', 'duration', 'orig_bytes', 'id.resp_p', 'resp_bytes',
                                 'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes'), contamination=0.01, n_neighbors=10):
        self.train_fields = train_fields
        self.include_fields = include_fields
        self.load_model = load_model
        self.domain = domain
        self.contamination = contamination
        self.n_neighbors = n_neighbors
        super(KNNAnomalyDetectorAnalyzer, self).__init__(input_inst, output_inst)

    def evaluate(self) -> KNNAnomalyDetectorAnalyzerClassType:
        input_df = pandas.DataFrame(self.input.data)
        if self.load_model:
            predictions = predict.predict_knn_anomaly_detector(input_df, domain=self.domain,
                                                               train_fields=self.train_fields,
                                                               include_fields=self.include_fields)
        else:
            train.train_knn_anomaly_detector(input_df, domain=self.domain, train_fields=self.train_fields,
                                             contamination=self.contamination, n_neighbors=self.n_neighbors)
            predictions = predict.predict_knn_anomaly_detector(input_df, domain=self.domain,
                                                               train_fields=self.train_fields,
                                                               include_fields=self.include_fields)

        for prediction in list(predictions):

            # Remove non-anomalies
            if not prediction[0]:
                continue
            prediction_dict = dict(
                score=prediction[0],
            )

            for i in range(0, len(self.include_fields)):
                prediction_dict[self.include_fields[i]] = prediction[i + 1]
            self.output.add_message(
                Message(dataset_name=self.domain, score=prediction_dict['score'], msg="anomaly",
                        data_extra=prediction_dict))
        return self
