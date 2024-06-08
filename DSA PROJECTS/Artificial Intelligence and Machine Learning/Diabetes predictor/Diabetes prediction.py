import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, KFold, learning_curve
from sklearn.metrics import confusion_matrix, accuracy_score, make_scorer
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
import xgboost as xgb
import warnings
import itertools

warnings.filterwarnings("ignore")

# Helper Functions
def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None, n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.1, color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r", label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g", label="Cross-validation score")
    plt.legend(loc="best")
    return plt

def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt), horizontalalignment="center", color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def compare_models_accuracy(X_train, y_train):
    models = [
        ('LR', LogisticRegression()),
        ('RF', RandomForestClassifier()),
        ('KNN', KNeighborsClassifier()),
        ('SVM', SVC()),
        ('LSVM', LinearSVC()),
        ('GNB', GaussianNB()),
        ('DTC', DecisionTreeClassifier()),
        ('GBC', GradientBoostingClassifier())
    ]
    
    results = []
    names = []
    for name, model in models:
        kfold = KFold(n_splits=10, random_state=7, shuffle=True)
        cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
        results.append(cv_results)
        names.append(name)
    
    fig = plt.figure()
    fig.suptitle('Algorithm Comparison: Accuracy')
    ax = fig.add_subplot(111)
    plt.boxplot(results)
    ax.set_xticklabels(names)
    ax.set_ylabel('Cross-Validation Accuracy Score')
    plt.show()

def run_decision_tree(X_train, y_train, X_test, y_test):
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    cnf_matrix = confusion_matrix(y_test, prediction)
    plot_learning_curve(model, 'Learning Curve For DecisionTreeClassifier', X_train, y_train, (0.60,1.1), cv=10)
    plt.show()
    plot_confusion_matrix(cnf_matrix, classes=['Healthy', 'Diabetes'], title='Confusion matrix')
    plt.show()
    print(f'DecisionTreeClassifier - Training set accuracy: {accuracy_score(y_test, prediction):.4f}')

def predict_diabetes(model, user_data):
    prediction = model.predict([user_data])
    confidence = model.predict_proba([user_data])
    result = "Diabetes" if prediction[0] == 1 else "Healthy"
    confidence_score = confidence[0][prediction[0]]
    print(f"Prediction: {result} with confidence: {confidence_score:.2f}")

# Load Data
data = pd.read_csv(r"C:\Users\Vincent\Documents\DSA PROJECTS\SENTIMENT\diabetes.csv")
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Data Imputation
imputer = SimpleImputer(missing_values=0, strategy='median')
X_imputed = imputer.fit_transform(X)

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=1)

# Compare Models
compare_models_accuracy(X_train, y_train)

# Train Decision Tree and Evaluate
run_decision_tree(X_train, y_train, X_test, y_test)

# Train XGBoost Classifier
xgb_model = xgb.XGBClassifier()
xgb_model.fit(X_train, y_train)
print(f'XGBoost Classifier Accuracy: {xgb_model.score(X_test, y_test):.4f}')

# Feature Importance
feature_names = X.columns
coefficients = xgb_model.feature_importances_
importance = pd.DataFrame({'Feature': feature_names, 'Importance': coefficients}).sort_values(by='Importance', ascending=False)
print('\nXGBoost Feature Importance:\n', importance)

# User Prediction
user_data = [6, 148, 72, 35, 0, 33.6, 0.627, 50]  # Example user data
predict_diabetes(xgb_model, user_data)
