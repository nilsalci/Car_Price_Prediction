# Car Price Prediction using Web Scraping and Regression

## Project Description
This project aims to predict car prices using data collected through web scraping from [arabam.com](https://www.arabam.com). The dataset includes various car features such as model, year, mileage, engine power, and more. Using regression models, the project aims to provide accurate price predictions based on these features.

## Data Sources
- **arabam.com**: Used to scrape car listings with features such as brand, series, model, year, mileage, engine power, and price.
- **Web Scraping Tools**: `requests` and `BeautifulSoup` were used to collect the data.

## Technologies and Tools
- **Programming Language:** Python
- **Libraries:** Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn
- **Web Scraping Tools:** Requests, BeautifulSoup
- **Regression Models:** Linear Regression, Ridge Regression, Lasso Regression, Decision Tree Regressor

## Analysis Steps
### Data Collection
- Used `requests` and `BeautifulSoup` to scrape car listing data from arabam.com.
- Collected features such as:
  - Brand, Series, Model, Year, Mileage, Gear Type, Fuel Type
  - Car body type, Color, Engine Power, Price, and other detailed attributes.

### Data Cleaning
- Removed invalid or null entries.
- Converted data types and standardized formats for numerical columns.
- Created new features by extracting details such as fuel efficiency and car age.

### Exploratory Data Analysis (EDA)
- Visualized the distribution of key features.
- Analyzed correlations to identify influential features for car price prediction.

### Model Training
- Implemented the following models for regression analysis:
  - Linear Regression
  - Ridge Regression
  - Lasso Regression
  - Decision Tree Regressor
- Evaluated models using metrics like Mean Squared Error (MSE) and R-squared score.

### Key Findings
- Features like car brand, model year, mileage, and engine power had significant impact on pricing.
- Ridge Regression showed the best performance with optimal regularization parameters.

## Recommendations
- For better accuracy, adding location-based data or seller type information may improve model performance.
- Outlier removal or advanced feature engineering can enhance prediction quality.

## How to Run the Project
### Prerequisites
- Python 3.7+
- Required Libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `beautifulsoup4`, `requests`

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Car_Price_Prediction
   ```
2. Navigate to the project directory:
   ```bash
   cd Car_Price_Prediction
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the scraping script to collect data:
   ```bash
   python part1_finalcode.py
   ```
5. Run the Jupyter Notebook for data analysis and model training:
   ```bash
   jupyter notebook arabam_car_price_prediction.ipynb
   ```

## Contributors
- [@Sevag9](https://github.com/Sevag9)
- [@nilsalci](https://github.com/nilsalci)

## References
- [arabam.com](https://www.arabam.com)

