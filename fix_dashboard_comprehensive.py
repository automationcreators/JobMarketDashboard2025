import pandas as pd
import json
from collections import defaultdict

print('=== COMPREHENSIVE DASHBOARD FIX ===')
print('1. Expanding to top 5 categories per state')
print('2. Regenerating all missing analysis sections')
print('3. Ensuring complete data for all dashboard tabs')

# Load the merged CSV data
df = pd.read_csv('key_categories_job_analysis_merged.csv')
print(f'Loaded {len(df):,} records with merged nursing categories')

# 1. REGENERATE COMPLETE CATEGORY OVERVIEW
print('\n=== REGENERATING CATEGORY OVERVIEW ===')
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

# 2. REGENERATE STATE STATISTICS WITH TOP 5 CATEGORIES
print('\n=== REGENERATING STATE STATISTICS (TOP 5) ===')
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
    
    # Sort categories by avg_jobs_per_listing to get top 5
    sorted_categories = sorted(state_categories.items(), 
                             key=lambda x: x[1]['avg_jobs_per_listing'], 
                             reverse=True)
    
    # Get top 5 instead of top 3
    top_5_categories = []
    for i, (category, data) in enumerate(sorted_categories[:5], 1):
        top_5_categories.append({
            'rank': i,
            'category': category,
            'avg_jobs_per_listing': data['avg_jobs_per_listing'],
            'avg_jobs_per_city': data['avg_jobs_per_city'],
            'cities_count': data['cities_count']
        })
    
    state_stats[state] = {
        'categories': state_categories,
        'top_5_categories': top_5_categories,  # Changed from top_3 to top_5
        'total_listings': len(state_data),
        'total_cities': state_data['cleaned_city'].nunique(),
        'total_categories': len(state_categories),
        'total_titles': len(state_data)
    }

# 3. REGENERATE DETAILED CITY BREAKDOWN
print('\n=== REGENERATING DETAILED CITY BREAKDOWN ===')
detailed_breakdown = {}

for category in df['job_category'].unique():
    category_data = df[df['job_category'] == category]
    city_breakdown = {}
    
    for city in category_data['cleaned_city'].unique():
        city_data = category_data[category_data['cleaned_city'] == city]
        
        city_breakdown[city] = {
            'state': city_data['cleaned_state'].iloc[0],
            'avg_jobs_per_listing': round(city_data['job_count'].mean(), 1),
            'listings_count': len(city_data),
            'min_jobs': int(city_data['job_count'].min()),
            'max_jobs': int(city_data['job_count'].max()),
            'closest_metro': city_data['closest_metro'].iloc[0] if pd.notna(city_data['closest_metro'].iloc[0]) else None,
            'metro_distance_band': city_data['metro_distance_band'].iloc[0] if pd.notna(city_data['metro_distance_band'].iloc[0]) else None,
            'closest_airport': city_data['closest_airport'].iloc[0] if pd.notna(city_data['closest_airport'].iloc[0]) else None
        }
    
    detailed_breakdown[category] = city_breakdown

# 4. REGENERATE METRO AREA ANALYSIS
print('\n=== REGENERATING METRO AREA ANALYSIS ===')
metro_stats = {}
for metro in df['closest_metro'].dropna().unique():
    metro_data = df[df['closest_metro'] == metro]
    
    metro_categories = {}
    for category in metro_data['job_category'].unique():
        cat_data = metro_data[metro_data['job_category'] == category]
        metro_categories[category] = {
            'avg_jobs_per_listing': round(cat_data['job_count'].mean(), 1),
            'listings_count': len(cat_data),
            'cities_count': cat_data['cleaned_city'].nunique()
        }
    
    metro_stats[metro] = {
        'state': metro_data['cleaned_state'].iloc[0],
        'categories': metro_categories,
        'total_listings': len(metro_data),
        'total_cities': metro_data['cleaned_city'].nunique(),
        'total_categories': len(metro_categories)
    }

# 5. REGENERATE AIRPORT PROXIMITY ANALYSIS
print('\n=== REGENERATING AIRPORT PROXIMITY ANALYSIS ===')
airport_stats = {}
for airport in df['closest_airport'].dropna().unique():
    airport_data = df[df['closest_airport'] == airport]
    
    airport_categories = {}
    for category in airport_data['job_category'].unique():
        cat_data = airport_data[airport_data['job_category'] == category]
        airport_categories[category] = {
            'avg_jobs_per_listing': round(cat_data['job_count'].mean(), 1),
            'listings_count': len(cat_data),
            'cities_count': cat_data['cleaned_city'].nunique()
        }
    
    airport_stats[airport] = {
        'categories': airport_categories,
        'total_listings': len(airport_data),
        'total_cities': airport_data['cleaned_city'].nunique(),
        'states_served': airport_data['cleaned_state'].nunique()
    }

