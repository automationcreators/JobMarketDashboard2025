import pandas as pd
import json
from collections import defaultdict

print('=== ADDING ENHANCED ANALYSIS ===')
print('Adding top 3 categories by state/city and 50-mile metro concentration analysis')

# Load the statistical analysis and original data
with open('statistical_job_analysis.json', 'r') as f:
    analysis_data = json.load(f)

df = pd.read_csv('key_categories_job_analysis.csv')
print(f'Loaded {len(df):,} original records')

# 1. Add top 3 categories by state
print('\\n=== ADDING TOP 3 CATEGORIES BY STATE ===')

for state_code, state_data in analysis_data['state_statistics'].items():
    categories = state_data['categories']
    
    # Sort categories by avg_jobs_per_listing
    category_list = [(cat, data) for cat, data in categories.items()]
    category_list.sort(key=lambda x: x[1]['avg_jobs_per_listing'], reverse=True)
    
    # Get top 3
    top_3_categories = []
    for i, (category, data) in enumerate(category_list[:3], 1):
        top_3_categories.append({
            'rank': i,
            'category': category,
            'avg_jobs_per_listing': data['avg_jobs_per_listing'],
            'avg_jobs_per_city': data['avg_jobs_per_city'],
            'cities_count': data['cities_count']
        })
    
    # Add to state data
    analysis_data['state_statistics'][state_code]['top_3_categories'] = top_3_categories
    
    print(f'{state_code}:')
    for cat in top_3_categories:
        print(f'  {cat["rank"]}. {cat["category"]}: {cat["avg_jobs_per_listing"]:.1f} avg/listing, {cat["cities_count"]} cities')

# 2. Add top 3 categories for top cities
print('\\n=== ADDING TOP 3 CATEGORIES FOR TOP CITIES ===')

if 'focused_city_analysis' in analysis_data:
    for city_group in ['top_20_by_population', 'top_20_outside_major_metros']:
        if city_group in analysis_data['focused_city_analysis']:
            for city_name, city_data in analysis_data['focused_city_analysis'][city_group].items():
                job_categories = city_data['job_categories']
                
                # Sort categories by avg_jobs_per_listing
                category_list = [(cat, data) for cat, data in job_categories.items()]
                category_list.sort(key=lambda x: x[1]['avg_jobs_per_listing'], reverse=True)
                
                # Get top 3
                top_3_categories = []
                for i, (category, data) in enumerate(category_list[:3], 1):
                    top_3_categories.append({
                        'rank': i,
                        'category': category,
                        'avg_jobs_per_listing': data['avg_jobs_per_listing'],
                        'listings_count': data['listings_count']
                    })
                
                city_data['top_3_categories'] = top_3_categories

print('Added top 3 categories for all focused cities')

# 3. Create 50-mile metro concentration analysis
print('\\n=== CREATING 50-MILE METRO CONCENTRATION ANALYSIS ===')

# Count cities within 50 miles of each metro
metro_city_counts = defaultdict(lambda: {'within_50_miles': 0, 'total_cities': 0, 'categories': defaultdict(int)})

for _, row in df.iterrows():
    metro = row['closest_metro']
    distance_band = row['metro_distance_band']
    category = row['job_category']
    city = row['cleaned_city']
    
    if pd.notna(metro):
        # Count unique cities (not listings)
        metro_city_counts[metro]['total_cities'] += 1
        metro_city_counts[metro]['categories'][category] += 1
        
        if distance_band in ['0-25 miles', '25-50 miles']:
            metro_city_counts[metro]['within_50_miles'] += 1

# Convert to regular dict and calculate concentration ratios
metro_concentration = {}
for metro, data in metro_city_counts.items():
    total_listings = data['total_cities']
    within_50_miles = data['within_50_miles']
    concentration_ratio = (within_50_miles / total_listings * 100) if total_listings > 0 else 0
    
    # Get state for this metro from original data
    metro_state = df[df['closest_metro'] == metro]['cleaned_state'].iloc[0] if len(df[df['closest_metro'] == metro]) > 0 else 'Unknown'
    
    metro_concentration[metro] = {
        'state': metro_state,
        'total_job_listings': total_listings,
        'within_50_miles_listings': within_50_miles,
        'concentration_percentage': round(concentration_ratio, 1),
        'categories_count': len(data['categories']),
        'top_categories': sorted(data['categories'].items(), key=lambda x: x[1], reverse=True)[:3]
    }

