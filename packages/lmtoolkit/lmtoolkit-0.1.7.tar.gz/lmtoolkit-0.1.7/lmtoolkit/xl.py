import pandas as pd
import numpy as np

class LIBFFMConverter():
    def __init__(self):
        self.features_map = None

    def fit(self, df, target):
        df = df.copy()
        self.features = list(df.columns.drop(target).values)
        appended_field_df = self.__append_fields(df, self.features)
        self.features_map = self.__build_features_map(df, self.features)
        return self

    def transform(self, df):
        mapped_df = self.map_df(df)
        return self.__to_libffm(mapped_df, self.features)

    def fit_transform(self, df, target):
        self.fit(df, target)
        return self.transform(df)

    def map_df(self, df):
        appended_field_df = self.__append_fields(df.copy(), self.features)
        mapped_df = self.__map_features(appended_field_df, self.features, self.features_map)
        return mapped_df

    def __map_features(self, df, features, features_map):
        for field_idx, c in enumerate(features):
            df[c] = df[c].apply(lambda x: features_map[x] if x in features_map.keys() else -1)
        return df

    def __to_libffm(self, df, features):
        def stringify(s, field_idx):
            return s.apply(lambda x: '{}:{}:{}'.format(field_idx, x, 1))

        for field_idx, c in enumerate(features):
            df[c] = stringify(df[c], field_idx)
        return df

    def __append_fields(self, df, features):
        def append_field(s, field_idx):
            return s.apply(lambda x: '{}-{}'.format(field_idx, x))
        
        for field_idx, c in enumerate(features):
            df[c] = append_field(df[c], field_idx)
        return df

    def __build_features_map(self, df, features):
        features_map = []
        for field_idx, c in enumerate(features):
            features_map += sorted(list(df[c].unique()))
        features_map = {v:k for (k, v) in dict(enumerate(features_map)).items()}
        return features_map

    def join_ffm_weights(self, df, weights_path):
        mapped_df = self.map_df(df)
        reader = FFMWeightReader()
        weights = reader.read_weights(weights_path)

        original_columns = list(df.columns.values)
        for f in self.features:
            temp = weights.copy()
            n_cols = weights.shape[1]
            temp.columns = ['{}_{}'.format(f, i) for i in range(n_cols)]
            mapped_df = mapped_df.join(temp, f)

        mapped_df = mapped_df.drop(original_columns, 1)
        return mapped_df

class FFMWeightReader:
    def read_weights(self, path):
        df = pd.read_csv(path, header=None)
        df['idx'] = df[0].apply(self.__get_idx)
        df['value'] = df[0].apply(self.__get_value)
        df.drop(0, 1, inplace=True)

        # read biases
        bias = df[df['idx'].apply(self.__get_biases)]
        bias['feature'] = bias['idx'].apply(self.__get_bias_feature)
        bias.drop('idx', 1, inplace=True)
        bias = bias.set_index('feature').reset_index(drop=True)
        bias['value'] = bias['value'].astype(np.float)

        # read latent vectors
        latents = df[df['idx'].apply(self.__get_latents)].reset_index(drop=True)
        X = np.stack(latents['value'].apply(self.__get_values).values)
        X = pd.DataFrame(X)
        latents = pd.concat([latents.drop('value', 1), X], 1)
        latents['feature'] = latents['idx'].apply(self.__get_latent_feature)
        latents.drop('idx', 1, inplace=True)

        vectors = []
        features = latents['feature'].unique()

        for f in features:
            vector = latents[latents['feature'] == f].drop('feature', 1)
            vector = list(vector.values.reshape(-1))
            vectors.append(vector)

        latents = pd.DataFrame(vectors, index=features)

        # merge bias and latent vectors
        weights = pd.DataFrame(np.hstack([bias.values, latents.values]))
        return weights

    def __get_idx(self, x):
        return x.split(':')[0]

    def __get_value(self, x):
        return x.split(':')[1]

    def __get_biases(self, x):
        return 'i_' in x

    def __get_bias_feature(self, x):
        return x.split('_')[1]

    def __get_latents(self, x):
        return 'v_' in x

    def __get_values(self, x):
        return [np.float(v) for v in x.split()]

    def __get_latent_feature(self, x):
        return x.split('_')[1]
