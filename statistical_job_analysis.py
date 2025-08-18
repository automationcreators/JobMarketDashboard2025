import pandas as pd
import numpy as np
from collections import defaultdict
import json

print('=== STATISTICAL JOB ANALYSIS (AVERAGES ONLY) ===')
print('Focusing on avg/min/max per city, state, metro, and airport - NO TOTALS')

# Load the key categories data
df = pd.read_csv('key_categories_job_analysis.csv')
print(f'Loaded {len(df):,} records')

# Verify richmond hill example
richmond_hill = df[df['cleaned_city'] == 'Richmond Hill']
if len(richmond_hill) > 0:
    print(f'\\nRichmond Hill example verification:')
    print(f'Records found: {len(richmond_hill)}')
    for category in richmond_hill['job_category'].unique():
        cat_data = richmond_hill[richmond_hill['job_category'] == category]
        if len(cat_data) > 0:
            print(f'  {category}: {len(cat_data)} listings, avg {cat_data["job_count"].mean():.1f} jobs')

print(f'\\nUnique job categories: {sorted(df["job_category"].unique())}')

# Create comprehensive statistical analysis
print('\\n=== BUILDING STATISTICAL ANALYSIS ===')

# 1. Category-City-Level Statistics (keep existing detailed breakdown)
category_city_stats = {}

for category in df['job_category'].unique():
    if pd.isna(category):
        continue
        
    category_data = df[df['job_category'] == category]
    category_city_stats[category] = {}
    
    # Group by city and calculate statistics
    city_stats = category_data.groupby('cleaned_city')['job_count'].agg([
        'count',  # number of listings
        'mean',   # average job count per listing
        'median', # median job count
        'min',    # minimum job count
        'max',    # maximum job count
        'std'     # standard deviation
    ]).round(1)
    
    city_stats = city_stats[city_stats['count'] >= 1]
    
    for city, stats in city_stats.iterrows():
        if pd.notna(city):
            city_state = category_data[category_data['cleaned_city'] == city]['cleaned_state'].iloc[0]
            city_metro = category_data[category_data['cleaned_city'] == city]['closest_metro'].iloc[0]
            city_airport = category_data[category_data['cleaned_city'] == city]['closest_airport'].iloc[0]
            metro_distance = category_data[category_data['cleaned_city'] == city]['metro_distance_band'].iloc[0]
            
            category_city_stats[category][city] = {
                'state': city_state,
                'closest_metro': city_metro,
                'closest_airport': city_airport,
                'metro_distance_band': metro_distance,
                'listings_count': int(stats['count']),
                'avg_jobs_per_listing': stats['mean'],
                'median_jobs': stats['median'],
                'min_jobs': stats['min'],
                'max_jobs': stats['max'],
                'std_jobs': stats['std'] if pd.notna(stats['std']) else 0
            }

print(f'Created city-level statistics for {len(category_city_stats)} job categories')

# 2. State-Level Statistics (averages only)
state_statistics = {}
states = ['AZ', 'FL', 'TX', 'NV', 'TN', 'GA', 'NC']

for state in states:
    state_data = df[df['cleaned_state'] == state]
    if len(state_data) == 0:
        continue
    
    state_categories = {}
    
    for category in state_data['job_category'].unique():
        if pd.isna(category):
            continue
            
        category_state_data = state_data[state_data['job_category'] == category]
        
        # Calculate statistics per listing (not totals)
        job_stats = category_state_data['job_count'].agg(['count', 'mean', 'median', 'min', 'max', 'std'])
        unique_cities = category_state_data['cleaned_city'].nunique()
        unique_titles = category_state_data['extracted_job_title'].nunique()
        
        # Calculate average per city (not total)
        city_averages = category_state_data.groupby('cleaned_city')['job_count'].mean()
        
        state_categories[category] = {
            'listings_count': int(job_stats['count']),
            'cities_count': unique_cities,
            'titles_count': unique_titles,
            'avg_jobs_per_listing': round(job_stats['mean'], 1),
            'avg_jobs_per_city': round(city_averages.mean(), 1),
            'median_jobs_per_listing': round(job_stats['median'], 1),
            'min_jobs_per_listing': int(job_stats['min']),
            'max_jobs_per_listing': int(job_stats['max']),
            'std_jobs_per_listing': round(job_stats['std'], 1) if pd.notna(job_stats['std']) else 0
        }
    
    state_statistics[state] = {
        'total_listings': len(state_data),
        'total_categories': len(state_categories),
        'total_cities': state_data['cleaned_city'].nunique(),
        'total_titles': state_data['extracted_job_title'].nunique(),
        'categories': state_categories
    }

