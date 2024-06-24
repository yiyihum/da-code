
## About Dataset

### Dataset Clarification

* This dataset was crawled from the TIKI e-commerce platform, a leading online marketplace in Vietnam often compared to Amazon.
* The primary objective of this dataset is to predict the quantity sold of each product. Additional analyses and tasks can also be performed using this dataset.
* The data primarily includes popular items based on TIKI's product rankings, aiming to provide a manageable dataset without empty or inactive product IDs.

### Note

* The main language of the dataset is Vietnamese UTF-8.
* Prices are listed in Vietnamese Dong (VND). For reference, 1 USD equals approximately 24,000 VND (as of September 2023).

### Files Arrangement

* The dataset consists of multiple .csv files, each representing a root category of products on TIKI.
* All files share the same format and feature structure, including headers.

### Features Explanation

* id: Unique product ID.
* name: Product title.
* description: Product description.
* original_price: Price without any discounts.
* price: Current price, which may include discounts.
* fulfillment_type: Method of fulfillment (dropship, seller_delivery, tiki_delivery).
* brand: Brand information (OEM or registered brands).
* review_counts: Number of reviews received.
* rating_average: Average rating of the product.
* favorite_count: Number of users who have added this product to their favorites.
* pay_later: Indicates whether the product allows a purchase now pay later program.
* current_seller: Name of the seller.
* date_created: Number of days since the last update or creation date.
* number_of_images: Number of images associated with the product.
* vnd_cashback: Amount of VND cashback offered.
* has_video: Boolean indicating if the product has a video clip.
* quantity_sold: Historical total units sold of the product.