# Sort by concentration percentage
metro_concentration_sorted = sorted(metro_concentration.items(), 
                                  key=lambda x: x[1]['concentration_percentage'], 
                                  reverse=True)

print(f'Analyzed {len(metro_concentration)} metro areas')
print('\\nTop 10 metros by 50-mile concentration:')
for i, (metro, data) in enumerate(metro_concentration_sorted[:10], 1):
    print(f'  {i:2d}. {metro}: {data["concentration_percentage"]}% ({data["within_50_miles_listings"]}/{data["total_job_listings"]} listings)')

# 4. State-level 50-mile metro concentration
print('\\n=== STATE-LEVEL 50-MILE METRO CONCENTRATION ===')

state_metro_concentration = defaultdict(lambda: {
    'metros': [],
    'total_metros': 0,
    'avg_concentration': 0,
    'total_listings_in_metros': 0,
    'total_within_50_miles': 0
})

for metro, data in metro_concentration.items():
    state = data['state']
    state_metro_concentration[state]['metros'].append({
        'metro': metro,
        'concentration_percentage': data['concentration_percentage'],
        'total_listings': data['total_job_listings'],
        'within_50_miles': data['within_50_miles_listings']
    })
    state_metro_concentration[state]['total_listings_in_metros'] += data['total_job_listings']
    state_metro_concentration[state]['total_within_50_miles'] += data['within_50_miles_listings']

# Calculate state averages
for state, data in state_metro_concentration.items():
    data['total_metros'] = len(data['metros'])
    data['avg_concentration'] = round(
        sum(metro['concentration_percentage'] for metro in data['metros']) / len(data['metros']), 1
    ) if len(data['metros']) > 0 else 0
    
    data['state_concentration_percentage'] = round(
        (data['total_within_50_miles'] / data['total_listings_in_metros'] * 100), 1
    ) if data['total_listings_in_metros'] > 0 else 0
    
    # Sort metros by concentration
    data['metros'].sort(key=lambda x: x['concentration_percentage'], reverse=True)

print('State-level metro concentration analysis:')
for state, data in sorted(state_metro_concentration.items()):
    print(f'{state}: {data["avg_concentration"]:.1f}% avg concentration across {data["total_metros"]} metros')

# 5. City coordinates for mapping (approximate)
print('\\n=== ADDING CITY COORDINATES FOR MAPPING ===')