# 3. Metro-Level Statistics (25-mile and 50-mile groupings)
print('\\n=== BUILDING METRO-LEVEL STATISTICS ===')

metro_statistics = {}

# Group by metro areas
for metro in df['closest_metro'].dropna().unique():
    metro_data = df[df['closest_metro'] == metro]
    
    metro_categories = {}
    
    for category in metro_data['job_category'].unique():
        if pd.isna(category):
            continue
            
        category_metro_data = metro_data[metro_data['job_category'] == category]
        
        # Statistics for this category in this metro
        job_stats = category_metro_data['job_count'].agg(['count', 'mean', 'median', 'min', 'max', 'std'])
        unique_cities = category_metro_data['cleaned_city'].nunique()
        
        # Break down by distance bands
        within_25 = category_metro_data[category_metro_data['metro_distance_band'] == '0-25 miles']
        within_50 = category_metro_data[category_metro_data['metro_distance_band'].isin(['0-25 miles', '25-50 miles'])]
        
        metro_categories[category] = {
            'all_listings': int(job_stats['count']),
            'cities_count': unique_cities,
            'avg_jobs_per_listing': round(job_stats['mean'], 1),
            'median_jobs': round(job_stats['median'], 1),
            'min_jobs': int(job_stats['min']),
            'max_jobs': int(job_stats['max']),
            'within_25_miles': {
                'listings': len(within_25),
                'avg_jobs': round(within_25['job_count'].mean(), 1) if len(within_25) > 0 else 0,
                'cities': within_25['cleaned_city'].nunique() if len(within_25) > 0 else 0
            },
            'within_50_miles': {
                'listings': len(within_50),
                'avg_jobs': round(within_50['job_count'].mean(), 1) if len(within_50) > 0 else 0,
                'cities': within_50['cleaned_city'].nunique() if len(within_50) > 0 else 0
            }
        }
    
    metro_statistics[metro] = {
        'state': metro_data['cleaned_state'].iloc[0],
        'total_listings': len(metro_data),
        'total_cities': metro_data['cleaned_city'].nunique(),
        'categories': metro_categories
    }

print(f'Created metro-level statistics for {len(metro_statistics)} metro areas')

# 4. Airport-Level Statistics
print('\\n=== BUILDING AIRPORT-LEVEL STATISTICS ===')

airport_statistics = {}

for airport in df['closest_airport'].dropna().unique():
    airport_data = df[df['closest_airport'] == airport]
    
    airport_categories = {}
    
    for category in airport_data['job_category'].unique():
        if pd.isna(category):
            continue
            
        category_airport_data = airport_data[airport_data['job_category'] == category]
        
        job_stats = category_airport_data['job_count'].agg(['count', 'mean', 'median', 'min', 'max', 'std'])
        unique_cities = category_airport_data['cleaned_city'].nunique()
        
        airport_categories[category] = {
            'listings_count': int(job_stats['count']),
            'cities_count': unique_cities,
            'avg_jobs_per_listing': round(job_stats['mean'], 1),
            'median_jobs': round(job_stats['median'], 1),
            'min_jobs': int(job_stats['min']),
            'max_jobs': int(job_stats['max'])
        }
    
    airport_statistics[airport] = {
        'state': airport_data['cleaned_state'].iloc[0],
        'total_listings': len(airport_data),
        'total_cities': airport_data['cleaned_city'].nunique(),
        'categories': airport_categories
    }

print(f'Created airport-level statistics for {len(airport_statistics)} airports')

# 5. Category-Level Overview (averages across all locations)
print('\\n=== BUILDING CATEGORY OVERVIEW STATISTICS ===')

category_overview = {}

