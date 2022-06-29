# ML_Customer-Segmentation
This is an end-to-end Machine Learning Project from Defining problem to building an app working on the ML model.

This project is on Unsupervised Learning Problem. Here we have data of online transactions of customers and we have to categorize them.

Data is from UCI archive dataset. (https://archive.ics.uci.edu/ml/datasets/online+retail)

After EDA ,data visualization K-means algo is deployed to categorize the customers. Then classification model is deployed on this results.(Number of Clusters=3,so multivariate classification problem). After this app is created based on the classification model to predict the category of new customers.

Description of files in this repository:

1.Customer_Segmentation_Notebook.ipynb -Main Jupyter notebook for this project. Everything from data cleaning, EDA, visaulizatoin to model deployment is done in this notebook.

2.app.py -Application file for this project. App is build using Flask and basic html,css.

3.templates/index.html -HTML file for app. (I used inline-css for little styling, you can add static/styles.css file as well for styling)

4.templates/prediction.html -HTML file for app 2nd page.

