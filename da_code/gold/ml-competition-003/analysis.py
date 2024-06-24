
from collections import defaultdict
from copy import copy
from functools import partial
from itertools import product

# Sub-modules and so on.
import numpy as np
import pandas as pd
import scipy.stats as stats

from scipy.stats import gaussian_kde
from scipy.stats import probplot
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.compose import make_column_selector
from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import mutual_info_classif
from sklearn.impute import KNNImputer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import Binarizer
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import PowerTransformer
from sklearn.preprocessing import StandardScaler

competition = "icr-identify-age-related-conditions"
train_path = f"../train.csv"
test_path = f"../test.csv"
greeks_path = f"../greeks.csv"
train = pd.read_csv(train_path, index_col="Id").rename(columns=str.strip)
test = pd.read_csv(test_path, index_col="Id").rename(columns=str.strip)
greeks = pd.read_csv(greeks_path, index_col="Id").rename(columns=str.strip)

missing_values_cols = train.isna().sum()[train.isna().sum() > 0].index.to_list()
print( "Training Dataset Missing Values\n")
for feature in missing_values_cols:
    print(
        (feature) + "\t",
        (str(train[feature].isna().sum())) + "\t",
        (f"{train[feature].isna().sum() / len(train):.1%}") + "\t",
        (f"{train[feature].dtype}"),
    )
def get_kde_estimation(data_series):
    kde = gaussian_kde(data_series.dropna())
    kde_range = np.linspace(
        data_series.min() - data_series.max() * 0.1,
        data_series.max() + data_series.max() * 0.1,
        len(data_series),
    )
    estimated_values = kde.evaluate(kde_range)
    estimated_values_cum = np.cumsum(estimated_values)
    estimated_values_cum /= estimated_values_cum.max()
    return kde_range, estimated_values, estimated_values_cum
def get_n_rows_axes(n_features, n_cols=5, n_rows=None):
    n_rows = int(np.ceil(n_features / n_cols))
    current_col = range(1, n_cols + 1)
    current_row = range(1, n_rows + 1)
    return n_rows, list(product(current_row, current_col))
problematic_variables = train[["AR", "AY", "BZ", "DF", "DV"]]

problematic_variables_vs_class = problematic_variables.join(train.Class)
duplicated_rows = problematic_variables_vs_class.duplicated(
    subset=["AR", "AY", "BZ", "DF", "DV"]
)

duplicates = problematic_variables_vs_class[duplicated_rows]
no_duplicates = problematic_variables_vs_class[~duplicated_rows]

print(
  "Ratio of duplicated / not duplicated rows in ['AR', 'AY', 'BZ', 'DF', 'DV'] subset:\n"
)
print("Duplicated rows:".ljust(20), f"{len(duplicates)}")
print("Not duplicated rows:".ljust(20),  f"{len(no_duplicates)}\n")

print("Class balance when ['AR', 'AY', 'BZ', 'DF', 'DV'] are duplicated:\n")
for key, value in duplicates.Class.value_counts(normalize=True).to_dict().items():
    print( f"Class {key}:",  f"{value:.1%}")

print( "\nClass balance when ['AR', 'AY', 'BZ', 'DF', 'DV'] are not duplicated:\n")
for key, value in no_duplicates.Class.value_counts(normalize=True).to_dict().items():
    print(f"Class {key}:", "{value:.1%}")
df = greeks[["Epsilon", "Class"]]

# Convert Epsilon to datetime, coerce errors to NaT
df["Epsilon"] = pd.to_datetime(df["Epsilon"], errors="coerce")

# Drop rows where Epsilon is NaT
df = df.dropna(subset=["Epsilon"])

# Apply toordinal to convert dates to integers
df["Epsilon"] = df["Epsilon"].apply(pd.Timestamp.toordinal)

# Replace ordinal value 1 with NaN (if needed)
df["Epsilon"] = df["Epsilon"].replace(1, np.nan)

# Normalize the dates
df["Epsilon"] = df["Epsilon"].transform(lambda x: (x - x.min()) / (x.max() - x.min()))

# Drop any rows that resulted in NaN from the transformation
df = df.dropna()

# Convert to numpy arrays for further processing
epsilon = df["Epsilon"].to_numpy()[:, np.newaxis]
target = df["Class"].to_numpy()

# Perform mutual information classification
mutual_info = mutual_info_classif(epsilon, target, random_state=42)

# Perform ANOVA F-test
f_stat, p_value = f_classif(epsilon, target)

# Output results
print("Mutual Information:", mutual_info)
print("F-statistic:", f_stat)
print("P-value:", p_value)

r2_scores = defaultdict(tuple)
numeric_data = train.select_dtypes("number")
numeric_cols = numeric_data.drop("Class", axis=1).columns.tolist()

