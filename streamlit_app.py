import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import re
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="IMDB 2024 Movies Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #E50914;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2C3E50 0%, #34495E 100%);
    }
    .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the IMDB data"""
    try:
        # Update this path to match your CSV file location
        csv_path = "scraping/scraping/imdb_2024_all_movies_cleaned.csv"
        df = pd.read_csv(csv_path)
        
        # Clean column names
        df.columns = [str(col).strip().replace(" ", "_") for col in df.columns]
        
        # Handle missing values and data cleaning
        def clean_cell(value):
            if pd.isna(value):
                return None
            if str(value).strip().lower() in ["nan", "none", ""]:
                return None
            return value
        
        df = df.applymap(clean_cell)
        
        # Clean and convert data types
        if 'Rating' in df.columns:
            df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        
        if 'Votes' in df.columns:
            # Remove commas and convert to numeric
            df['Votes'] = df['Votes'].astype(str).str.replace(',', '').str.replace('K', '000').str.replace('M', '000000')
            df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce')
        
        if 'Duration' in df.columns:
            # Extract duration in minutes
            def extract_duration(duration_str):
                if pd.isna(duration_str):
                    return None
                duration_str = str(duration_str)
                # Look for patterns like "2h 30m" or "120 min"
                hours = re.findall(r'(\d+)h', duration_str)
                minutes = re.findall(r'(\d+)m', duration_str)
                
                total_minutes = 0
                if hours:
                    total_minutes += int(hours[0]) * 60
                if minutes:
                    total_minutes += int(minutes[0])
                
                # If no h/m pattern found, try to extract just numbers (assume minutes)
                if total_minutes == 0:
                    nums = re.findall(r'\d+', duration_str)
                    if nums:
                        total_minutes = int(nums[0])
                
                return total_minutes if total_minutes > 0 else None
            
            df['Duration_Minutes'] = df['Duration'].apply(extract_duration)
            df['Duration_Hours'] = df['Duration_Minutes'] / 60
        
        # Remove rows with all NaN values
        df = df.dropna(how='all')
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def create_summary_metrics(df):
    """Create summary metrics cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_movies = len(df)
        st.metric("Total Movies", f"{total_movies:,}")
    
    with col2:
        avg_rating = df['Rating'].mean() if 'Rating' in df.columns else 0
        st.metric("Average Rating", f"{avg_rating:.1f}/10")
    
    with col3:
        total_votes = df['Votes'].sum() if 'Votes' in df.columns else 0
        st.metric("Total Votes", f"{total_votes:,.0f}")
    
    with col4:
        unique_genres = df['Genre'].nunique() if 'Genre' in df.columns else 0
        st.metric("Unique Genres", unique_genres)

def create_top_movies_chart(df, metric='Rating', top_n=10):
    """Create top movies chart"""
    if metric not in df.columns:
        return None
    
    top_movies = df.nlargest(top_n, metric)[['Title', metric]].copy()
    
    fig = px.bar(
        top_movies, 
        x=metric, 
        y='Title',
        orientation='h',
        title=f'Top {top_n} Movies by {metric}',
        color=metric,
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        height=400,
        yaxis={'categoryorder': 'total ascending'},
        template='plotly_white'
    )
    
    return fig

def create_genre_distribution(df):
    """Create genre distribution chart"""
    if 'Genre' not in df.columns:
        return None
    
    genre_counts = df['Genre'].value_counts().head(20)
    
    fig = px.bar(
        x=genre_counts.index,
        y=genre_counts.values,
        title='Movie Distribution by Genre (Top 20)',
        labels={'x': 'Genre', 'y': 'Number of Movies'},
        color=genre_counts.values,
        color_continuous_scale='plasma'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=400,
        template='plotly_white'
    )
    
    return fig

def create_rating_distribution(df):
    """Create rating distribution histogram"""
    if 'Rating' not in df.columns:
        return None
    
    fig = px.histogram(
        df,
        x='Rating',
        nbins=20,
        title='Distribution of Movie Ratings',
        labels={'Rating': 'IMDb Rating', 'count': 'Number of Movies'},
        color_discrete_sequence=['#E50914']
    )
    
    fig.update_layout(
        height=400,
        template='plotly_white'
    )
    
    return fig

