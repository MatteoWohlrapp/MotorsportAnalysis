import logging
from io import BytesIO

import pandas as pd
import plotly.express as px
from flask import Flask, render_template_string
import typing as t
import os
from google.cloud import storage

bucket_name = 'motorsportanalysis.appspot.com'
file_path = '20130810_01_01_01_grandsport.csv' #hardcoded file name in this case as working with google cloud storage is not that easy

def on_cloud():
    return 'GAE_ENV' in os.environ


def load_df_from_gcs():
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_path)

    file_content = blob.download_as_bytes()  # Downloads the file content as bytes
    buffer = BytesIO(file_content)  # Creates a file-like buffer
    header = pd.read_csv(buffer, encoding='unicode_escape', skiprows=10, nrows=1, header=None)

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_path)

    file_content = blob.download_as_bytes()  # Downloads the file content as bytes
    buffer = BytesIO(file_content)  # Creates a file-like buffer
    df = pd.read_csv(buffer, encoding='unicode_escape', skiprows=12, header=None, names=header.iloc[0])

    return df


def load_df_from_csv():
    data_dir = os.path.join(os.path.curdir, 'data')
    available_files = os.listdir(data_dir)
    for file_name in available_files:
        if '.csv' in file_name:
            file = os.path.join(data_dir, file_name)
            break
    header = pd.read_csv(file, encoding='unicode_escape', skiprows=10, nrows=1, header=None)
    df = pd.read_csv(file, encoding='unicode_escape', skiprows=12, header=None, names=header.iloc[0])
    return df


def load_data():
    if on_cloud():
        return load_df_from_gcs()
    else:
        return load_df_from_csv()


class MotorsportApplication(Flask):
    def __init__(
            self,
            import_name: str,
            static_url_path: t.Optional[str] = None,
            static_folder: t.Optional[t.Union[str, os.PathLike]] = "static",
            static_host: t.Optional[str] = None,
            host_matching: bool = False,
            subdomain_matching: bool = False,
            template_folder: t.Optional[t.Union[str, os.PathLike]] = "templates",
            instance_path: t.Optional[str] = None,
            instance_relative_config: bool = False,
            root_path: t.Optional[str] = None,
    ):
        super().__init__(import_name, static_url_path, static_folder, static_host, host_matching, subdomain_matching,
                         template_folder, instance_path, instance_relative_config, root_path)
        self.df = load_data()


app = MotorsportApplication(__name__)


@app.route('/')
def index():
    x = app.df['time'].tolist()
    y = app.df['handwheelAngle'].tolist()
    df = pd.DataFrame({'s': x, 'throttle': y})
    fig = px.line(df, x='s', y='throttle', title='Throttle Analysis')

    plot_div = fig.to_html(full_html=False)

    return render_template_string("""
<!doctype html>
<html>
    <head>
        <title>Motorsport analysis</title>
    </head>
    <body>
        {{ plot_div|safe }}
    </body>
</html>
""", plot_div=plot_div)


if __name__ == '__main__':
    app.run(debug=True)