for feature in numeric_cols:
    orig = train[feature].dropna()
    _, (*_, R_orig) = probplot(orig, rvalue=True)
    _, (*_, R_log) = probplot(np.log(orig), rvalue=True)
    _, (*_, R_sqrt) = probplot(np.sqrt(orig), rvalue=True)
    _, (*_, R_reci) = probplot(np.reciprocal(orig), rvalue=True)
    _, (*_, R_boxcox) = probplot(stats.boxcox(orig)[0], rvalue=True)
    _, (*_, R_yeojohn) = probplot(stats.yeojohnson(orig)[0], rvalue=True)
    r2_scores[feature] = (
        R_orig * R_orig,
        R_log * R_log,
        R_sqrt * R_sqrt,
        R_reci * R_reci,
        R_boxcox * R_boxcox,
        R_yeojohn * R_yeojohn,
    )

r2_scores = pd.DataFrame(
    r2_scores, index=("Original", "Log", "Sqrt", "Reciprocal", "BoxCox", "YeoJohnson")
).T

r2_scores["Winner"] = r2_scores.idxmax(axis=1)

no_transform_cols = r2_scores.query("Winner == 'Original'").index
log_transform_cols = r2_scores.query("Winner == 'Log'").index
sqrt_transform_cols = r2_scores.query("Winner == 'Sqrt'").index
reciprocal_transform_cols = r2_scores.query("Winner == 'Reciprocal'").index
boxcox_transform_cols = r2_scores.query("Winner == 'BoxCox'").index
yeojohnson_transform_cols = r2_scores.query("Winner == 'YeoJohnson'").index
numeric_descr = (
    train.drop("Class", axis=1)
    .describe(percentiles=[0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99])
    .drop("count")
    .T.rename(columns=str.title)
)
semi_constant_mask = np.isclose(numeric_descr["Min"], numeric_descr["50%"])
semi_constant_descr = numeric_descr[semi_constant_mask]
semi_constant_features_corr = (
    train[np.r_[semi_constant_descr.index, ["Class"]]]
    .corr(method="pearson")["Class"]
    .to_dict()
)
semi_const_cols_thresholds = semi_constant_descr["50%"].to_dict()
semi_const_cols = semi_const_cols_thresholds.keys()

# We don't have square root transformations.
no_transform_cols = no_transform_cols.drop(semi_const_cols, errors="ignore")
log_transform_cols = log_transform_cols.drop(semi_const_cols, errors="ignore")
reciprocal_transform_cols = reciprocal_transform_cols.drop(semi_const_cols, errors="ignore")
boxcox_transform_cols = boxcox_transform_cols.drop(semi_const_cols, errors="ignore")
yeojohnson_transform_cols = yeojohnson_transform_cols.drop(semi_const_cols, errors="ignore")