# 6. REGENERATE POPULATION-BASED ANALYSIS
print('\n=== REGENERATING POPULATION-BASED ANALYSIS ===')

# Define city populations (from previous analysis)
city_populations = {
    # Texas
    'Houston': 2300000, 'San Antonio': 1540000, 'Dallas': 1340000, 'Austin': 980000,
    'Fort Worth': 910000, 'El Paso': 680000, 'Arlington': 400000, 'Corpus Christi': 320000,
    'Plano': 290000, 'Lubbock': 260000, 'Laredo': 260000, 'Garland': 240000,
    'Irving': 240000, 'Amarillo': 200000, 'Grand Prairie': 190000, 'Brownsville': 185000,
    'McKinney': 195000, 'Frisco': 200000, 'Mesquite': 140000, 'Killeen': 155000,
    
    # Florida  
    'Jacksonville': 910000, 'Miami': 470000, 'Tampa': 390000, 'Orlando': 310000,
    'St. Petersburg': 260000, 'Hialeah': 230000, 'Tallahassee': 190000, 'Fort Lauderdale': 180000,
    'Port St. Lucie': 200000, 'Cape Coral': 190000, 'Pembroke Pines': 170000,
    'Hollywood': 150000, 'Miramar': 140000, 'Gainesville': 140000, 'Coral Springs': 130000,
    'Miami Gardens': 110000, 'Clearwater': 115000, 'Palm Bay': 115000, 'West Palm Beach': 110000,
    'Pompano Beach': 110000, 'Spring Hill': 110000, 'Lakeland': 110000,
    
    # Georgia
    'Atlanta': 500000, 'Augusta': 200000, 'Columbus': 195000, 'Macon': 150000,
    'Savannah': 145000, 'Athens': 125000, 'Sandy Springs': 110000, 'Roswell': 95000,
    'Johns Creek': 85000, 'Albany': 70000, 'Warner Robins': 80000, 'Alpharetta': 65000,
    'Marietta': 60000, 'Valdosta': 55000, 'Smyrna': 55000, 'Dunwoody': 50000,
    
    # North Carolina
    'Charlotte': 880000, 'Raleigh': 470000, 'Greensboro': 295000, 'Durham': 280000,
    'Winston-Salem': 245000, 'Fayetteville': 210000, 'Cary': 175000, 'Wilmington': 120000,
    'High Point': 115000, 'Concord': 95000, 'Asheville': 95000, 'Gastonia': 75000,
    'Greenville': 90000, 'Rocky Mount': 55000, 'Huntersville': 60000, 'Burlington': 55000,
    
    # Arizona
    'Phoenix': 1680000, 'Tucson': 550000, 'Mesa': 510000, 'Chandler': 270000,
    'Scottsdale': 260000, 'Glendale': 250000, 'Gilbert': 250000, 'Tempe': 195000,
    'Peoria': 180000, 'Surprise': 140000, 'Yuma': 95000, 'Avondale': 90000,
    'Goodyear': 80000, 'Flagstaff': 75000, 'Buckeye': 70000, 'Lake Havasu City': 55000,
    
    # Tennessee
    'Nashville': 690000, 'Memphis': 650000, 'Knoxville': 190000, 'Chattanooga': 180000,
    'Clarksville': 160000, 'Murfreesboro': 150000, 'Franklin': 80000, 'Jackson': 65000,
    'Johnson City': 65000, 'Bartlett': 60000, 'Hendersonville': 60000, 'Kingsport': 55000,
    'Collierville': 50000, 'Cleveland': 45000, 'Smyrna': 50000, 'Germantown': 40000,
    
    # Nevada
    'Las Vegas': 650000, 'Henderson': 320000, 'Reno': 250000, 'North Las Vegas': 250000,
    'Sparks': 105000, 'Carson City': 55000, 'Fernley': 20000, 'Elko': 20000,
    'Mesquite': 20000, 'Boulder City': 15000
}

major_metros = {
    'Atlanta', 'Houston', 'Dallas', 'Phoenix', 'Miami', 'Tampa', 'Charlotte', 'Nashville', 
    'Las Vegas', 'Orlando', 'Jacksonville', 'Austin', 'Fort Worth', 'San Antonio',
    'Raleigh', 'Memphis', 'Tucson', 'Greensboro', 'Durham', 'Winston-Salem'
}

# Get all cities from job analysis that have population data
all_job_cities = set()
for category_data in detailed_breakdown.values():
    all_job_cities.update(category_data.keys())

cities_with_both = []
for city in all_job_cities:
    if city in city_populations:
        cities_with_both.append({
            'city': city,
            'population': city_populations[city],
            'is_major_metro': city in major_metros
        })

cities_with_both.sort(key=lambda x: x['population'], reverse=True)

