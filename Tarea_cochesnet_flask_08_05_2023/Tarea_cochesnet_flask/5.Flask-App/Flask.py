#!/usr/bin/python3

# -----------------------------------------------------------
# VERSION v0.8
# LAST MODIFIED: 04-05-2023 12:52
# -----------------------------------------------------------

# =============================================================================
# LIBRARIES
# =============================================================================

from flask import Flask, request, render_template, url_for
from flask_cors import CORS
from os.path import realpath
import pandas as pd
import numpy as np
import pickle
import gc
from tensorflow.keras.models import load_model

# =============================================================================
# FUNCTIONS
# =============================================================================

def model_distinct_values_by_make(df:pd.DataFrame, model:str):
	return list(set(df.query('make == @model')['model'].values))

# -----------------------------------------------------------

def feature_distinct_values(df:pd.DataFrame, feature:pd.core.series.Series):
	return list(set(df[feature].values))

# -----------------------------------------------------------

def load_data(path):
	data = list()
	with open(realpath(path), 'rb') as f:
		data = pickle.load(f)
	return data

# -----------------------------------------------------------

def load_keras_model(path):
    try:
        model = load_model(realpath(path))
    except Exception as err:
        raise ValueError(f'Error whiel trying to load Keras model:\n {err}')
    return model

# -----------------------------------------------------------

def sum_up_features(df:pd.DataFrame):
    all_features = list(df)
    target = df.columns[-1]
    all_features_but_target = all_features.copy()
    all_features_but_target.remove(target)
    numeric_features = df.select_dtypes(include=[np.number]).columns.to_list()
    numeric_features.remove(target)
    categorical_features = df.select_dtypes(exclude=[np.number]).columns.to_list()    
    return all_features, target, all_features_but_target, numeric_features, categorical_features

# -----------------------------------------------------------

def transform_record(
          record:dict, 
          encoder, 
          scaler,
          all_features,
          categorical_features,
          numeric_features,
          all_features_but_target,
          target
          ):
    """
    @input: dictionary
    #output: Pandas DataFrame
    Description:
        Transforms a single record into a model-predictable data.
    Transformations done: 
        > OrdinalEncoder()
        > StandardScaler()
    """
    # Build a Pandas DataFrame from record
    df_temp = pd.DataFrame(data=record)
    df_temp = df_temp.astype({
        'doors':str,
        'year':str
    })
    # Get list of numeric and categorical features
    df_temp = df_temp.infer_objects()
    df_temp = df_temp.convert_dtypes()
    # Encode dataframe
    data_transformed = encoder.transform(df_temp[categorical_features])
    df_temp_transformed = pd.DataFrame(data=data_transformed, columns=categorical_features)
    # Build new dataframe with encoded data
    df_temp_transformed = pd.concat([df_temp_transformed, df_temp[numeric_features], df_temp[target]], axis=1)
    # Re-arrange new dataframe columns
    df_temp_transformed = df_temp_transformed[all_features]
    # Scaling data
    data_transformed_scaled = scaler.transform(df_temp_transformed[all_features_but_target])
    """
    There is a problem when building "df_temp_transformed_scaled" dataframe: 
    wrong numeric data types. 
    Python engine cannot transform Numpy array into a tensor because wrong numeric 'float' type

    # Build new dataframe with scaled data
    df_temp_transformed_scaled = pd.concat([
        pd.DataFrame(data=data_transformed_scaled, columns=ALL_FEATURES_BUT_TARGET),
        df_temp_transformed[TARGET]
    ], axis=1)
    # Re-arrange new dataframe columns
    df_temp_transformed_scaled = df_temp_transformed_scaled[ALL_FEATURES]     
    """
    # Wipe out unused variables
    del df_temp, df_temp_transformed, data_transformed
    gc.collect()

    return data_transformed_scaled

# =============================================================================
# CONFIGURATION
# =============================================================================