# Define approximate coordinates for major cities (lat, lng)
city_coordinates = {
    # Texas
    'Houston': [29.7604, -95.3698], 'Dallas': [32.7767, -96.7970], 'San Antonio': [29.4241, -98.4936],
    'Austin': [30.2672, -97.7431], 'Fort Worth': [32.7555, -97.3308], 'El Paso': [31.7619, -106.4850],
    'Arlington': [32.7357, -97.1081], 'Corpus Christi': [27.8006, -97.3964], 'Plano': [33.0198, -96.6989],
    'Lubbock': [33.5779, -101.8552], 'Laredo': [27.5306, -99.4803], 'Garland': [32.9126, -96.6389],
    'Irving': [32.8140, -96.9489], 'Amarillo': [35.2220, -101.8313], 'Grand Prairie': [32.7460, -96.9978],
    
    # Florida
    'Jacksonville': [30.3322, -81.6557], 'Miami': [25.7617, -80.1918], 'Tampa': [27.9506, -82.4572],
    'Orlando': [28.5383, -81.3792], 'St. Petersburg': [27.7676, -82.6403], 'Hialeah': [25.8576, -80.2781],
    'Tallahassee': [30.4518, -84.2807], 'Fort Lauderdale': [26.1224, -80.1373], 'Port St. Lucie': [27.2937, -80.3501],
    'Cape Coral': [26.5629, -81.9495], 'Pembroke Pines': [26.0073, -80.2962], 'Hollywood': [26.0112, -80.1495],
    'Gainesville': [29.6516, -82.3248], 'Coral Springs': [26.2712, -80.2706], 'Clearwater': [27.9659, -82.8001],
    'Palm Bay': [28.0345, -80.5887], 'West Palm Beach': [26.7153, -80.0534], 'Spring Hill': [28.4769, -82.5265],
    
    # Georgia
    'Atlanta': [33.7490, -84.3880], 'Augusta': [33.4735, -82.0105], 'Columbus': [32.4609, -84.9877],
    'Macon': [32.8407, -83.6324], 'Savannah': [32.0835, -81.0998], 'Athens': [33.9519, -83.3576],
    'Sandy Springs': [33.9304, -84.3733], 'Roswell': [34.0232, -84.3616], 'Johns Creek': [34.0289, -84.1987],
    'Albany': [31.5804, -84.1557], 'Warner Robins': [32.6130, -83.5985], 'Alpharetta': [34.0754, -84.2941],
    
    # North Carolina  
    'Charlotte': [35.2271, -80.8431], 'Raleigh': [35.7796, -78.6382], 'Greensboro': [36.0726, -79.7920],
    'Durham': [35.9940, -78.8986], 'Winston-Salem': [36.0999, -80.2442], 'Fayetteville': [35.0527, -78.8784],
    'Cary': [35.7915, -78.7811], 'Wilmington': [34.2257, -77.9447], 'High Point': [35.9557, -80.0053],
    'Asheville': [35.5951, -82.5515], 'Gastonia': [35.2621, -81.1873], 'Greenville': [35.6127, -77.3664],
    
    # Arizona
    'Phoenix': [33.4484, -112.0740], 'Tucson': [32.2226, -110.9747], 'Mesa': [33.4152, -111.8315],
    'Chandler': [33.3062, -111.8413], 'Scottsdale': [33.4942, -111.9261], 'Glendale': [33.5387, -112.1860],
    'Gilbert': [33.3528, -111.7890], 'Tempe': [33.4255, -111.9400], 'Peoria': [33.5806, -112.2374],
    'Surprise': [33.6292, -112.3679], 'Yuma': [32.6927, -114.6277], 'Flagstaff': [35.1983, -111.6513],
    
    # Tennessee
    'Nashville': [36.1627, -86.7816], 'Memphis': [35.1495, -90.0490], 'Knoxville': [35.9606, -83.9207],
    'Chattanooga': [35.0456, -85.3097], 'Clarksville': [36.5298, -87.3595], 'Murfreesboro': [35.8456, -86.3903],
    'Franklin': [35.9251, -86.8689], 'Jackson': [35.6145, -88.8140], 'Johnson City': [36.3134, -82.3535],
    
    # Nevada
    'Las Vegas': [36.1699, -115.1398], 'Henderson': [36.0395, -114.9817], 'Reno': [39.5296, -119.8138],
    'North Las Vegas': [36.1989, -115.1175], 'Sparks': [39.5349, -119.7527], 'Carson City': [39.1638, -119.7674]
}

# Add coordinates to all cities in detailed breakdown
city_mapping_data = {}
for category, cities in analysis_data['detailed_city_breakdown'].items():
    for city, data in cities.items():
        if city not in city_mapping_data:
            city_mapping_data[city] = {
                'state': data['state'],
                'coordinates': city_coordinates.get(city, None),
                'categories': {}
            }
        
        city_mapping_data[city]['categories'][category] = {
            'avg_jobs': data['avg_jobs_per_listing'],
            'listings': data['listings_count'],
            'min_jobs': data['min_jobs'],
            'max_jobs': data['max_jobs']
        }

# Add enhanced analysis to main data
analysis_data['enhanced_analysis'] = {
    'metro_concentration_50_miles': dict(metro_concentration_sorted),
    'state_metro_concentration': dict(state_metro_concentration),
    'city_mapping_data': city_mapping_data,
    'summary_stats': {
        'metros_analyzed': len(metro_concentration),
        'cities_with_coordinates': len([c for c in city_mapping_data.values() if c['coordinates']]),
        'total_cities_for_mapping': len(city_mapping_data)
    }
}

# Save updated analysis
with open('statistical_job_analysis.json', 'w') as f:
    json.dump(analysis_data, f, indent=2)

print(f'\\n✅ Enhanced analysis added to statistical_job_analysis.json')

# Summary
print(f'\\n=== ENHANCEMENT SUMMARY ===')
print(f'• Added top 3 categories for all states')
print(f'• Added top 3 categories for focused cities')
print(f'• Created 50-mile metro concentration analysis for {len(metro_concentration)} metros')
print(f'• Added state-level metro concentration statistics')
print(f'• Prepared mapping data for {len(city_mapping_data)} cities')
print(f'• Cities with coordinates for mapping: {len([c for c in city_mapping_data.values() if c["coordinates"]])}')

print(f'\\n📊 Ready for dashboard integration!')