# Top 20 by population analysis
def analyze_city_group(city_list, group_name):
    group_analysis = {}
    
    for city_data in city_list:
        city = city_data['city']
        city_job_data = {}
        
        # Collect job data for this city across all categories
        for category, category_cities in detailed_breakdown.items():
            if city in category_cities:
                city_job_data[category] = category_cities[city]
        
        if city_job_data:  # Only include if city has job data
            # Get top 3 categories for this city
            categories_sorted = sorted(city_job_data.items(), 
                                     key=lambda x: x[1]['avg_jobs_per_listing'], 
                                     reverse=True)
            
            top_3_categories = []
            for i, (category, data) in enumerate(categories_sorted[:3], 1):
                top_3_categories.append({
                    'rank': i,
                    'category': category,
                    'avg_jobs_per_listing': data['avg_jobs_per_listing'],
                    'listings_count': data['listings_count']
                })
            
            group_analysis[city] = {
                'population': city_data['population'],
                'is_major_metro': city_data['is_major_metro'],
                'job_categories': city_job_data,
                'top_3_categories': top_3_categories,
                'category_count': len(city_job_data),
                'total_listings': sum(data['listings_count'] for data in city_job_data.values()),
                'avg_jobs_across_categories': round(
                    sum(data['avg_jobs_per_listing'] for data in city_job_data.values()) / len(city_job_data), 1
                ) if city_job_data else 0
            }
    
    return group_analysis

# Generate focused city analysis
top_20_by_population = cities_with_both[:20]
outside_major_metros = [city for city in cities_with_both if not city['is_major_metro']][:20]

focused_city_analysis = {
    'methodology': {
        'top_population_criteria': 'Top 20 cities by population with job data available',
        'outside_metros_criteria': 'Top 20 cities outside major metro centers by population',
        'major_metros_defined': list(major_metros),
        'population_source': 'Approximate 2023 estimates for metropolitan areas'
    },
    'top_20_by_population': analyze_city_group(top_20_by_population, 'Top 20 by Population'),
    'top_20_outside_major_metros': analyze_city_group(outside_major_metros, 'Top 20 Outside Major Metros'),
    'city_populations': city_populations,
    'summary': {
        'total_cities_with_population_data': len(cities_with_both),
        'major_metros_count': len(major_metros),
        'top_pop_with_jobs': len(analyze_city_group(top_20_by_population, 'test')),
        'outside_metros_with_jobs': len(analyze_city_group(outside_major_metros, 'test'))
    }
}

# 7. CREATE COMPREHENSIVE ANALYSIS JSON
print('\n=== CREATING COMPREHENSIVE ANALYSIS JSON ===')

# Load existing enhanced analysis (metro concentration, etc.)
try:
    with open('statistical_job_analysis.json', 'r') as f:
        existing_data = json.load(f)
    enhanced_analysis = existing_data.get('enhanced_analysis', {})
    power_cities_analysis = existing_data.get('power_cities_analysis', {})
except:
    enhanced_analysis = {}
    power_cities_analysis = {}

comprehensive_analysis = {
    'methodology': {
        'note': 'Licensed Practical Nurse merged with Registered Nurse - same job category',
        'merge_date': '2025-08-13',
        'approach': 'Statistical averages only - no misleading totals due to overlapping listings',
        'top_categories_expanded': 'Now showing top 5 categories per state instead of top 3'
    },
    'category_overview': category_stats,
    'state_statistics': state_stats,
    'metro_area_statistics': metro_stats,
    'airport_proximity_statistics': airport_stats,
    'detailed_city_breakdown': detailed_breakdown,
    'focused_city_analysis': focused_city_analysis,
    'enhanced_analysis': enhanced_analysis,
    'power_cities_analysis': power_cities_analysis,
    'summary_stats': {
        'total_categories': len(category_stats),
        'total_states': len(state_stats),
        'total_metros': len(metro_stats),
        'total_airports': len(airport_stats),
        'total_records': len(df),
        'total_cities': len(all_job_cities)
    }
}

# Save comprehensive analysis
with open('statistical_job_analysis.json', 'w') as f:
    json.dump(comprehensive_analysis, f, indent=2)

print(f'\n✅ COMPREHENSIVE ANALYSIS COMPLETE')
print(f'📊 Categories: {len(category_stats)}')
print(f'🏛️  States: {len(state_stats)} (now with top 5 categories each)')
print(f'🏙️  Metro areas: {len(metro_stats)}')
print(f'✈️  Airports: {len(airport_stats)}')
print(f'🌆 Cities: {len(all_job_cities)}')
print(f'📋 Total records: {len(df):,}')

print(f'\n=== TOP 5 CATEGORIES BY STATE ===')
for state_code in sorted(state_stats.keys()):
    state_data = state_stats[state_code]
    top_5 = state_data['top_5_categories']
    
    print(f'\n{state_code}:')
    for cat in top_5:
        print(f'  {cat["rank"]}. {cat["category"]}: {cat["avg_jobs_per_listing"]} avg/listing')

print(f'\n🎯 All dashboard tabs should now have complete data!')