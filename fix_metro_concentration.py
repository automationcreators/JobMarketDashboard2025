import pandas as pd
import json
from collections import defaultdict

print('=== FIXING METRO CONCENTRATION ANALYSIS ===')

# Load data
with open('statistical_job_analysis.json', 'r') as f:
    analysis_data = json.load(f)

df = pd.read_csv('key_categories_job_analysis.csv')

print('Metro distance band distribution:')
print(df['metro_distance_band'].value_counts())

# Fix 50-mile metro concentration analysis with correct distance bands
metro_city_counts = defaultdict(lambda: {
    'within_metro': 0, 
    'within_25_miles': 0, 
    'within_50_miles': 0, 
    'beyond_50_miles': 0,
    'total_listings': 0,
    'cities': set(),
    'categories': defaultdict(int)
})

for _, row in df.iterrows():
    metro = row['closest_metro']
    distance_band = row['metro_distance_band']
    category = row['job_category']
    city = row['cleaned_city']
    
    if pd.notna(metro) and pd.notna(distance_band):
        metro_city_counts[metro]['total_listings'] += 1
        metro_city_counts[metro]['cities'].add(city)
        metro_city_counts[metro]['categories'][category] += 1
        
        if distance_band == 'Within Metro':
            metro_city_counts[metro]['within_metro'] += 1
        elif distance_band == 'Within 25 miles':
            metro_city_counts[metro]['within_25_miles'] += 1
        elif distance_band == 'Within 50 miles':
            metro_city_counts[metro]['within_50_miles'] += 1
        elif distance_band == 'Beyond 50 miles':
            metro_city_counts[metro]['beyond_50_miles'] += 1

# Calculate concentration metrics
metro_concentration = {}
for metro, data in metro_city_counts.items():
    total_listings = data['total_listings']
    within_50_total = data['within_metro'] + data['within_25_miles'] + data['within_50_miles']
    concentration_ratio = (within_50_total / total_listings * 100) if total_listings > 0 else 0
    
    # Get state for this metro
    metro_state = df[df['closest_metro'] == metro]['cleaned_state'].iloc[0] if len(df[df['closest_metro'] == metro]) > 0 else 'Unknown'
    
    metro_concentration[metro] = {
        'state': metro_state,
        'total_listings': total_listings,
        'unique_cities': len(data['cities']),
        'within_metro': data['within_metro'],
        'within_25_miles': data['within_25_miles'],
        'within_50_miles': data['within_50_miles'],
        'beyond_50_miles': data['beyond_50_miles'],
        'within_50_total': within_50_total,
        'concentration_percentage': round(concentration_ratio, 1),
        'categories_count': len(data['categories']),
        'top_categories': sorted(data['categories'].items(), key=lambda x: x[1], reverse=True)[:3]
    }

# Sort by total listings (market size)
metro_concentration_sorted = sorted(metro_concentration.items(), 
                                  key=lambda x: x[1]['total_listings'], 
                                  reverse=True)

print(f'\\nAnalyzed {len(metro_concentration)} metro areas')
print('\\nTop 10 metros by total job listings:')
for i, (metro, data) in enumerate(metro_concentration_sorted[:10], 1):
    print(f'  {i:2d}. {metro}: {data["total_listings"]:,} listings ({data["unique_cities"]} cities)')
    print(f'      Within 50 miles: {data["within_50_total"]:,} ({data["concentration_percentage"]}%)')

# State-level analysis with corrected data
state_metro_concentration = defaultdict(lambda: {
    'metros': [],
    'total_metros': 0,
    'total_listings': 0,
    'total_within_50_miles': 0,
    'total_cities': 0
})

for metro, data in metro_concentration.items():
    state = data['state']
    state_metro_concentration[state]['metros'].append({
        'metro': metro,
        'total_listings': data['total_listings'],
        'within_50_total': data['within_50_total'],
        'concentration_percentage': data['concentration_percentage'],
        'unique_cities': data['unique_cities']
    })
    state_metro_concentration[state]['total_listings'] += data['total_listings']
    state_metro_concentration[state]['total_within_50_miles'] += data['within_50_total']
    state_metro_concentration[state]['total_cities'] += data['unique_cities']

# Calculate state metrics
for state, data in state_metro_concentration.items():
    data['total_metros'] = len(data['metros'])
    data['state_concentration_percentage'] = round(
        (data['total_within_50_miles'] / data['total_listings'] * 100), 1
    ) if data['total_listings'] > 0 else 0
    
    data['avg_concentration'] = round(
        sum(metro['concentration_percentage'] for metro in data['metros']) / len(data['metros']), 1
    ) if len(data['metros']) > 0 else 0
    
    # Sort metros by total listings
    data['metros'].sort(key=lambda x: x['total_listings'], reverse=True)

print('\\n=== STATE-LEVEL METRO CONCENTRATION ===')
for state, data in sorted(state_metro_concentration.items()):
    print(f'{state}: {data["state_concentration_percentage"]:.1f}% overall concentration')
    print(f'    {data["total_within_50_miles"]:,}/{data["total_listings"]:,} listings, {data["total_cities"]:,} cities, {data["total_metros"]} metros')

# Update the enhanced analysis with corrected data
analysis_data['enhanced_analysis']['metro_concentration_50_miles'] = dict(metro_concentration_sorted)
analysis_data['enhanced_analysis']['state_metro_concentration'] = dict(state_metro_concentration)

# Save corrected analysis
with open('statistical_job_analysis.json', 'w') as f:
    json.dump(analysis_data, f, indent=2)

print(f'\\n✅ Fixed metro concentration analysis in statistical_job_analysis.json')
print(f'📊 Ready for dashboard integration with correct concentration metrics!')