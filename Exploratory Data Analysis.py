import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

plt.style.use(
    'ggplot')  # sets the style of the plots to mimic the aesthetics of the "ggplot" style from the R programming language's ggplot2 library.
pd.options.display.max_columns = 200

df = pd.read_csv('/Users/eftropioskaragkiozis/Desktop/coaster_db.csv')

# Step 1. Data Understanding
# Dataframe shape, head and tail, dtypes, describe

print(df.shape)  # df.shape shoulde actually work as well the same way as print(df.shape)

print(df.head)  # Default = the first 5 rows

print(df.columns)

print(df.dtypes)

print(df.describe())  # Good way to get statistics about the numeric data

# Step 2. Data Preperation
# Dropping irrelevant columns and rows, Identifying duplicated columns, Renaming columns, Feature creation

df = df[['coaster_name',  # 'Length', 'Speed',
         'Location', 'Status',  # 'Opening date',
         # 'Type',
         # 'Manufacturer', 'Height restriction', 'Model', 'Height',
         # 'Inversions', 'Lift/launch system', 'Cost', 'Trains', 'Park section',
         # 'Duration', 'Capacity', 'G-force', 'Designer', 'Max vertical angle',
         # 'Drop', 'Soft opening date', 'Fast Lane available', 'Replaced',
         # 'Track layout', 'Fastrack available', 'Soft opening date.1',
         # 'Closing date',
         'Opened',  # 'Replaced by', 'Website',
         # 'Flash Pass Available', 'Must transfer from wheelchair', 'Theme',
         # 'Single rider line available', 'Restraint Style',
         # 'Flash Pass available', 'Acceleration', 'Restraints', 'Name',
         'year_introduced', 'latitude', 'longitude', 'Type_Main',
         'opening_date_clean',  # 'speed1', 'speed2', 'speed1_value', 'speed1_unit',
         'speed_mph',  # 'height_value', 'height_unit',
         'height_ft',
         'Inversions_clean',
         'Gforce_clean']].copy()  # After the df.columns where i got to see all the columns of the dataset, I can now keep only those that I need. So I assign the df with those columns to a new varriable named new_df
print(df)

print(df.dtypes)

# Another way of doing the same is the .drop eg, df.drop(['Opening date'], axis=1). The axis info is needed so that it knows it is a column, not a row.

df['opening_date_clean'] = pd.to_datetime(
    df['opening_date_clean'])  # Cause it was initialy an object but made no sence. So I force it to become a date

# print(pd.to_datetime(df['opening_date_clean']))

# Rename the columns

print(df.columns)

df = df.rename(columns={'coaster_name': 'Coaster_Name',
                        'year_introduced': 'Year_Introduced',
                        'opening_date_clean': 'Opening_Date',
                        'speed_mph': 'Speed_mph',
                        'height_ft': 'Height_ft',
                        'Inversions_clean': 'Inversions',
                        'Gforce_clean': 'Gforce'})

print(df.columns)

# Check missing values

print(df.isna())
# or
print(df.isna().sum())  # to get an overview of the sum of missing values per column

# Find duplicated data

print(df.duplicated())

print(df.loc[df.duplicated()])  # to locate the duplicates

print(df.duplicated(subset=['Coaster_Name']))  # if I want to check for duplicates in a specific subset/column

print(df.loc[df.duplicated(subset=['Coaster_Name'])].head(
    5))  # it will give every duplicated row(the second time it appears)

# checking an example of a duplicated value by using the query command
print(df.query('Coaster_Name=="Crystal Beach Cyclone"'))  # the only difference is the Year_Introduced

print(~df.duplicated(subset=['Coaster_Name', 'Location',
                             'Opening_Date']))  # by using ~ we get the columns that are not the duplicate, so that means only the first row and not the duplicate of it.

df = df.loc[~df.duplicated(subset=['Coaster_Name', 'Location', 'Opening_Date'])] \
    .reset_index(drop=True)  # to locate them.
# But since we are now dropping rows, the index will be false, since it won't change automatically.
# So by adding the .reset_index() we get the index right again. The \ added before .reset_index is just the line continuantion character, to show that the code continues to the next line
# the reset_index addes a new column named index. We don't want it, so we add the (drop=True)

print(df)
print(df.shape)

# Step 3. Feature Understanding   (Univariate Analysis)
# Plotting Feature Distributions (Histogram, KDE, Boxplot)

print(df['Year_Introduced'].value_counts())  # the .value_counts is very powerfull and very ofted used
# It counts how many occurences we have per Year_Introduced. And gives the results in descending order of the value counts.

# make it now into a plot

ax = df['Year_Introduced'].value_counts() \
    .head(10) \
    .plot(kind='bar', title='Top 10 Years Coasters Introduced')

ax.set_xlabel('Year Introduced')
ax.set_ylabel('Count')
# we shaved it as a matplotlib diagram ax. And now we can add more info. Eg xlabel

# plt.show()  #!! in order to Display the plot. print() doesn't work here

# Get an idea of the distribution in a column. A good practise if examining one column seperately

# ax = df['Speed_mph'].plot(kind='hist', bins=20, title='Coaster Speed (mph)')

# ax.set_xlabel('Speed (mph)')

ax = df['Speed_mph'].plot(kind='kde', title='Coaster Speed (mph)')

ax.set_xlabel('Speed (mph)')

plt.show()

# Till now checked each feature seperately and some distributions and other characteristics of a given column in the dataset.

# Important though: How do different features relate to each other.

# Step 4. Feature Relationships
# Scatterplot, Heatmap Correlation, Pairplot, Groupby comparisons

df.plot(kind='scatter',
        x='Speed_mph',
        y='Height_ft',
        title='Coaster Speed vs Height')
plt.show()

# With seaborn imported as sns we can do more advanced analysis

sns.scatterplot(x='Speed_mph',
                # sns.scatterplot(). If I go in the parenthesis and press swift/tab, I get a list of what varriables the plot can work with eg x,y, data, hue etc
                y='Height_ft',
                data=df)  # This one is same as with the matplotlib scatterplot.
# But if we add the hue and set it to Year_Introduced, we have the color of the dots on the scatterplot changing according to the year. And we get a legend explaining the colours

sns.scatterplot(x='Speed_mph',
                y='Height_ft',
                hue='Year_Introduced',
                data=df)
plt.show()

# How to compare more than two features. With seaborn
sns.pairplot(df, vars=['Year_Introduced', 'Speed_mph', 'Height_ft', 'Inversions', 'Gforce'],
             hue='Type_Main')  # Pairplots are a great tool for comparisons
plt.show()

# Checking correlations

df_corr = df[['Year_Introduced', 'Speed_mph', 'Height_ft', 'Inversions',
              'Gforce']].dropna().corr()  # Only numeric values! .dropna() = leaves all the null values and .corr() gives a correlation
print(df_corr)
# .corr() function-> gives a result of the correlation between features eg Speed_mph and Height_ft etc
# The same results we can present in a heatmap with seaborn.

sns.heatmap(df_corr, annot=True)
plt.show()

# Step 5. Ask a Question about the data
# Eg. what are the locations with the fastest roller coasters (with minimum of 10 coasters)?
print(df['Location'].value_counts()
      )

ax = df.query('Location != "Other"') \
    .groupby('Location')['Speed_mph'] \
    .agg(['mean', 'count']) \
    .query('count >= 10') \
    .sort_values('mean')['mean'] \
    .plot(kind='barh', figsize=(12, 5),
          title='Average Coaster Speed by Location')  # To filter the list and get only the rest
ax.set_xlabel('Average Coaster Speed')
plt.show()
# .agg() = Aggregate by location and get the mean value
