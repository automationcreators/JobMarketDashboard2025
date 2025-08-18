import pandas as pd
import json
from collections import defaultdict, Counter

print('=== CREATING POWER CITIES ANALYSIS ===')
print('Analyzing top 3 cities per job category and identifying consistent leaders')

# Load the statistical analysis
with open('statistical_job_analysis.json', 'r') as f:
    analysis_data = json.load(f)

# Create top 3 cities analysis for each category
top_cities_by_category = {}
all_top_cities = []

print('\\n=== ANALYZING TOP 3 CITIES PER CATEGORY ===')

for category, city_data in analysis_data['detailed_city_breakdown'].items():
    # Get all cities for this category and sort by avg jobs per listing
    cities_list = []
    for city, data in city_data.items():
        cities_list.append({
            'city': city,
            'state': data['state'],
            'avg_jobs': data['avg_jobs_per_listing'],
            'listings': data['listings_count'],
            'min_jobs': data['min_jobs'],
            'max_jobs': data['max_jobs']
        })
    
    # Sort by average jobs per listing (descending)
    cities_list.sort(key=lambda x: x['avg_jobs'], reverse=True)
    
    # Get top 3
    top_3 = cities_list[:3]
    top_cities_by_category[category] = top_3
    
    # Add to overall tracking
    for rank, city_data in enumerate(top_3, 1):
        all_top_cities.append({
            'city': city_data['city'],
            'state': city_data['state'],
            'category': category,
            'rank': rank,
            'avg_jobs': city_data['avg_jobs']
        })
    
    print(f'{category}:')
    for i, city in enumerate(top_3, 1):
        print(f'  {i}. {city["city"]}, {city["state"]}: {city["avg_jobs"]:.1f} avg jobs ({city["listings"]} listings)')

# Analyze city consistency across categories
print('\\n=== ANALYZING CITY CONSISTENCY ACROSS CATEGORIES ===')

# Count appearances in top 3
city_appearances = Counter(f"{city['city']}, {city['state']}" for city in all_top_cities)
city_categories = defaultdict(list)

for city_data in all_top_cities:
    city_key = f"{city_data['city']}, {city_data['state']}"
    city_categories[city_key].append({
        'category': city_data['category'],
        'rank': city_data['rank'],
        'avg_jobs': city_data['avg_jobs']
    })

# Categorize cities by consistency
consistent_leaders = {}  # Appear in top 3 for many categories
occasional_leaders = {}  # Appear in top 3 for some categories
specialist_cities = {}   # Appear in top 3 for few categories

for city, count in city_appearances.items():
    categories_info = city_categories[city]
    
    # Calculate average rank and #1 positions
    avg_rank = sum(cat['rank'] for cat in categories_info) / len(categories_info)
    num_first_place = sum(1 for cat in categories_info if cat['rank'] == 1)
    categories_list = [cat['category'] for cat in categories_info]
    
    city_analysis = {
        'appearances': count,
        'categories': categories_list,
        'avg_rank': round(avg_rank, 1),
        'first_place_count': num_first_place,
        'category_details': categories_info
    }
    
    # Categorize based on appearances
    if count >= 8:  # Appears in top 3 for 8+ categories (consistent leaders)
        consistent_leaders[city] = city_analysis
    elif count >= 4:  # Appears in top 3 for 4-7 categories (occasional leaders)
        occasional_leaders[city] = city_analysis
    else:  # Appears in top 3 for 1-3 categories (specialists)
        specialist_cities[city] = city_analysis

print(f'Consistent Leaders (8+ categories): {len(consistent_leaders)}')
print(f'Occasional Leaders (4-7 categories): {len(occasional_leaders)}')
print(f'Specialist Cities (1-3 categories): {len(specialist_cities)}')

# Create efficient summary tables
print('\\n=== CREATING EFFICIENT SUMMARY TABLES ===')

# Sort each group by most appearances, then by avg rank
def sort_cities(cities_dict):
    return sorted(cities_dict.items(), key=lambda x: (-x[1]['appearances'], x[1]['avg_rank']))

consistent_sorted = sort_cities(consistent_leaders)
occasional_sorted = sort_cities(occasional_leaders)

# Create compact category matrix showing top city for each category
category_leaders = {}
for category, top_cities in top_cities_by_category.items():
    if top_cities:
        leader = top_cities[0]  # #1 city
        category_leaders[category] = {
            'city': leader['city'],
            'state': leader['state'],
            'avg_jobs': leader['avg_jobs']
        }

# Prepare power cities analysis for dashboard
power_cities_analysis = {
    'methodology': {
        'approach': 'Top 3 cities per job category based on average jobs per listing',
        'consistency_tiers': {
            'consistent_leaders': '8+ categories in top 3',
            'occasional_leaders': '4-7 categories in top 3', 
            'specialist_cities': '1-3 categories in top 3'
        },
        'metrics': ['appearances_in_top_3', 'average_rank', 'first_place_count']
    },
    'top_3_by_category': top_cities_by_category,
    'category_leaders': category_leaders,
    'power_cities': {
        'consistent_leaders': {city: data for city, data in consistent_sorted},
        'occasional_leaders': {city: data for city, data in occasional_sorted[:10]},  # Top 10 occasional
        'top_specialists': {city: data for city, data in sort_cities(specialist_cities)[:5]}  # Top 5 specialists
    },
    'summary_stats': {
        'total_unique_cities_in_top_3': len(city_appearances),
        'total_category_leader_positions': len(all_top_cities),
        'most_consistent_city': consistent_sorted[0][0] if consistent_sorted else None,
        'categories_analyzed': len(top_cities_by_category)
    }
}

# Add to main analysis
analysis_data['power_cities_analysis'] = power_cities_analysis

# Save updated analysis
with open('statistical_job_analysis.json', 'w') as f:
    json.dump(analysis_data, f, indent=2)

print(f'\\n✅ Added power cities analysis to statistical_job_analysis.json')

# Print summary for verification
print(f'\\n=== POWER CITIES SUMMARY ===')

if consistent_sorted:
    print(f'\\nCONSISTENT LEADERS (Top 5):')
    for i, (city, data) in enumerate(consistent_sorted[:5], 1):
        print(f'  {i}. {city}: {data["appearances"]} categories, avg rank {data["avg_rank"]}, {data["first_place_count"]} #1s')

if occasional_sorted:
    print(f'\\nOCCASIONAL LEADERS (Top 5):')
    for i, (city, data) in enumerate(occasional_sorted[:5], 1):
        categories = ', '.join(data['categories'][:3])
        if len(data['categories']) > 3:
            categories += f' +{len(data["categories"])-3} more'
        print(f'  {i}. {city}: {data["appearances"]} categories ({categories})')

print(f'\\nCATEGORY LEADERS (#1 in each category):')
for category, leader in category_leaders.items():
    print(f'  {category}: {leader["city"]}, {leader["state"]} ({leader["avg_jobs"]:.1f} avg jobs)')

print(f'\\n📊 Ready for compact dashboard display!')