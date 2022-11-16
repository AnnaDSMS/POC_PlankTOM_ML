# POC_PlankTOM_ML

The repository containes python and jupyter notebook codes that enable:
1. extract the data from global biogeochemical ocean model PlankTOM12 at the postion and time from the real UVP5 observations;
2. prepare the data in requered format for Machine Learning methods;
3. train and test Random Forest and XGBoost regressor for the reconstruction of particulate organic carbon concentration 
at the position of real-world observations and over the global ocean;
4. estimate the role of drivers in reconstruction of particulate organic carbon concentration (feature importance);
5. reconstruct particulate organic carbon concentration over the global ocean for 2009-2013;
6. plot the statistical results.

Essential required packages:
numpy
pandas
xarray
matplotlib
matplotlib.pyplot
mpl_toolkits.basemap
pylab
scipy.io
scipy.signal
datetime import date
sklearn.ensemble
sklearn.base
xgboost
