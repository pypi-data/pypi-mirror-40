# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import types
import numpy as np
import pandas as pd
import collections
from collections import Counter
import numpy as np
import traceback

from sklearn.preprocessing import LabelEncoder
from lime.discretize import QuartileDiscretizer


class TrainingStats():
    """
        Class to generate statistics related to training data
    """

    def __init__(self, training_data_frame, training_data_info):
        self.training_data_frame = training_data_frame
        self.training_data_info = training_data_info
        self.__validate_parameters()

    def __validate_parameters(self):
        # Valudate training data frame
        if self.training_data_frame is None:
            raise Exception("training_data_frame cannot be None or empty")

        if self.training_data_info is None or self.training_data_info == {}:
            raise Exception("Missing training_data_info")

        self.__validate_training_data_info()
        return

    def __validate_training_data_info(self):
        self.feature_columns = []
        self.categorical_columns = []
        self.label_column = None
        self.model_type = None

        self.model_type = self.training_data_info.get("model_type")
        accepted_model_types = ["regression", "binary", "multiclass"]
        if self.model_type not in accepted_model_types:
            raise Exception(
                "Invalid/Missing model type.Accepted values are:"+accepted_model_types)

        # Existence check for label column
        self.label_column = self.training_data_info.get("class_label")
        if self.label_column is None or len(self.label_column) == 0:
            raise Exception("'class_label' cannot be empty")

        #Feature column checks
        self.feature_columns = self.training_data_info.get("feature_columns")
        if self.feature_columns is None or type(self.feature_columns) is not list or len(self.feature_columns) == 0:
            raise Exception("'feature_columns should be a non empty list")

        #Verify existence of feature columns in training data
        columns_from_data_frame = list(self.training_data_frame.columns.values)
        check_feature_column_existence = list(
            set(self.feature_columns) - set(columns_from_data_frame))
        if len(check_feature_column_existence) > 0:
            raise Exception("Feature columns missing in training data.Details:{}".format(
                check_feature_column_existence))


        #Categorical column checks
        self.categorical_columns = self.training_data_info.get("categorical_columns")
        if self.categorical_columns is not None and type(self.categorical_columns) is not list:
            raise Exception("'categorical_columns' should be a list of values")

        # Verify existence of  categorical columns in feature columns
        if self.categorical_columns is not None and len(self.categorical_columns) > 0:
            check_cat_col_existence = list(
                set(self.categorical_columns) - set(self.feature_columns))
            if len(check_cat_col_existence) > 0:
                raise Exception("'categorical_columns' should be subset of feature columns.Details:{}".format(
                    check_cat_col_existence))

    def __get_common_configuration(self):
        common_configuration = {}
        common_configuration["problem_type"] = self.model_type
        common_configuration["label_column"] = self.label_column
        common_configuration["feature_fields"] = self.feature_columns
        common_configuration["categorical_fields"] = self.categorical_columns

        try:
            input_data_schema = self.__generate_training_schema()
        except Exception as ex:
            raise Exception("Error generating input_data_schema.Reason:"+ex)

        common_configuration["input_data_schema"] = input_data_schema
        return common_configuration

    def __generate_training_schema(self):
        fields = []
        payload_df = self.training_data_frame
        columns = payload_df.columns.tolist()
        for column in columns[:]:
            field = {}
            field["name"] = column

            data_type = None
            if payload_df[column].dtype == np.float64 or payload_df[column].dtype == np.float32 or payload_df[column].dtype == np.double or payload_df[column].dtype == np.longdouble:
                data_type = "double"
            elif(payload_df[column].dtype == np.int64 or payload_df[column].dtype == np.int32):
                data_type = "integer"
            elif(payload_df[column].dtype.name.startswith("object")):
                data_type = "string"
            else:
                data_type =  payload_df[column].dtype.name #Defualt to Dataframe data frame data type

            field["type"] = data_type
            field["nullable"] = True

            metadata = {}
            #Set feature column in input schema
            if column in self.feature_columns:
                metadata["modeling_role"] = "feature"

            #Set categorical column in input schema
            if self.categorical_columns is not None:
                if column in self.categorical_columns:
                    metadata["measure"] = "discrete"

            field["metadata"] = metadata
            fields.append(field)

        training_data_schema = {}
        training_data_schema["type"] = "struct"
        training_data_schema["fields"] = fields

        return training_data_schema

    def __get_fairness_configuration(self):
        return {}

    def __get_explanability_configuration(self):
        try:
            data_df = self.training_data_frame
            numeric_columns = list(set(self.feature_columns) ^ set(self.categorical_columns))

            # Convert columns to numeric incase data frame read them as non-numeric
            data_df[numeric_columns] = data_df[numeric_columns].apply(
                pd.to_numeric, errors="coerce")

            # Drop rows with invalid values
            data_df.dropna(axis="index", subset=self.feature_columns, inplace=True)

            random_state = 10
            training_data_schema = list(data_df.columns.values)

            # Feature column index
            feature_column_index = [training_data_schema.index(x) for x in self.feature_columns]

            # Categorical columns index as per feature colums
            categorical_column_index = []
            categorical_column_index = [self.feature_columns.index(x) for x in self.categorical_columns]

            # numeric columns
            numeric_column_index = []
            for f_col_index in feature_column_index:
                index = feature_column_index.index(f_col_index)
                if index not in categorical_column_index:
                    numeric_column_index.append(index)

            # class labels
            class_labels = []
            if self.model_type != "regression":
                if(self.label_column != None):
                    class_labels = data_df[self.label_column].unique()
                    class_labels = class_labels.tolist()

            # Filter feature columns from training data frames
            data_frame = data_df.values
            data_frame_features = data_frame[:, feature_column_index]

            # Compute stats on complete training data
            data_frame_num_features = data_frame_features[:, numeric_column_index]
            num_base_values = np.median(data_frame_num_features, axis=0)
            stds = np.std(data_frame_num_features, axis=0, dtype="float64")
            mins = np.min(data_frame_num_features, axis=0)
            maxs = np.max(data_frame_num_features, axis=0)

            main_base_values = {}
            main_cat_counts = {}
            if(len(categorical_column_index) > 0):
                for cat_col in categorical_column_index:
                    cat_col_value_counts = Counter(data_frame_features[:, cat_col])
                    values, frequencies = map(
                        list, zip(*(cat_col_value_counts.items())))
                    max_freq_index = frequencies.index(np.max(frequencies))
                    cat_base_value = values[max_freq_index]
                    main_base_values[cat_col] = cat_base_value
                    main_cat_counts[cat_col] = cat_col_value_counts

            num_feature_range = np.arange(len(numeric_column_index))
            main_stds = {}
            main_mins = {}
            main_maxs = {}
            for x in num_feature_range:
                index = numeric_column_index[x]
                main_base_values[index] = num_base_values[x]
                main_stds[index] = stds[x]
                main_mins[index] = mins[x]
                main_maxs[index] = maxs[x]

            # Encode categorical columns
            categorical_columns_encoding_mapping = {}
            for column_index_to_encode in categorical_column_index:
                le = LabelEncoder()
                le.fit(data_frame_features[:, column_index_to_encode])
                data_frame_features[:, column_index_to_encode] = le.transform(
                    data_frame_features[:, column_index_to_encode])
                categorical_columns_encoding_mapping[column_index_to_encode] = le.classes_

            # Compute training stats on descritized data
            descritizer = QuartileDiscretizer(
                data_frame_features, categorical_features=categorical_column_index, feature_names=self.feature_columns, labels=class_labels, random_state=random_state)

            d_means = descritizer.means
            d_stds = descritizer.stds
            d_mins = descritizer.mins
            d_maxs = descritizer.maxs
            d_bins = descritizer.bins(data_frame_features, labels=class_labels)

            # Compute feature values and frequencies of all columns
            cat_features = np.arange(data_frame_features.shape[1])
            discretized_training_data = descritizer.discretize(data_frame_features)

            feature_values = {}
            feature_frequencies = {}
            for feature in cat_features:
                column = discretized_training_data[:, feature]
                feature_count = collections.Counter(column)
                values, frequencies = map(list, zip(*(feature_count.items())))
                feature_values[feature] = values
                feature_frequencies[feature] = frequencies

            index = 0
            d_bins_revised = {}
            for bin in d_bins:
                d_bins_revised[numeric_column_index[index]] = bin.tolist()
                index = index + 1

            # Encode categorical columns
            cat_col_mapping = {}
            for column_index_to_encode in categorical_column_index:
                cat_col_encoding_mapping_value = categorical_columns_encoding_mapping[
                    column_index_to_encode]
                cat_col_mapping[column_index_to_encode] = cat_col_encoding_mapping_value.tolist(
                )
        except Exception as ex:
            print(ex.with_traceback)
            raise Exception("Error while generating explanability configuration.Reason:%s" % ex)

        # Construct stats
        data_stats = {}
        data_stats["feature_columns"] = self.feature_columns
        data_stats["categorical_columns"] = self.categorical_columns

        # Common
        data_stats["feature_values"] = feature_values
        data_stats["feature_frequencies"] = feature_frequencies
        data_stats["class_labels"] = class_labels
        data_stats["categorical_columns_encoding_mapping"] = cat_col_mapping

        # Descritizer
        data_stats["d_means"] = d_means
        data_stats["d_stds"] = d_stds
        data_stats["d_maxs"] = d_maxs
        data_stats["d_mins"] = d_mins
        data_stats["d_bins"] = d_bins_revised

        # Full data
        data_stats["base_values"] = main_base_values
        data_stats["stds"] = main_stds
        data_stats["mins"] = main_mins
        data_stats["maxs"] = main_maxs
        data_stats["categorical_counts"] = main_cat_counts

        # Convert to json
        explainability_configuration = {}
        for k in data_stats:
            key_details = data_stats.get(k)
            if(key_details is not None) and (not isinstance(key_details, list)):
                new_details = {}
                for key_in_details in key_details:
                    new_details[str(key_in_details)
                                ] = key_details[key_in_details]
            else:
                new_details = key_details
            explainability_configuration[k] = new_details

        return explainability_configuration

    def get_training_statistics(self):
        """
            Method to generate training data distribution
        """
        common_config = self.__get_common_configuration()
        fairness_config = self.__get_fairness_configuration()
        explain_config = self.__get_explanability_configuration()

        stats_configuration = {}
        stats_configuration["common_configuration"] = common_config
        stats_configuration["fairness_configuration"] = fairness_config
        stats_configuration["explainability_configuration"] = explain_config
        return stats_configuration