application = Flask(__name__, template_folder='C:\Python\project-flask\Templates', static_folder='C:\Python\project-flask\Static')
CORS(application)

# =============================================================================
# GLOBAL SCOPE
# =============================================================================
# CONSTANTS
PATH_PROJECT = 'C:/Python/project-flask/Files/'
FILENAME_DATA = 'cochesnet-data-03-05-2023-10-21.pkl'
FILENAME_MODEL = 'cochesnet-model-2016-MAE-03-05-2023-10-21.h5'
# Load project data: 
# coches.net dataframes, data transformers 
# and Keras MLP model
# 1. Pandas dataframes
data_list = load_data(PATH_PROJECT+FILENAME_DATA)
DF_TRAIN = data_list[0]
DF_VAL = data_list[1]
DF_PRED = data_list[2]
DF_CLEANED = data_list[3]
DF_CLEANED_TRANSFORMED = data_list[4]
DF_CLEANED_TRANSFORMED_SCALED = data_list[5]
# List of data used to make predictions: 
# list of Pandas DataFrame indexes. 
# Use them in 'df_cleaned' dataset
INDEX_LIST = data_list[6]
# Data normalizer and categorical encoder
SCALER = data_list[7]
ENCODER = data_list[8]    
# Load Keras model from file
MODEL = load_keras_model(PATH_PROJECT+FILENAME_MODEL)
# ------------------------------------
# Compute features summarization
ALL_FEATURES, \
TARGET, \
ALL_FEATURES_BUT_TARGET, \
NUMERIC_FEATURES, \
CATEGORICAL_FEATURES = sum_up_features(DF_CLEANED)

# =============================================================================
# LOCAL SCOPE: FLASK APPs
# =============================================================================

# -----------------------------------------------------------
# En el navegador debemos escribir en la barra de direcciones:
# http://127.0.0.1:5000/predict
@application.route('/predict')
def prediction(): 
    # response.headers.add('Access-Control-Allow-Origin')
    # Get request parameters
    color = request.args.get('color', '<no word>')
    fuelType = request.args.get('fuelType', '<no word>')
    km = request.args.get('km', '<no word>')
    make = request.args.get('make', '<no word>')
    model = request.args.get('model', '<no word>')
    province = request.args.get('province', '<no word>')
    transmissionType = request.args.get('transmissionType', '<no word>')
    year = request.args.get('year', '<no word>')
    seller_type = request.args.get('seller_type', '<no word>')
    bodyType = request.args.get('bodyType', '<no word>')
    cubicCapacity = request.args.get('cubicCapacity', '<no word>')
    doors = request.args.get('doors', '<no word>')
    hp = request.args.get('hp', '<no word>')
    # ------------------------------------
    # Set the data to predict
    record = {
        'color': [str(color)],
        'fuelType':	[str(fuelType)],
        'km': [float(km)],	
        'make':	[str(make)],
        'model': [str(model)],
        'province':	[str(province)],
        'transmissionType':	[str(transmissionType)],
        'year':	[str(year)],
        'seller_type': [str(seller_type)],
        'bodyType': [str(bodyType)],
        'cubicCapacity': [float(cubicCapacity)],
        'doors': [str(doors)],
        'hp': [float(hp)],
        'price': [0.0]
    }

    # ------------------------------------
    # Transform data
    data_transformed_scaled = transform_record(
        record,
        ENCODER,
        SCALER,
        ALL_FEATURES,
        CATEGORICAL_FEATURES,
        NUMERIC_FEATURES,
        ALL_FEATURES_BUT_TARGET,
        TARGET        
        )
    # ------------------------------------
    # Make prediction: data to predict should be as Numpy tensor like
    outcome = MODEL.predict(data_transformed_scaled)
    price_predicted = str(int(round(outcome[0][0], 0)))
    # ------------------------------------
    return render_template('predict.html', 
                        color=color,
                        fuelType=fuelType,
                        km=km,
                        make=make,
                        model=model,
                        province=province,
                        transmissionType=transmissionType,
                        year=year,
                        seller_type=seller_type,
                        bodyType=bodyType,
                        cubicCapacity=cubicCapacity,
                        doors=doors,
                        hp=hp,
                        price=price_predicted, 
                        link=url_for('home')
                        )

