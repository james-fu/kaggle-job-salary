from data_io import (
    get_paths,
    read_column,
    save_model,
    join_features,
)
from os.path import join as path_join
#import joblib
import numpy as np
#from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_absolute_error


paths = get_paths("Settings.json")
data_dir = paths["data_path"]
cache_dir = path_join(data_dir, "tmp")

features = join_features("%strain_count_vector_matrix_max_f_100",
        ["Title", "FullDescription", "LocationRaw", "LocationNormalized"],
        data_dir)
validation_features = join_features("%svalid_count_vector_matrix_max_f_100",
        ["Title", "FullDescription", "LocationRaw", "LocationNormalized"],
        data_dir)
#try:
    #features = joblib.load(path_join(cache_dir, "train_features_join_100"))
    #print "Loaded features"
#except Exception as e:
    #print e
    #filename = "%strain_count_vector_matrix_max_f_100"
    #extracted = []
    #print("Extracting features and training model")
    #for column_name in ["Title", "FullDescription", "LocationRaw", "LocationNormalized"]:
        #print "Extracting: ", column_name
        #fea = joblib.load(path_join(cache_dir, filename % column_name))
        #if hasattr(fea, "toarray"):
            #extracted.append(fea.toarray())
        #else:
            #extracted.append(fea)
    #if len(extracted) > 1:
        #features = np.concatenate(extracted, axis=1)
    #else:
        #features = extracted[0]
    #joblib.dump(features, path_join(cache_dir, "train_features_join_100"))
print "features", features.shape
print "valid features", validation_features.shape
salaries = np.array(list(read_column(paths["train_data_path"], "SalaryNormalized"))).astype(np.float64)
valid_salaries = np.array(list(read_column(paths["valid_data_path"], "SalaryNormalized"))).astype(np.float64)
print salaries.shape
#classifier = RandomForestRegressor(n_estimators=50,
                                   #verbose=2,
                                   #n_jobs=1,
                                   #oob_score=True,
                                   #min_samples_split=30,
                                   #random_state=3465343)
classifier = SGDRegressor(random_state=3465343, verbose=0, n_iter=1000)
classifier.fit(features, salaries)
predictions = classifier.predict(validation_features)
#oob_predictions = classifier.oob_predictions_
print valid_salaries[1:10]
print predictions[1:10]
mae = mean_absolute_error(valid_salaries, predictions)
print "MAE validation: ", mae
save_model(classifier, "sgd_regressor_default_1000", mae)
