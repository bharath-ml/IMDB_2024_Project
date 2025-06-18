# 🎬 IMDB 2024 Movies - Data Scraping & Interactive Dashboard

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io)
[![Selenium](https://img.shields.io/badge/Selenium-4.0%2B-green.svg)](https://selenium.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive data pipeline that scrapes IMDb movie data for 2024, processes it, stores it in a SQL database, and provides an interactive dashboard for data exploration and analysis.

## 🚀 Features

- **🔍 Automated Web Scraping**: Extract movie data from IMDb using Selenium
- **🧹 Data Processing**: Clean and standardize scraped data
- **💾 Database Storage**: Store processed data in SQL database
- **📊 Interactive Dashboard**: Streamlit-powered visualization interface
- **🎛️ Advanced Filtering**: Multi-parameter filtering system
- **📈 Rich Visualizations**: Multiple chart types using Plotly
- **📁 Export Functionality**: Download filtered data as CSV

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Features](#features-detailed)
- [Data Schema](#data-schema)
- [Dashboard Overview](#dashboard-overview)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Chrome browser
- ChromeDriver (automatically managed by Selenium)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/imdb-2024-movies.git
   cd imdb-2024-movies
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup directories**
   ```bash
   mkdir -p scraping/genre_csvs
   mkdir -p scraping/scraping
   ```

## 🚀 Quick Start

### 1. Run Data Scraping
```bash
python scraping_script.py
```

### 2. Clean the Data
```bash
python data_cleaning.py
```

### 3. Launch Dashboard
```bash
streamlit run dashboard.py
```

Visit `http://localhost:8501` to access the interactive dashboard.

## 📁 Project Structure

```
imdb-2024-movies/
│
├── scraping/
│   ├── genre_csvs/           # Individual genre CSV files
│   └── scraping/
│       ├── imdb_2024_all_movies.csv
│       └── imdb_2024_all_movies_cleaned.csv
│
├── scraping_script.py        # Web scraping automation
├── data_cleaning.py          # Data preprocessing
├── dashboard.py              # Streamlit dashboard
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── PROJECT_REPORT.md         # Detailed project report
```

## 💻 Usage

### Web Scraping

The scraping script automatically:
- Navigates to IMDb 2024 movie pages by genre
- Handles pagination with "Load More" buttons
- Extracts movie details (title, rating, votes, duration, genre)
- Saves genre-specific CSV files

```python
# Modify genres list in scraping_script.py
genres = ['action', 'adventure', 'animation', 'biography', 'comedy', 'drama']
```

### Data Cleaning

The cleaning script processes raw data:
- Standardizes data formats
- Converts duration to minutes
- Handles missing values
- Validates data integrity

### Dashboard Features

Access the interactive dashboard to:
- **Filter movies** by rating, duration, votes, and genre
- **Visualize trends** with interactive charts
- **Explore correlations** between different metrics
- **Export filtered data** for further analysis

## 🎯 Features Detailed

### 🔍 Data Scraping
- **Multi-genre Support**: Configurable genre list
- **Pagination Handling**: Automatic "Load More" clicking
- **Error Recovery**: Robust exception handling
- **Data Validation**: Quality checks during extraction

### 📊 Interactive Dashboard

#### Filtering Options
- **Rating Filter**: Minimum IMDb rating (0-10)
- **Duration Filter**: Movie length categories
- **Vote Filter**: Minimum vote count threshold
- **Genre Filter**: Multi-select genre filtering

#### Visualization Types
- **Rankings**: Top movies by rating/votes
- **Distributions**: Rating and duration histograms
- **Genre Analysis**: Distribution and heatmaps
- **Correlations**: Rating vs. vote relationships

### 📈 Chart Types
- Bar Charts (Horizontal & Vertical)
- Histograms
- Scatter Plots with Trendlines
- Heatmaps
- Interactive Tables

## 🗄️ Data Schema

| Field | Type | Description |
|-------|------|-------------|
| Title | String | Movie title |
| Rating | Float | IMDb rating (0-10) |
| Votes | Integer | Number of user votes |
| Duration | Integer | Movie length in minutes |
| Genre | String | Movie genre category |

## 📊 Dashboard Overview

### Main Sections

1. **📈 Rankings Tab**
   - Top 10 movies by rating
   - Top 10 movies by vote count
   - Rating distribution analysis

2. **🎭 Genres Tab**
   - Genre distribution visualization
   - Genre vs. rating heatmap

3. **⏱️ Duration Tab**
   - Duration distribution analysis
   - Average duration by genre

4. **💫 Correlations Tab**
   - Rating vs. vote count analysis
   - Correlation coefficients

5. **📋 Data Table Tab**
   - Filtered data display
   - Sortable columns
   - CSV export functionality

## 🛠️ Requirements

```txt
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.0.0
selenium>=4.0.0
numpy>=1.21.0
sqlalchemy>=1.4.0
```

## 🎯 Use Cases

### For Movie Industry Professionals
- **Producers**: Identify successful genre trends
- **Distributors**: Analyze market preferences
- **Analysts**: Comprehensive industry research

### For Data Enthusiasts
- **Learning**: Web scraping and visualization techniques
- **Analysis**: Movie industry trend exploration
- **Development**: Base for advanced analytics projects

## 🔧 Configuration

### Scraping Settings
```python
# Modify in scraping_script.py
BASE_URL = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres={}"
GENRES = ['action', 'adventure', 'animation', 'biography']
```

### Dashboard Settings
```python
# Modify in dashboard.py
CSV_PATH = "scraping/scraping/imdb_2024_all_movies_cleaned.csv"
PAGE_CONFIG = {
    "page_title": "IMDB 2024 Movies Dashboard",
    "page_icon": "🎬",
    "layout": "wide"
}
```

## 🚨 Known Issues & Solutions

### Common Issues

1. **ChromeDriver Issues**
   - Ensure Chrome browser is updated
   - Selenium automatically manages ChromeDriver

2. **Data Loading Errors**
   - Check CSV file path in dashboard.py
   - Ensure data cleaning step completed successfully

3. **Dashboard Performance**
   - Use filtering to reduce dataset size
   - Clear browser cache if charts don't load

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to functions
- Include error handling
- Test on sample data first

## 📈 Future Enhancements

- [ ] **API Integration**: Real-time data updates
- [ ] **Cloud Deployment**: AWS/Azure hosting
- [ ] **Advanced Analytics**: Machine learning insights
- [ ] **Additional Data Sources**: Multiple movie databases
- [ ] **Mobile Optimization**: Responsive design improvements

## ⚠️ Disclaimer

This project is for educational purposes. Please respect IMDb's robots.txt and terms of service. Consider rate limiting and responsible scraping practices.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

If you found this project helpful, please give it a ⭐!

For questions or support:
- Open an issue on GitHub
- Contact: [parimibharathkumar@gmail.com]

## 🏆 Acknowledgments

- **IMDb** for providing comprehensive movie data
- **Streamlit** for the amazing dashboard framework
- **Plotly** for interactive visualization capabilities
- **Selenium** for robust web scraping tools

---

**Made with ❤️ and Python**

*Last Updated: June 2025*