# Job Market Analysis Dashboard

Interactive job market analysis dashboard with comprehensive statistical insights for 7 target states (AZ, FL, TX, NV, TN, GA, NC).

## 🚀 Live Demo

Visit the live dashboard: [https://joblistings-analysis.vercel.app](https://joblistings-analysis.vercel.app)

## 📊 Features

- **Interactive Dashboard** with 7 geographic analysis tabs
- **Statistical Methodology** using averages to eliminate duplicate counting
- **Top 4 Categories Analysis** per city with rankings and job numbers
- **Metro Concentration Analysis** with 50-mile radius mapping
- **Population-Based Analysis** comparing major metros vs secondary markets
- **Power Cities Analysis** showing category leadership across markets

## 🗂️ Dashboard Sections

1. **By State** - Enhanced with top 5 categories and concentration metrics
2. **By Metro Area** - Metropolitan area job market analysis
3. **Metro Concentration** - 50-mile analysis showing regional concentration
4. **Top 20 by Population** - Major metropolitan areas analysis
5. **Top 20 Outside Metros** - Secondary markets with key insights
6. **Power Cities** - Category leadership matrix analysis
7. **All Cities Detail** - Comprehensive city breakdown with mapping

## 📈 Key Data Insights

- **2.46M Realistic Jobs** analyzed (corrected from 21.3M inflated count)
- **75,152 Job Listings** across 11 categories and 7 states
- **24 Metro Areas** with concentration analysis
- **Healthcare Dominance** - Registered Nurse leads in 50% of secondary markets
- **Geographic Specialization** - Different cities excel in different job categories

## 🛠️ Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Visualization**: Plotly.js, D3.js
- **Mapping**: Leaflet.js
- **Data Processing**: Python, Pandas
- **Deployment**: Vercel

## 📁 File Structure

```
├── index.html                          # Main dashboard
├── statistical_job_analysis.json       # Complete analysis data
├── key_categories_job_analysis.csv     # Original dataset
├── statistical_job_analysis.py         # Core analysis script
├── vercel.json                         # Deployment configuration
└── analysis_scripts/                   # Data processing scripts
```

## 🚀 Local Development

1. Clone the repository:
```bash
git clone https://github.com/automationcreators/JoblistingsAnalysis.git
cd JoblistingsAnalysis
```

2. Start a local server:
```bash
python3 -m http.server 8000
```

3. Open `http://localhost:8000` in your browser

## 📊 Data Sources

- **Indeed.com Job Listings** (~100K original records)
- **Geographic Data** with metro/airport proximity
- **Population Data** for city analysis
- **7 Target States**: Arizona, Florida, Texas, Nevada, Tennessee, Georgia, North Carolina

## 🔧 Methodology

- **Statistical Averages**: Uses averages instead of sums to avoid duplicate counting
- **Geographic Context**: Metro/airport proximity for realistic job concentration
- **Data Quality**: Merged similar categories (Licensed Practical Nurse + Registered Nurse)
- **Realistic Estimates**: 2.46M total realistic job opportunities

## 📝 License

This project is open source and available under the MIT License.

---

*🤖 Generated with [Claude Code](https://claude.ai/code)*