preliminary_preprocess = make_pipeline(
    make_column_transformer(
        (
            StandardScaler(),
            no_transform_cols.to_list(),
        ),
        (
            make_pipeline(
                FunctionTransformer(func=np.log, feature_names_out="one-to-one"),
                StandardScaler(),
            ),
            log_transform_cols.to_list(),
        ),
        (
            make_pipeline(
                FunctionTransformer(func=np.reciprocal, feature_names_out="one-to-one"),
                StandardScaler(),
            ),
            reciprocal_transform_cols.to_list(),
        ),
        (
            PowerTransformer(method="box-cox", standardize=True),
            boxcox_transform_cols.to_list(),
        ),
        (
            PowerTransformer(method="yeo-johnson", standardize=True),
            yeojohnson_transform_cols.to_list(),
        ),
        (
            make_pipeline(
                SimpleImputer(strategy="most_frequent"),
                OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
            ),
            make_column_selector(dtype_include=object),  # type: ignore
        ),
        *[
            (
                make_pipeline(
                    SimpleImputer(strategy="median"),
                    Binarizer(threshold=thresh),
                ),
                [col],
            )
            for col, thresh in semi_const_cols_thresholds.items()
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    ),
    KNNImputer(n_neighbors=10, weights="distance"),
).set_output(transform="pandas")
def get_undersampling_fraction(y_true):
    N0, N1 = np.bincount(y_true)
    return 1 - N1 / N0


def assert_balanced_learning(y_train, n_samples_tol=1):
    N0, N1 = np.bincount(y_train)
    assert np.isclose(N0, N1, atol=n_samples_tol)


def get_sample_weights(y_true, weights=None):
    """Pass `weights` tuple as `(weight_class_0, weight_class_1)`
    if you want to use custom weights."""
    N0, N1 = np.bincount(y_true)
    y0, y1 = np.unique(y_true)

    if weights:
        w0, w1 = weights
        return np.where(y_true == y1, w1, w0)

    w0 = (N0 + N1) / N0
    w1 = (N0 + N1) / N1

    return np.where(y_true == y1, w1, w0)


def perform_proba_postprocessing(
    y_proba,
    rounding=True,
    rounding_prec=4,
    boosting=True,
    boosting_coef=0.8,
    shifting=True,
    shifting_map=None,
):
    """Fancy postprocessing. Highly probable that do nothing or deteriorates."""

    def my_ceil(x, prec=rounding_prec):
        return np.true_divide(np.ceil(x * 10**prec), 10**prec)

    def my_floor(x, prec=rounding_prec):
        return np.true_divide(np.floor(x * 10**prec), 10**prec)

    proba = y_proba.copy()

    if rounding:
        proba = np.where(proba > 0.5, my_floor(proba), my_ceil(proba))

    if boosting:
        odds = boosting_coef * proba / (1 - proba)
        proba = odds / (1 + odds)

    if shifting:
        if not shifting_map:
            shifting_map = {"low": (0.01, 0.02), "high": (0.99, 0.98)}
        low_shift_from, low_shift_to = shifting_map.get("low", (0.01, 0.02))
        high_shift_from, high_shift_to = shifting_map.get("high", (0.99, 0.98))
        proba[proba < low_shift_from] = low_shift_to
        proba[proba > high_shift_from] = high_shift_to

    return proba


n_bags = 20
n_folds = 10

np.random.seed(42)
seeds = np.random.randint(0, 19937, size=n_bags)

X = train.drop("Class", axis=1)
y = train.Class

lgbm_params = {
    "max_depth": 4,
    "num_leaves": 9,
    "min_child_samples": 17,
    "n_estimators": 200,
    "learning_rate": 0.15,
    "colsample_bytree": 0.4,
    "min_split_gain": 1e-4,
    "reg_alpha": 1e-2,
    "reg_lambda": 5e-3,
}

xgb_params = {
    "max_depth": 2,
    "n_estimators": 200,
    "learning_rate": 0.4,
    "subsample": 0.6,
    "min_child_weight": 0.1,
    "max_delta_step": 0.35,
    "colsample_bytree": 0.3,
    "colsample_bylevel": 0.7,
    "min_split_loss": 1e-4,
    "reg_alpha": 2e-3,
    "reg_lambda": 6e-2,
}

svc_params = {
    "probability": True,
    "C": 3,
}
undersampling_frac = get_undersampling_fraction(y)
y_proba = np.zeros_like(y, dtype=np.float64)
classifiers = defaultdict(object)

for bag, seed in enumerate(seeds):
    skfold = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=seed)

    for fold, (train_ids, valid_ids) in enumerate(skfold.split(X, y)):
        y_train_full = y.iloc[train_ids]
        to_undersample_ids = (
            y_train_full[y_train_full == 0]
            .sample(frac=undersampling_frac, random_state=seed)
            .index.to_numpy()
        )
        # Skfold returns numbers, but `y` is a series with IDs, so we map them.
        to_undersample_ids = [y.index.get_loc(idx) for idx in to_undersample_ids]
        train_ids = np.setdiff1d(train_ids, to_undersample_ids)

        X_train, y_train = X.iloc[train_ids], y.iloc[train_ids]
        X_valid, y_valid = X.iloc[valid_ids], y.iloc[valid_ids]

        assert_balanced_learning(y_train)

        current_ensemble = make_pipeline(
            preliminary_preprocess,
            VotingClassifier(
                [
                    ("lgbm", LGBMClassifier(random_state=seed, **lgbm_params)),
                    ("xgb", XGBClassifier(random_state=seed, **xgb_params)),
                    ("svc", SVC(random_state=seed, **svc_params)),
                ],
                voting="soft",
                weights=(0.45, 0.45, 0.10),
            ),
        ).fit(X_train, y_train)

        y_proba[valid_ids] += current_ensemble.predict_proba(X_valid)[:, 1]
        classifiers[f"Voting Bag: {bag} Fold: {fold}"] = current_ensemble

y_proba_averaged = y_proba / n_bags
# Dummy protection for an empty test dataset.
if np.all(np.isclose(test.select_dtypes("number").sum(), 0)):
    test_numeric_cols = test.select_dtypes("number").columns
    test[test_numeric_cols] += 1e-9

test_ids = test.index
y_test = np.zeros_like(test_ids)

for classifier in classifiers.values():
    # Each classifier contains preprocessing, so we pass raw test dataset.
    y_test += classifier.predict_proba(test)[:, 1]

y_test_averaged = y_test / len(classifiers)

submission = pd.DataFrame(
    {
        "Id": test_ids,
        "class_0": 1 - y_test_averaged,
        "class_1": y_test_averaged,
    }
).set_index("Id")

submission.to_csv("submission.csv")


