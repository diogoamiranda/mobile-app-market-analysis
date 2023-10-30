import pandas as pd
import matplotlib.pyplot as plt
import os

from db_connection import connect_to_db

def generate_chart_total_apps_by_category():
    # Load data from database
    collection = db["google_app_infos"]

    # Fetch all data from the collection and transforms it into a DataFrame
    data = pd.DataFrame(collection.find({}))

    # Aggregation of data (counting the number of apps/records per category)
    data = data['category'].value_counts()

    # Create a chart with bars
    plt.figure(figsize=(11, 7))
    data.plot(kind='bar', width=0.7)
    plt.title('Distribution of the total apps by category')
    plt.xlabel('Category')
    plt.ylabel('Counting')
    # Adjust the subplot parameters to provide extra space for x-axis labels
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.4)
    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=80)

    filename =  os.path.join(save_charts_directory, 'total_apps_by_category.png')
    # store chart as image
    plt.savefig(filename)

    # show chart
    # plt.show()

def generate_chart_total_apps_by_category_with_pricing_distribution():
    # Load data from database
    collection = db["google_app_infos"]

    # Fetch all the data from the collection and transforms it into a DataFrame
    data = pd.DataFrame(collection.find({}))
    # Count the categories that are free or not.
    grouped_data = data.groupby(['category', 'free']).size().unstack(fill_value=0)

    # Calculate the total sum of apps for each category
    grouped_data['Total'] = grouped_data.sum(axis=1)
    # Sort the data by total number of apps in descending order
    grouped_data = grouped_data.sort_values(by='Total', ascending=False)
    # Remove the 'Total' column so it doesn't appear in the visualisation
    grouped_data = grouped_data.drop(columns='Total')

    top_10_categories = grouped_data.head(10)
    bottom_10_categories = grouped_data.tail(10)

    # Create a chart with bars
    plt.figure(figsize=(11, 7))
    ax = top_10_categories.plot(kind='bar', stacked=True)
    plt.title('Top 10 categories with the most apps (Free vs Paid)')
    plt.ylabel('Counting')
    # Adjust the subplot parameters to provide extra space for x-axis labels
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.4)

    # Customise x-axis labels based on categories
    ax.set_xticklabels(top_10_categories.index, rotation=70)

    # Add a legend to the chart
    plt.legend(title='Free vs Paid', labels=['Free', 'Paid'])

    filename =  os.path.join(save_charts_directory,'top_10_total_apps_by_category_with_pricing_distribution.png')
    # store chart as image
    plt.savefig(filename)

    ##################
    # Create a chart with bars
    plt.figure(figsize=(11, 7))
    ax = bottom_10_categories.plot(kind='bar', stacked=True)
    plt.title('Top 10 categories with the fewest apps (Free vs Paid)')
    plt.xlabel('Category')
    plt.ylabel('Counting')
    # Adjust the subplot parameters to provide extra space for X-axis labels
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.4)

    # Customise x-axis labels based on categories
    ax.set_xticklabels(bottom_10_categories.index, rotation=70)

    # Add a legend to the chart
    plt.legend(title='Free vs Paid', labels=['Free', 'Paid'])

    filename = os.path.join(save_charts_directory,'bottom_10_total_apps_by_category_with_pricing_distribution.png')
    # store chart as image
    plt.savefig(filename)

    # show chart
    # plt.show()

######
db = connect_to_db()

if db is not None:
    save_charts_directory = os.path.realpath("charts")

    generate_chart_total_apps_by_category()
    generate_chart_total_apps_by_category_with_pricing_distribution()