def create_duration_analysis(df):
    """Create duration analysis charts"""
    if 'Duration_Hours' not in df.columns:
        return None, None
    
    # Duration distribution
    fig1 = px.histogram(
        df.dropna(subset=['Duration_Hours']),
        x='Duration_Hours',
        nbins=20,
        title='Distribution of Movie Durations',
        labels={'Duration_Hours': 'Duration (Hours)', 'count': 'Number of Movies'},
        color_discrete_sequence=['#764ba2']
    )
    
    fig1.update_layout(height=300, template='plotly_white')
    
    # Average duration by genre
    if 'Genre' in df.columns:
        genre_duration = df.groupby('Genre')['Duration_Hours'].mean().sort_values(ascending=False).head(15)
        
        fig2 = px.bar(
            x=genre_duration.values,
            y=genre_duration.index,
            orientation='h',
            title='Average Duration by Genre (Top 15)',
            labels={'x': 'Average Duration (Hours)', 'y': 'Genre'},
            color=genre_duration.values,
            color_continuous_scale='viridis'
        )
        
        fig2.update_layout(
            height=400,
            yaxis={'categoryorder': 'total ascending'},
            template='plotly_white'
        )
    else:
        fig2 = None
    
    return fig1, fig2

def create_correlation_analysis(df):
    """Create correlation scatter plot"""
    if 'Rating' not in df.columns or 'Votes' not in df.columns:
        return None
    
    # Remove outliers for better visualization
    clean_df = df.dropna(subset=['Rating', 'Votes'])
    
    fig = px.scatter(
        clean_df,
        x='Rating',
        y='Votes',
        title='Correlation: Rating vs Vote Count',
        labels={'Rating': 'IMDb Rating', 'Votes': 'Number of Votes'},
        opacity=0.6,
        color='Rating',
        color_continuous_scale='viridis'
    )
    
    # Add manual trendline using numpy polyfit (alternative to statsmodels)
    if len(clean_df) > 1:
        # Calculate linear regression manually
        x = clean_df['Rating'].values
        y = clean_df['Votes'].values
        
        # Remove any remaining NaN values
        mask = ~(np.isnan(x) | np.isnan(y))
        x_clean = x[mask]
        y_clean = y[mask]
        
        if len(x_clean) > 1:
            # Fit linear regression
            coeffs = np.polyfit(x_clean, y_clean, 1)
            trendline_x = np.linspace(x_clean.min(), x_clean.max(), 100)
            trendline_y = np.polyval(coeffs, trendline_x)
            
            # Add trendline to plot
            fig.add_trace(
                go.Scatter(
                    x=trendline_x,
                    y=trendline_y,
                    mode='lines',
                    name='Trendline',
                    line=dict(color='red', width=2, dash='dash')
                )
            )
    
    fig.update_layout(height=400, template='plotly_white')
    
    return fig

def create_genre_rating_heatmap(df):
    """Create genre vs rating heatmap"""
    if 'Genre' not in df.columns or 'Rating' not in df.columns:
        return None
    
    # Create rating bins
    df_clean = df.dropna(subset=['Genre', 'Rating']).copy()
    df_clean['Rating_Bin'] = pd.cut(df_clean['Rating'], bins=[0, 6, 7, 8, 9, 10], labels=['≤6', '6-7', '7-8', '8-9', '9-10'])
    
    # Create crosstab
    heatmap_data = pd.crosstab(df_clean['Genre'], df_clean['Rating_Bin'])
    
    # Take top 15 genres
    top_genres = df_clean['Genre'].value_counts().head(15).index
    heatmap_data = heatmap_data.loc[top_genres]
    
    fig = px.imshow(
        heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        title='Genre vs Rating Distribution Heatmap',
        labels={'x': 'Rating Range', 'y': 'Genre', 'color': 'Number of Movies'},
        color_continuous_scale='blues'
    )
    
    fig.update_layout(height=500, template='plotly_white')
    
    return fig

def apply_filters(df, filters):
    """Apply user-selected filters to the dataframe"""
    filtered_df = df.copy()
    
    # Rating filter
    if filters['min_rating'] > 0:
        filtered_df = filtered_df[filtered_df['Rating'] >= filters['min_rating']]
    
    # Duration filter
    if filters['duration_range'] != 'All':
        if 'Duration_Hours' in filtered_df.columns:
            if filters['duration_range'] == '< 2 hours':
                filtered_df = filtered_df[filtered_df['Duration_Hours'] < 2]
            elif filters['duration_range'] == '2-3 hours':
                filtered_df = filtered_df[(filtered_df['Duration_Hours'] >= 2) & (filtered_df['Duration_Hours'] <= 3)]
            elif filters['duration_range'] == '> 3 hours':
                filtered_df = filtered_df[filtered_df['Duration_Hours'] > 3]
    
    # Voting filter
    if filters['min_votes'] > 0:
        if 'Votes' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Votes'] >= filters['min_votes']]
    
    # Genre filter
    if filters['selected_genres']:
        filtered_df = filtered_df[filtered_df['Genre'].isin(filters['selected_genres'])]
    
    return filtered_df

