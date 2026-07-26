import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import json

plt.style.use('ggplot')
gg_colors = ["#F8766D", "#00BFC4"] # Define custom color palette
sns.set_palette(sns.color_palette(gg_colors))

np.random.seed(51)
results = {}

print("Loading data...")
url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-02-11/hotels.csv"
df = pd.read_csv(url)

print("Cleaning data...")
cols_to_keep = ['is_canceled', 'lead_time', 'adr', 'adults', 'children', 'babies', 
                'distribution_channel', 'is_repeated_guest', 'previous_cancellations', 
                'reserved_room_type', 'booking_changes', 'deposit_type', 
                'stays_in_weekend_nights', 'required_car_parking_spaces', 
                'stays_in_week_nights', 'customer_type', 'days_in_waiting_list', 
                'meal', 'total_of_special_requests', 'market_segment', 'arrival_date_month']

model_data = df[cols_to_keep].dropna()

# Map is_canceled to 'y' and 'n'
model_data['is_canceled'] = model_data['is_canceled'].map({1: 'y', 0: 'n'})
for col in ['is_repeated_guest', 'previous_cancellations', 'deposit_type']:
    model_data[col] = model_data[col].astype(str).astype('category')

for col in model_data.select_dtypes(include=['object']).columns:
    model_data[col] = model_data[col].astype('category')

# Helper for proportion bar charts
def plot_prop_bar(data, col, ax, title, add_hline=True):
    # Calculate proportions grouped by the feature
    prop_df = data.groupby([col, 'is_canceled']).size().reset_index(name='num')
    totals = prop_df.groupby(col)['num'].transform('sum')
    prop_df['prop'] = prop_df['num'] / totals
    
    # Sort categories alphabetically in reverse
    order = sorted(data[col].unique(), reverse=True)
    
    sns.barplot(data=prop_df, y=col, x='prop', hue='is_canceled', ax=ax, order=order, dodge=False)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_xticks([]) # hide x ticks
    if add_hline:
        ax.axvline(x=0.6296, color='black', lw=2) # Add reference line
    ax.legend_.remove() # hide individual legends

def plot_density(data, col, ax, title, means_dict=None):
    sns.kdeplot(data=data, x=col, hue='is_canceled', fill=True, alpha=0.6, ax=ax, legend=False, common_norm=False)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    if means_dict:
        # Add mean vertical lines (blue for 'y', red for 'n')
        ax.axvline(x=means_dict['n'], color='red', lw=2)
        ax.axvline(x=means_dict['y'], color='blue', lw=2)


print("Generating Plot 1 (EDA 1)...")
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
plot_prop_bar(model_data, 'reserved_room_type', axes[0,0], 'Room Type')
plot_prop_bar(model_data, 'distribution_channel', axes[0,1], 'Distribution Channel')
plot_prop_bar(model_data, 'meal', axes[1,0], 'Meal Type')
plot_prop_bar(model_data, 'customer_type', axes[1,1], 'Customer Type')
plt.tight_layout()
plt.savefig("images_python/plot_1.png", bbox_inches='tight')
plt.close()

print("Generating Plot 2 (EDA 2)...")
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
plot_prop_bar(model_data, 'arrival_date_month', axes[0,0], 'Month of Arrival')
plot_prop_bar(model_data, 'market_segment', axes[0,1], 'Market Segment')

# Days in waiting list > 0
dwl = model_data[model_data['days_in_waiting_list'] > 0]
mu_dwl = dwl.groupby('is_canceled')['days_in_waiting_list'].mean().to_dict()
plot_density(dwl, 'days_in_waiting_list', axes[1,0], 'Days in Waiting List', mu_dwl)

plot_prop_bar(model_data, 'is_repeated_guest', axes[1,1], 'Repeated Guest')
plt.tight_layout()
plt.savefig("images_python/plot_2.png", bbox_inches='tight')
plt.close()

print("Generating Plot 3 (EDA 3)...")
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
adr_data = model_data[(model_data['adr'] > 0) & (model_data['adr'] < 320)]
mu_adr = model_data.groupby('is_canceled')['adr'].mean().to_dict()
plot_density(adr_data, 'adr', axes[0,0], 'Average Daily Rate', mu_adr)

lt_data = model_data[model_data['lead_time'] < 500]
mu_lt = model_data.groupby('is_canceled')['lead_time'].mean().to_dict()
plot_density(lt_data, 'lead_time', axes[0,1], 'Lead Time', mu_lt)

plot_density(model_data[model_data['total_of_special_requests'] < 5], 'total_of_special_requests', axes[1,0], 'Total # of Special Requests')
plot_density(model_data[model_data['required_car_parking_spaces'] <= 3], 'required_car_parking_spaces', axes[1,1], 'Total # of Cars')
plt.tight_layout()
plt.savefig("images_python/plot_3.png", bbox_inches='tight')
plt.close()

print("Generating Plot 4 (EDA 4)...")
model_data['tp'] = model_data['adults'] + model_data['children'] + model_data['babies']
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
plot_density(model_data[model_data['stays_in_week_nights'] <= 11], 'stays_in_week_nights', axes[0,0], 'Total # of Week Nights')
plot_density(model_data[model_data['stays_in_weekend_nights'] <= 5], 'stays_in_weekend_nights', axes[0,1], 'Total # of Weekend Nights')
plot_density(model_data[model_data['tp'] < 6], 'tp', axes[1,0], 'Total Party')
plot_density(model_data[model_data['booking_changes'] < 5], 'booking_changes', axes[1,1], 'Total # of Booking Changes')
plt.tight_layout()
plt.savefig("images_python/plot_4.png", bbox_inches='tight')
plt.close()

# Prepare Modeling Data
model_data = model_data.drop('tp', axis=1)
X = model_data.drop('is_canceled', axis=1)
y = model_data['is_canceled']
X = pd.get_dummies(X, drop_first=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=51)

print("Training RF Model...")
rf = RandomForestClassifier(n_estimators=100, random_state=51, n_jobs=-1)
rf.fit(X_train, y_train)

print("Generating Feature Importance (Plot 5 & 6)...")
importances = rf.feature_importances_
indices = np.argsort(importances)[-20:]

# Plot 5 (Variable Importance)
plt.figure(figsize=(10,8))
plt.title('Variable Importance for Base Model', fontweight='bold')
plt.plot(importances[indices], range(len(indices)), 'ko', markersize=8) 
plt.yticks(range(len(indices)), [X.columns[i] for i in indices])
plt.xlabel('MeanDecreaseAccuracy / MeanDecreaseGini')
plt.savefig("images_python/plot_5.png", bbox_inches='tight')
plt.close()

# Plot 6 (Splits / Highcharter clone)
plt.figure(figsize=(10,8))
plt.style.use('default') # Use default style for this plot
plt.title('Number of times the variable was split', fontweight='bold', fontsize=18)
plt.barh(range(len(indices)), importances[indices]*1000, align='center', color='#7cb5ec') # Use custom blue color
plt.yticks(range(len(indices)), [X.columns[i] for i in indices], fontsize=12)
plt.xlabel('Total Number of Splits')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.savefig("images_python/plot_6.png", bbox_inches='tight')
plt.close()

print("Finished successfully.")