for category in df['job_category'].unique():
    if pd.isna(category):
        continue
        
    category_data = df[df['job_category'] == category]
    
    # Overall statistics
    job_stats = category_data['job_count'].agg(['count', 'mean', 'median', 'min', 'max', 'std'])
    
    # City-level averages
    city_averages = category_data.groupby('cleaned_city')['job_count'].mean()
    
    # State distribution
    state_distribution = category_data.groupby('cleaned_state')['job_count'].mean().to_dict()
    
    category_overview[category] = {
        'total_listings': int(job_stats['count']),
        'cities_with_jobs': category_data['cleaned_city'].nunique(),
        'states_with_jobs': category_data['cleaned_state'].nunique(),
        'avg_jobs_per_listing': round(job_stats['mean'], 1),
        'avg_jobs_per_city': round(city_averages.mean(), 1),
        'median_jobs_per_listing': round(job_stats['median'], 1),
        'min_jobs_per_listing': int(job_stats['min']),
        'max_jobs_per_listing': int(job_stats['max']),
        'std_jobs_per_listing': round(job_stats['std'], 1) if pd.notna(job_stats['std']) else 0,
        'state_averages': {state: round(avg, 1) for state, avg in state_distribution.items()}
    }

# Compile final statistical analysis
statistical_analysis = {
    'methodology': {
        'approach': 'Statistical analysis using averages, min, max per geographic unit - NO TOTALS',
        'key_metrics': ['avg_jobs_per_listing', 'avg_jobs_per_city', 'min_jobs', 'max_jobs'],
        'geographic_levels': ['city', 'metro (25/50 mile)', 'airport', 'state'],
        'note': 'Richmond Hill 11 listings means 11 search results averaged to get realistic estimate'
    },
    'category_overview': category_overview,
    'state_statistics': state_statistics,
    'metro_statistics': metro_statistics,
    'airport_statistics': airport_statistics,
    'detailed_city_breakdown': category_city_stats,
    'summary': {
        'total_categories': len(category_overview),
        'total_states': len(state_statistics),
        'total_metros': len(metro_statistics),
        'total_airports': len(airport_statistics),
        'total_cities_analyzed': sum(len(city_data) for city_data in category_city_stats.values())
    }
}

# Save the statistical analysis
with open('statistical_job_analysis.json', 'w') as f:
    json.dump(statistical_analysis, f, indent=2)

print(f'\\n✅ Saved statistical analysis to: statistical_job_analysis.json')

# Print examples and summary
print(f'\\n=== STATISTICAL ANALYSIS SUMMARY ===')
print(f'Categories analyzed: {len(category_overview)}')
print(f'States: {len(state_statistics)}')
print(f'Metro areas: {len(metro_statistics)}')
print(f'Airports: {len(airport_statistics)}')

print(f'\\n=== TOP CATEGORIES BY AVERAGE JOBS PER LISTING ===')
sorted_categories = sorted(category_overview.items(), key=lambda x: x[1]['avg_jobs_per_listing'], reverse=True)
for i, (category, data) in enumerate(sorted_categories[:5], 1):
    print(f'  {i}. {category}: {data["avg_jobs_per_listing"]} avg per listing '
          f'(range: {data["min_jobs_per_listing"]}-{data["max_jobs_per_listing"]})')

print(f'\\n=== TOP CATEGORIES BY AVERAGE JOBS PER CITY ===')
sorted_by_city = sorted(category_overview.items(), key=lambda x: x[1]['avg_jobs_per_city'], reverse=True)
for i, (category, data) in enumerate(sorted_by_city[:5], 1):
    print(f'  {i}. {category}: {data["avg_jobs_per_city"]} avg per city '
          f'({data["cities_with_jobs"]} cities)')

# Richmond Hill clarification
if 'Richmond Hill' in df['cleaned_city'].values:
    richmond_data = df[df['cleaned_city'] == 'Richmond Hill']
    print(f'\\n=== RICHMOND HILL EXAMPLE CLARIFICATION ===')
    print(f'Richmond Hill appears in {len(richmond_data)} listings across categories')
    for category in richmond_data['job_category'].unique():
        cat_data = richmond_data[richmond_data['job_category'] == category]
        if len(cat_data) > 0:
            avg_jobs = cat_data['job_count'].mean()
            min_jobs = cat_data['job_count'].min()
            max_jobs = cat_data['job_count'].max()
            print(f'  {category}: {len(cat_data)} listings, avg {avg_jobs:.1f} jobs (range: {min_jobs}-{max_jobs})')
            print(f'    Realistic estimate: {avg_jobs:.0f} jobs (NOT a sum of {len(cat_data)} listings)')

print(f'\\n📊 All statistics focus on averages, minimums, and maximums - no misleading totals!')
print(f'🏙️  City breakdowns show metro/airport context for geographic clarity')