## About Dataset

### **Context**

Traditionally speaking, finding the right home is often a long, stressful, and tedious process. But, online system and e-real state makes it easier by giving customer details and unique insights on the homes they’re interested in. Real Estate systems have been expanded recently, generally each company built its own website to advertise its products and perform online buying and selling. Therefore, consumers can get lost in searching among those all websites and it became more conflict and time consuming. For that reason, building Real Estate Recommender System to be used as base for many user of one product became more desirable.

Also the recommendation systems here assist the user to filter the information according to users’ needs because the database for system can be huge and it will take time to get the information.

### Content

The dataset has been generated by one of these real state systems and the system logs is a mirror of online rental process. That means that from user subscription to visit and rent there are several steps which each step has a record in user-activity.csv file. Also property.csv will get more details about the items. user-activity collaboration is main data for behavioral analysis and building recommendation algorithms.** **

### Starter Kernels

* [Clustering](https://www.kaggle.com/arashnic/eda-and-clustering)
* [Data Understanding and EDA](https://www.kaggle.com/arashnic/data-understanding-eda)

### Inspiration

* You can find property data a good source for segmentation and clustering. How do you cluster the properties ? How feature engineering will help and which preprocessing step should be followed?
* user-activity data is the main data source for implementing recommendation algorithms.:
  1. What are similar users? Similar properties?
  2. We have to present a mechanism for rating the properties (by customer,/customer interest) by user if we plan to use model based CF e.g. Matrix** **
     Factorization algorithms for better results. How we can deliver this rating by data in hands e.g. event logs. Do the outputs from clustering help?
  3. Is the data quality enough to implement collaborative filtering algorithms or other recommendation methods ?** **
  4. How do you validate your recommendation models?