# Interactive Job Analysis Dashboard

A web-based interactive dashboard for exploring job market data with dynamic visualizations and filtering capabilities.

## 🚀 Quick Start

### Option 1: Using Python Server (Recommended)
```bash
python3 serve_dashboard.py
```
Then open: http://localhost:8000/interactive_dashboard.html

### Option 2: Using Custom Port
```bash
python3 serve_dashboard.py 8080
```
Then open: http://localhost:8080/interactive_dashboard.html

### Option 3: Direct File Opening
Simply open `interactive_dashboard.html` in your web browser (some features may be limited due to CORS restrictions).

## 📊 Dashboard Features

### 🎯 Interactive Controls
- **Dataset Selection**: Switch between State, City, Category, and Detailed Job Title analyses
- **Chart Types**: Bar charts, pie charts, scatter plots, and line charts
- **Top N Filter**: Show top 10, 15, 20, or 25 results
- **Search Filter**: Real-time filtering of data table results

### 📈 Visualizations
1. **Primary Chart**: Main visualization based on selected dataset and chart type
2. **Secondary Analysis**: Complementary insights (e.g., Jobs vs Confidence correlation)
3. **Statistics Overview**: Key metrics cards showing totals and summaries
4. **Data Table**: Sortable, searchable table with detailed data

### 📋 Available Datasets

#### 1. State Level Analysis
- **Metrics**: Total listings, average jobs per search, cities covered, confidence scores
- **Visualizations**: State rankings, job availability vs confidence scatter plots
- **Use Cases**: Regional strategy, market expansion planning

#### 2. City Level Analysis  
- **Metrics**: City listings, job category diversity, average jobs per search
- **Visualizations**: City rankings, diversity analysis
- **Use Cases**: Local market research, city-specific opportunities

#### 3. Job Category Analysis
- **Metrics**: Category totals, unique titles, confidence scores, geographic spread
- **Visualizations**: Category popularity, confidence by category
- **Use Cases**: Industry analysis, skill demand assessment

#### 4. Detailed Job Titles
- **Metrics**: Title frequency, confidence, geographic distribution
- **Visualizations**: Most common titles, title performance analysis
- **Use Cases**: Job title optimization, market positioning

## 🎨 Dashboard Sections

### Statistics Grid
Real-time overview cards showing:
- Total job listings analyzed
- States and cities covered  
- Job categories identified
- Key performance metrics

### Interactive Charts
- **Responsive Design**: Charts adapt to screen size
- **Hover Details**: Rich tooltips with additional information
- **Dynamic Updates**: Charts update instantly when filters change
- **Export Capability**: Charts can be downloaded as images

### Data Table
- **Live Search**: Filter rows in real-time
- **Formatted Numbers**: Automatic number formatting with commas
- **Sticky Headers**: Headers remain visible while scrolling
- **Top 50 Display**: Shows most relevant results for performance

## 🛠️ Technical Features

### Built With
- **D3.js**: Data manipulation and processing
- **Plotly.js**: Interactive charting library
- **PapaParse**: CSV parsing and processing
- **Vanilla JavaScript**: No heavy frameworks, fast loading

### Browser Compatibility
- ✅ Chrome/Chromium (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ⚠️ Internet Explorer (limited support)

### Performance Optimizations
- **Lazy Loading**: Charts load only when needed
- **Data Chunking**: Large datasets processed in chunks
- **Responsive Design**: Optimized for desktop and mobile
- **Caching**: Browser caches data for faster subsequent loads

## 📁 Required Files

The dashboard requires these CSV files in the same directory:
- `state_level_analysis.csv` - State-level aggregated data
- `city_level_analysis.csv` - City-level aggregated data
- `job_category_analysis.csv` - Job category summaries
- `detailed_job_title_analysis.csv` - Individual job title data

## 🔧 Troubleshooting

### Common Issues

#### "Failed to load data files"
- **Cause**: CSV files not found or CORS restrictions
- **Solution**: Use the Python server (`python3 serve_dashboard.py`)

#### Charts not displaying
- **Cause**: JavaScript disabled or old browser
- **Solution**: Enable JavaScript and use a modern browser

#### Port already in use
- **Cause**: Another service using port 8000
- **Solution**: Use custom port (`python3 serve_dashboard.py 8080`)

#### Data appears incomplete
- **Cause**: CSV files may be missing or corrupted
- **Solution**: Regenerate CSV files using the analysis scripts

### Browser Console
Check browser developer tools (F12) for detailed error messages if issues persist.

## 💡 Usage Tips

### For Job Seekers
1. Use **State Analysis** to identify high-opportunity regions
2. Switch to **City Analysis** for local market insights
3. Explore **Job Categories** to understand demand trends
4. Filter **Detailed Titles** to find specific opportunities

### For Employers/Recruiters
1. **Geographic Analysis**: Identify talent hotspots and underserved markets
2. **Competition Analysis**: Use job counts to assess market saturation
3. **Title Optimization**: Analyze confidence scores for better job posting titles
4. **Market Expansion**: Use emerging markets data for strategic planning

### For Analysts
1. **Trend Analysis**: Compare metrics across different dimensions
2. **Market Segmentation**: Use scatter plots to identify patterns
3. **Data Export**: Use browser tools to export chart data
4. **Regional Comparison**: Toggle between datasets for comprehensive analysis

## 🚀 Advanced Usage

### Custom Analysis
- Use search filters to focus on specific regions or job types
- Combine multiple chart types to uncover hidden patterns
- Export chart images for presentations and reports

### Data Integration
- CSV files can be updated with new data
- Dashboard automatically picks up changes on page refresh
- Compatible with standard data processing workflows

---

## 🆘 Support

If you encounter issues:
1. Check browser console for error messages
2. Verify all CSV files are present
3. Try using the Python server instead of direct file opening
4. Ensure you're using a modern browser with JavaScript enabled

**Enjoy exploring your job market data! 📊✨**