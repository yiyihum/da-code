# Hints
***
## 1. Read in the avocado data
Begin by reading the avocado data from CSV file in the `data` folder - it is actually tab-delimited. This creates quite a large DataFrame, so it's a good idea to subset it to only a smaller number of relevant columns. Then read in the file for relevant category tags for avocados.


### Reading tab-delimited data
To read a tab-delimited file, such as `avocado.csv`, the filepath can be passed to `pd.read_csv()`. Set `sep = '\t'` in your `read_csv()` function, and save the DataFrame as `avocado`.


### Subsetting large DataFrame
You can create a list of the relevant columns, like so: relevant_columns = `['code', 'lc', 'product_name_en', 'quantity', 'serving_size', 'packaging_tags', 'brands', 'brands_tags', 'categories_tags', 'labels_tags', 'countries', 'countries_tags', 'origins','origins_tags']`. 

Then use `df = df[list]` to do the sub-setting.


### Reading data from TXT files for relevant category tags
You can use this code to load the relevant category tags for avocados:  

```python
with open(filepath, "r") as file:
    relevant_avocado_categories = file.read().splitlines()
    file.close()
```

## 2. Filter avocado data using relevant category tags
Each food DataFrame contains a column called categories_tags, which contains the food item category, **e.g., fruits, vegetables, fruit-based oils, etc.** 

Start by dropping rows with null values in `categories_tags`. This column is comma-separated, so you'll first need to turn it into a column of lists so that you can treat each item in the list as a separate tag. Filter this reduced DataFrame to contain only the rows where there is a relevant category tag.


### Turning a column of comma separated tags into a column of lists
You can use the syntax `df['col_name'] = df['col_name'].str.split(',')` to turn a column of comma-separated values into a column of lists.


### Dropping rows with null values in a particular column
To drop rows in a DataFrame called `df` where values are null in a particular column, you can use the syntax `df = df.dropna(subset = col_name)`


### Filtering a DataFrame based on a column of lists
To return only those rows from avocado where `categories_list` contains any of the values contained in a reference list (e.g. a list called `relevant_categories`), you can use the syntax: 

```python 
df = df[df['categories_list'].apply(lambda x: any([i for i in x if i in relevant_categories]))]
```

This applies a temporary function called lambda to the value in each row, denoted as x, and checks if any value in the list passed to `any()` is True. The list passed to any will be a list of Boolean values, checking if any value in a row is contained in the reference list called relevant_categories.

## 3. Where do most UK avocados come from?
Your avocado DataFrame should contain a column called `origins_tags`. Create a variable called `top_avocado_origin`, containing the top country where avocados in the `United Kingdom` come from.

### Filtering your DataFrame by a particular country
To return only avocados from the **United Kingdom**, you can use the syntax 

```python
avocado[(avocado['countries']=='United Kingdom')]
``` 
and store this as any variable you like.

### Counting and ordering by the unique values in the country of origin column
For a given DataFrame df, and a column called `col_name`, the syntax `df['col_name'].value_counts()` will return an ordered list of the origins of avocados. Apply this syntax to your filtered UK DataFrame to return a list of value counts of `origins_tags`.

### Get the country with the highest count
You can use `.index[0]` to get the first element of the index, so this line could look like: 
```python
avocado_origin = (avocados_uk['origins_tags'].value_counts().index[0])
```
### Strip out characters before country name
The country string you've identified up to this point could have leading characters like `"en:"` that need to be removed to just get the country name. You can do this using the syntax `country_string.lstrip("en:")`.

### Replace hyphen in country name with a space, if needed
You can use the string method `replace()` to accomplish this, using the syntax: `string = string.replace('-', ' ')`. If there is no hyphen in the string, nothing happens.

## 4. Create a user-defined function to call for each ingredient
The golden rule of programming when performing repetitive tasks such as this one is **Don't Repeat Yourself (DRY)**. Turn the code you created to analyze the avocado data and determine its top country of origin into a general function that can be used to do the same with each of the other ingredients. You should also add new steps in it to handle ties, which wasn't necessary for the avocado data.

### Creating function to call for each ingredient
Create a function called `read_and_filter_data()` which takes two arguments, a filename string pointing to this ingredient's CSV file, and relevant_categories, which is a list of strings indicating which are the relevant food categories for this ingredient. The function should return a string that is the top country of origin for this food item. This can be accomplished with the syntax: 

```python 
def function_name(filename, string_list):
``` 
and a return statement as the last line of the function.

### Performing same tasks in function as you did for the avocado process
Use the same code you did to analyze the avocado data: 
- Read the file 
- Subset to just the relevant columns
- Split categories tags into lists 
- Drop rows with null categories values 
- Filter DataFrame based on column of lists 
- Filter for data where countries equals "United Kingdom." 
- Count and order by the unique values in the country of origin column
- Get the country with the highest count
- Clean up the country string data


## 5. Read relevant categories data file and call function for each ingredient
Just as you did with the avocado data, create the variables `top_olive_oil_origin`, and `top_sourdough_origin`, using the relevant category data and analyzing country origin data. To determine these last two origin variables, you'll call the function you've created.