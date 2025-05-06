import streamlit as st
from scraper_module import ProductScraper, DataAnalyzer, Visualizer  # Adjust import paths
import logging

# Custom Cichlify CSS
st.markdown("""
    <style>
        body {
            background-color: #EAEBED;
            color: #282B28;
        }
        .main {
            background-color: #EAEBED;
        }
        h1, h2, h3 {
            color: #3B28CC;
        }
        .stButton>button {
            background-color: #1098F7;
            color: white;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title("Cichlify Product Intelligence")
st.markdown("🔍 Analyze Amazon & eBay product trends with **real-time scraping and forecasting**.")

# Input
product_name = st.text_input("Enter Product Name:", "wireless headphones")

if st.button("Analyze"):
    with st.spinner("Scraping data..."):
        try:
            scraper = ProductScraper(max_retries=3, delay_between_requests=2)
            amazon_data = scraper.scrape_amazon(product_name, max_pages=2)
            ebay_data = scraper.scrape_ebay(product_name, max_pages=2)
            scraper.close()

            analyzer = DataAnalyzer(amazon_data, ebay_data)

            st.subheader("📊 Price Statistics")
            st.dataframe(analyzer.get_price_statistics())

            st.subheader("🤼 Competitive Analysis")
            st.dataframe(analyzer.get_competitive_analysis())

            st.subheader("📈 Price Predictions")
            predictions, model = analyzer.predict_future_prices()
            if predictions is not None:
                st.dataframe(predictions)

            st.subheader("🖼️ Visual Insights")
            vis_data = analyzer.create_visualization_data()
            visualizer = Visualizer(vis_data)

            # Render plots
            st.pyplot(visualizer.create_price_distribution())
            st.pyplot(visualizer.create_price_boxplot())
            if predictions is not None:
                st.pyplot(visualizer.create_price_prediction_chart(predictions, model))
            visualizer.create_interactive_plots()  # Optional: save HTML and embed?

        except Exception as e:
            st.error(f"An error occurred: {e}")
