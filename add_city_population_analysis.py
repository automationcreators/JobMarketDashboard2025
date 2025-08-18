import pandas as pd
import json

print('=== ADDING CITY POPULATION ANALYSIS ===')

# Load the statistical analysis
with open('statistical_job_analysis.json', 'r') as f:
    analysis_data = json.load(f)

# Define approximate population data for major cities in our target states
# This includes major metropolitan areas and their populations
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

# Define major metropolitan areas (these are the primary metro centers)
major_metros = {
    'Atlanta', 'Houston', 'Dallas', 'Phoenix', 'Miami', 'Tampa', 'Charlotte', 'Nashville', 
    'Las Vegas', 'Orlando', 'Jacksonville', 'Austin', 'Fort Worth', 'San Antonio',
    'Raleigh', 'Memphis', 'Tucson', 'Greensboro', 'Durham', 'Winston-Salem'
}

print(f'Defined populations for {len(city_populations)} cities')
print(f'Identified {len(major_metros)} major metro centers')

# Get all cities from our job analysis
all_job_cities = set()
for category_data in analysis_data['detailed_city_breakdown'].values():
    all_job_cities.update(category_data.keys())

print(f'Found {len(all_job_cities)} cities with job data')

# Create population-based analysis
print('\\n=== ANALYZING TOP CITIES BY POPULATION ===')

# Filter cities that have both job data and population data
cities_with_both = []
for city in all_job_cities:
    if city in city_populations:
        cities_with_both.append({
            'city': city,
            'population': city_populations[city],
            'is_major_metro': city in major_metros
        })

cities_with_both.sort(key=lambda x: x['population'], reverse=True)
print(f'Found {len(cities_with_both)} cities with both job and population data')

# Top 20 by population
top_20_by_population = cities_with_both[:20]
print(f'\\nTop 20 cities by population:')
for i, city_data in enumerate(top_20_by_population, 1):
    metro_status = "Major Metro" if city_data['is_major_metro'] else "Secondary"
    print(f'  {i:2d}. {city_data["city"]}: {city_data["population"]:,} ({metro_status})')

# Top 20 outside major metros
outside_major_metros = [city for city in cities_with_both if not city['is_major_metro']]
outside_major_metros.sort(key=lambda x: x['population'], reverse=True)
top_20_outside_metros = outside_major_metros[:20]

print(f'\\nTop 20 cities outside major metros:')
for i, city_data in enumerate(top_20_outside_metros, 1):
    print(f'  {i:2d}. {city_data["city"]}: {city_data["population"]:,}')

# Create job analysis for these specific city groups
def analyze_city_group(city_list, group_name):
    group_analysis = {}
    
    for city_data in city_list:
        city = city_data['city']
        city_job_data = {}
        
        # Collect job data for this city across all categories
        for category, category_cities in analysis_data['detailed_city_breakdown'].items():
            if city in category_cities:
                city_job_data[category] = category_cities[city]
        
        if city_job_data:  # Only include if city has job data
            group_analysis[city] = {
                'population': city_data['population'],
                'is_major_metro': city_data['is_major_metro'],
                'job_categories': city_job_data,
                'category_count': len(city_job_data),
                'total_listings': sum(data['listings_count'] for data in city_job_data.values()),
                'avg_jobs_across_categories': round(
                    sum(data['avg_jobs_per_listing'] for data in city_job_data.values()) / len(city_job_data), 1
                ) if city_job_data else 0
            }
    
    return group_analysis

# Analyze both groups
top_population_analysis = analyze_city_group(top_20_by_population, 'Top 20 by Population')
outside_metros_analysis = analyze_city_group(top_20_outside_metros, 'Top 20 Outside Major Metros')

print(f'\\n=== ANALYSIS RESULTS ===')
print(f'Top 20 by population: {len(top_population_analysis)} cities with job data')
print(f'Top 20 outside metros: {len(outside_metros_analysis)} cities with job data')

# Add to the main analysis data
analysis_data['focused_city_analysis'] = {
    'methodology': {
        'top_population_criteria': 'Top 20 cities by population with job data available',
        'outside_metros_criteria': 'Top 20 cities outside major metro centers by population',
        'major_metros_defined': list(major_metros),
        'population_source': 'Approximate 2023 estimates for metropolitan areas'
    },
    'top_20_by_population': top_population_analysis,
    'top_20_outside_major_metros': outside_metros_analysis,
    'city_populations': city_populations,
    'summary': {
        'total_cities_with_population_data': len(cities_with_both),
        'major_metros_count': len(major_metros),
        'top_pop_with_jobs': len(top_population_analysis),
        'outside_metros_with_jobs': len(outside_metros_analysis)
    }
}

# Save updated analysis
with open('statistical_job_analysis.json', 'w') as f:
    json.dump(analysis_data, f, indent=2)

print(f'\\n✅ Updated statistical_job_analysis.json with focused city analysis')

# Show examples
print(f'\\n=== EXAMPLE INSIGHTS ===')

if 'Mesa' in top_population_analysis:
    mesa_data = top_population_analysis['Mesa']
    print(f'Mesa, AZ (pop. {mesa_data["population"]:,}):')
    print(f'  Categories: {mesa_data["category_count"]}')
    print(f'  Avg jobs across categories: {mesa_data["avg_jobs_across_categories"]}')
    print(f'  Total listings: {mesa_data["total_listings"]}')

if 'Spring Hill' in outside_metros_analysis:
    spring_hill_data = outside_metros_analysis['Spring Hill']
    print(f'\\nSpring Hill, FL (pop. {spring_hill_data["population"]:,}) - Outside Major Metro:')
    print(f'  Categories: {spring_hill_data["category_count"]}')
    print(f'  Avg jobs across categories: {spring_hill_data["avg_jobs_across_categories"]}')
    print(f'  Total listings: {spring_hill_data["total_listings"]}')

print(f'\\n📊 Ready for dashboard integration!')