def main():
    # Header
    st.markdown('<h1 class="main-header">🎬 IMDB 2024 Movies Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    if df.empty:
        st.error("No data available. Please check your CSV file path.")
        return
    
    # Sidebar filters
    st.sidebar.header("🔧 Filters & Controls")
    
    # Rating filter
    min_rating = st.sidebar.slider(
        "Minimum Rating",
        min_value=0.0,
        max_value=10.0,
        value=0.0,
        step=0.1
    )
    
    # Duration filter
    duration_options = ['All', '< 2 hours', '2-3 hours', '> 3 hours']
    duration_range = st.sidebar.selectbox("Duration Range", duration_options)
    
    # Voting filter
    min_votes = st.sidebar.number_input(
        "Minimum Votes",
        min_value=0,
        max_value=int(df['Votes'].max()) if 'Votes' in df.columns else 100000,
        value=0,
        step=1000
    )
    
    # Genre filter
    if 'Genre' in df.columns:
        all_genres = sorted(df['Genre'].dropna().unique())
        selected_genres = st.sidebar.multiselect(
            "Select Genres",
            options=all_genres,
            default=[]
        )
    else:
        selected_genres = []
    
    # Apply filters
    filters = {
        'min_rating': min_rating,
        'duration_range': duration_range,
        'min_votes': min_votes,
        'selected_genres': selected_genres
    }
    
    filtered_df = apply_filters(df, filters)
    
    # Summary metrics
    st.subheader("📊 Overview")
    create_summary_metrics(filtered_df)
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Rankings", "🎭 Genres", "⏱️ Duration", "💫 Correlations", "📋 Data Table"])
    
    with tab1:
        st.subheader("Top Movies Rankings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top rated movies
            fig_rating = create_top_movies_chart(filtered_df, 'Rating', 10)
            if fig_rating:
                st.plotly_chart(fig_rating, use_container_width=True)
        
        with col2:
            # Top voted movies
            fig_voting = create_top_movies_chart(filtered_df, 'Votes', 10)
            if fig_voting:
                st.plotly_chart(fig_voting, use_container_width=True)
        
        # Rating distribution
        fig_rating_dist = create_rating_distribution(filtered_df)
        if fig_rating_dist:
            st.plotly_chart(fig_rating_dist, use_container_width=True)
    
    with tab2:
        st.subheader("Genre Analysis")
        
        # Genre distribution
        fig_genre = create_genre_distribution(filtered_df)
        if fig_genre:
            st.plotly_chart(fig_genre, use_container_width=True)
        
        # Genre vs rating heatmap
        fig_heatmap = create_genre_rating_heatmap(filtered_df)
        if fig_heatmap:
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab3:
        st.subheader("Duration Analysis")
        
        fig_duration_dist, fig_duration_genre = create_duration_analysis(filtered_df)
        
        if fig_duration_dist:
            st.plotly_chart(fig_duration_dist, use_container_width=True)
        
        if fig_duration_genre:
            st.plotly_chart(fig_duration_genre, use_container_width=True)
    
    with tab4:
        st.subheader("Correlation Analysis")
        
        fig_correlation = create_correlation_analysis(filtered_df)
        if fig_correlation:
            st.plotly_chart(fig_correlation, use_container_width=True)
        
        # Additional insights
        if 'Rating' in filtered_df.columns and 'Votes' in filtered_df.columns:
            correlation = filtered_df['Rating'].corr(filtered_df['Votes'])
            st.metric("Rating-Votes Correlation", f"{correlation:.3f}")
    
    with tab5:
        st.subheader("Filtered Data Table")
        
        # Display filter info
        st.info(f"Showing {len(filtered_df)} out of {len(df)} movies based on your filters.")
        
        # Select columns to display
        if not filtered_df.empty:
            available_columns = filtered_df.columns.tolist()
            display_columns = st.multiselect(
                "Select columns to display:",
                options=available_columns,
                default=[col for col in ['Title', 'Genre', 'Rating', 'Votes', 'Duration'] if col in available_columns]
            )
            
            if display_columns:
                # Sort options
                sort_column = st.selectbox("Sort by:", options=display_columns)
                sort_ascending = st.checkbox("Ascending order", value=False)
                
                # Display the table
                display_df = filtered_df[display_columns].sort_values(
                    by=sort_column, 
                    ascending=sort_ascending
                ).reset_index(drop=True)
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    height=400
                )
                
                # Download button
                csv = display_df.to_csv(index=False)
                st.download_button(
                    label="Download filtered data as CSV",
                    data=csv,
                    file_name=f"imdb_2024_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    # Footer
    st.markdown("---")
    st.markdown("**IMDB 2024 Movies Dashboard** | Built with Streamlit & Plotly | Data source: IMDb")

if __name__ == "__main__":
    main()