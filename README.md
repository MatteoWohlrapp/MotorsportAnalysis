### Overview 
There are two parts to this repository: <br>

1. Analysis
2. Deployment

Before you run, add one csv file from the data set https://purl.stanford.edu/tt103jr6546 into a 'data' folder which you have to create at the root of the repository. 

### Analysis 
To analyze the data locally, you can eiter run 'MotorsportAnalysis.ipynb' or 'MotorsportAnalysis.py'. 

'MotorsportAnalysis.ipynbNB' is a jupyter notebook, in there you can find a lot of information and my thoughts on it. <br>
However, this is relatively slow as the amouts of data is huge, so if you just want to see the plots, I would suggest to run Motorsport_Analysis.py as it is much faster and has the same funcionality. The plots will be shown in the browser, and in a separate window from matplotlib. 

### Deployment
The other files: 'app.yaml', 'main.py' and 'requirements.txt' are for deployment to Google Cloud. Running main.py will open a browser window connected to local host and show one plot. This is just to underline how to combine these plots with Flask and create html templates. <br> 
As stated in the .pdf document, this did not make it on the cloud because of memory limitations I was not able to overcome. 