# -----------------------------------------------------------

@application.route('/input')
def input1():
    color = feature_distinct_values(DF_CLEANED, DF_CLEANED.color.name)
    fuelType = feature_distinct_values(DF_CLEANED, DF_CLEANED.fuelType.name)
    make = feature_distinct_values(DF_CLEANED, DF_CLEANED.make.name)
    model = feature_distinct_values(DF_CLEANED, DF_CLEANED.model.name)
    province = feature_distinct_values(DF_CLEANED, DF_CLEANED.province.name)
    transmissionType = feature_distinct_values(DF_CLEANED, DF_CLEANED.transmissionType.name)
    year = feature_distinct_values(DF_CLEANED, DF_CLEANED.year.name)
    seller_type = feature_distinct_values(DF_CLEANED, DF_CLEANED.seller_type.name)
    bodyType = feature_distinct_values(DF_CLEANED, DF_CLEANED.bodyType.name)
    doors = feature_distinct_values(DF_CLEANED, DF_CLEANED.doors.name)
    # ------------------------------------
    make.sort()
    # ------------------------------------
    return render_template('input1.html', 
                        color=color,
                        fuelType=fuelType,
                        make=make,
                        model=model,
                        province=province,
                        transmissionType=transmissionType,
                        year=year,
                        seller_type=seller_type,
                        bodyType=bodyType,
                        doors=doors, 
                        link=url_for('home')
                        )

# -----------------------------------------------------------

@application.route('/input2')
def input2():
    # ------------------------------------
    make = [request.args.get('make', '<no word>')]
    model = model_distinct_values_by_make(DF_CLEANED, make[0])
    # ------------------------------------
    color = feature_distinct_values(DF_CLEANED, DF_CLEANED.color.name)
    fuelType = feature_distinct_values(DF_CLEANED, DF_CLEANED.fuelType.name)
    # make = ...
    # model = ...
    province = feature_distinct_values(DF_CLEANED, DF_CLEANED.province.name)
    transmissionType = feature_distinct_values(DF_CLEANED, DF_CLEANED.transmissionType.name)
    year = feature_distinct_values(DF_CLEANED, DF_CLEANED.year.name)
    seller_type = feature_distinct_values(DF_CLEANED, DF_CLEANED.seller_type.name)
    bodyType = feature_distinct_values(DF_CLEANED, DF_CLEANED.bodyType.name)
    doors = feature_distinct_values(DF_CLEANED, DF_CLEANED.doors.name)
    # ------------------------------------
    # Sort list values
    color.sort()
    fuelType.sort()
    make.sort()
    model.sort()
    province.sort()
    transmissionType.sort()
    year.sort()
    seller_type.sort()
    bodyType.sort()
    doors.sort()
    # ------------------------------------
    return render_template('input2.html', 
                        color=color,
                        fuelType=fuelType,
                        make=make,
                        model=model,
                        province=province,
                        transmissionType=transmissionType,
                        year=year,
                        seller_type=seller_type,
                        bodyType=bodyType,
                        doors=doors, 
                        link=url_for('home')
                        )

# -----------------------------------------------------------

@application.route('/flask', methods=['GET'])
def flask():
    return '<p><a href="https://flask.palletsprojects.com/en/2.2.x/">Flask web site</a></p>'

# -----------------------------------------------------------

# Definimos qué respuesta devolverá el servidor
# cuando se introduzca la siguiente dirección:
#  http://127.0.0.1:5000/
@application.route('/')
def home():
    return render_template('index.html', link=url_for('input1'))

# -----------------------------------------------------------

if __name__ == '__main__':
    application.run()