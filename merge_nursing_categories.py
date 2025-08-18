import pandas as pd
import json
from collections import defaultdict

print('=== MERGING NURSING CATEGORIES ===')
print('Combining Licensed Practical Nurse with Registered Nurse')

# Load the original CSV data
df = pd.read_csv('key_categories_job_analysis.csv')
print(f'Loaded {len(df):,} original records')

# Check current nursing categories
nursing_counts = df[df['job_category'].str.contains('Nurse', case=False)]['job_category'].value_counts()
print('\nCurrent nursing categories:')
for category, count in nursing_counts.items():
    print(f'  {category}: {count:,} records')

# Merge Licensed Practical Nurse into Registered Nurse
df.loc[df['job_category'] == 'Licensed Practical Nurse', 'job_category'] = 'Registered Nurse'

# Verify the merge
nursing_counts_after = df[df['job_category'].str.contains('Nurse', case=False)]['job_category'].value_counts()
print('\nAfter merging:')
for category, count in nursing_counts_after.items():
    print(f'  {category}: {count:,} records')

# Save the updated CSV
df.to_csv('key_categories_job_analysis_merged.csv', index=False)
print(f'\n✅ Saved merged data to key_categories_job_analysis_merged.csv')

# Now regenerate the statistical analysis with merged categories
print('\n=== REGENERATING STATISTICAL ANALYSIS WITH MERGED NURSING ===')

# Statistical analysis by category
category_stats = {}
for category in df['job_category'].unique():
    category_data = df[df['job_category'] == category]
    
    category_stats[category] = {
        'avg_jobs_per_listing': round(category_data['job_count'].mean(), 1),
        'avg_jobs_per_city': round(category_data.groupby('cleaned_city')['job_count'].mean().mean(), 1),
        'min_jobs': int(category_data['job_count'].min()),
        'max_jobs': int(category_data['job_count'].max()),
        'listings_count': len(category_data),
        'cities_count': category_data['cleaned_city'].nunique(),
        'states_count': category_data['cleaned_state'].nunique()
    }

# State analysis with merged nursing
state_stats = {}
for state in df['cleaned_state'].unique():
    state_data = df[df['cleaned_state'] == state]
    
    # Category breakdown for this state
    state_categories = {}
    for category in state_data['job_category'].unique():
        cat_data = state_data[state_data['job_category'] == category]
        state_categories[category] = {
            'avg_jobs_per_listing': round(cat_data['job_count'].mean(), 1),
            'avg_jobs_per_city': round(cat_data.groupby('cleaned_city')['job_count'].mean().mean(), 1),
            'listings_count': len(cat_data),
            'cities_count': cat_data['cleaned_city'].nunique()
        }
    
    # Sort categories by avg_jobs_per_listing to get top 3
    sorted_categories = sorted(state_categories.items(), 
                             key=lambda x: x[1]['avg_jobs_per_listing'], 
                             reverse=True)
    
    top_3_categories = []
    for i, (category, data) in enumerate(sorted_categories[:3], 1):
        top_3_categories.append({
            'rank': i,
            'category': category,
            'avg_jobs_per_listing': data['avg_jobs_per_listing'],
            'avg_jobs_per_city': data['avg_jobs_per_city'],
            'cities_count': data['cities_count']
        })
    
    state_stats[state] = {
        'categories': state_categories,
        'top_3_categories': top_3_categories,
        'total_listings': len(state_data),
        'total_cities': state_data['cleaned_city'].nunique(),
        'total_categories': len(state_categories),
        'total_titles': len(state_data)  # Total job postings/titles
    }

print('\n=== UPDATED STATE STATISTICS WITH MERGED NURSING ===')
print('State\tTop 3 Categories\tTotal Cities\tTotal Categories\tTotal Titles')
print('-' * 120)

for state_code in sorted(state_stats.keys()):
    state_data = state_stats[state_code]
    top_3 = state_data['top_3_categories']
    
    top_3_str = ', '.join([f"{cat['category']} ({cat['avg_jobs_per_listing']})" for cat in top_3])
    
    print(f"{state_code}\t{state_data['total_cities']}\t{state_data['total_categories']}\t{state_data['total_titles']}")
    print(f"\tTop 3: {top_3_str}")

# Load existing metro concentration data from previous analysis
try:
    with open('statistical_job_analysis.json', 'r') as f:
        existing_analysis = json.load(f)
    
    # Get metro concentration data
    metro_concentration = existing_analysis.get('enhanced_analysis', {}).get('state_metro_concentration', {})
    
    print('\n=== COMPLETE STATE STATISTICS SUMMARY TABLE ===')
    print('State\tCategories\tCities\tTitles\tTop Category\tAvg/Listing\tConcentration\tDetails')
    print('-' * 150)
    
    for state_code in sorted(state_stats.keys()):
        state_data = state_stats[state_code]
        top_3 = state_data['top_3_categories']
        
        # Get concentration percentage
        concentration = 'N/A'
        if state_code in metro_concentration:
            concentration = f"{metro_concentration[state_code]['state_concentration_percentage']}%"
        
        # Format top 3 categories
        top_3_formatted = []
        for i, cat in enumerate(top_3, 1):
            top_3_formatted.append(f"{i}. {cat['category']} ({cat['avg_jobs_per_listing']})")
        
        top_category_str = top_3_formatted[0] if top_3_formatted else 'N/A'
        
        print(f"{state_code}\t{state_data['total_cities']}\t{state_data['total_categories']} categories\t{state_data['total_titles']} titles")
        print(f"\t{concentration}\t{', '.join(top_3_formatted)}")
        print()

except FileNotFoundError:
    print('Note: Metro concentration data not found, showing basic state stats only')

# Create updated analysis JSON
updated_analysis = {
    'methodology': {
        'note': 'Licensed Practical Nurse merged with Registered Nurse - same job category',
        'merge_date': '2025-08-13',
        'approach': 'Statistical averages only - no misleading totals due to overlapping listings'
    },
    'category_overview': category_stats,
    'state_statistics': state_stats,
    'total_categories': len(category_stats),
    'total_states': len(state_stats),
    'total_records': len(df)
}

# If previous analysis exists, preserve other sections
if 'existing_analysis' in locals():
    # Preserve other analysis sections
    for key, value in existing_analysis.items():
        if key not in ['category_overview', 'state_statistics']:
            updated_analysis[key] = value

# Save updated analysis
with open('statistical_job_analysis_merged.json', 'w') as f:
    json.dump(updated_analysis, f, indent=2)

print(f'\n✅ Updated statistical analysis saved to statistical_job_analysis_merged.json')
print(f'📊 Categories reduced from 12 to {len(category_stats)} after nursing merge')
print(f'🏥 Nursing categories now combined under "Registered Nurse"')