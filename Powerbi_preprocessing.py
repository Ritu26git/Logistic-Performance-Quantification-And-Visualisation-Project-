import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class PowerBIDataPreprocessor:
    """
    Complete preprocessing pipeline for Power BI Logistics Dashboard
    Handles cleaning, transformation, and feature engineering
    """
    
    def __init__(self):
        self.salesperson_df = None
        self.shipment_df = None
        self.country_df = None
        self.product_df = None
        
    def load_data(self, salesperson_path, shipment_path, country_path, product_path):
        """Load all CSV files"""
        print("Loading data files...")
        self.salesperson_df = pd.read_csv(salesperson_path)
        self.shipment_df = pd.read_csv(shipment_path)
        self.country_df = pd.read_csv(country_path)
        self.product_df = pd.read_csv(product_path)
        print("✓ Data loaded successfully\n")
        
    def clean_salesperson_data(self):
        """Clean and preprocess salesperson data"""
        print("Cleaning SalesPerson data...")
        df = self.salesperson_df.copy()
        
        # Remove empty rows
        df = df.dropna(how='all')
        
        # Strip whitespace from all string columns
        df['Sales Person'] = df['Sales Person'].str.strip()
        df['Team'] = df['Team'].str.strip()
        
        # Validate picture URLs
        df['Picture'] = df['Picture'].fillna('')
        
        self.salesperson_df = df
        print(f"✓ SalesPerson: {len(df)} records cleaned\n")
        return df
    
    def clean_shipment_data(self):
        """Clean and preprocess shipment data"""
        print("Cleaning Shipment data...")
        df = self.shipment_df.copy()
        
        # Convert date columns to datetime
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
        df['Delivered On'] = pd.to_datetime(df['Delivered On'], format='%d/%m/%Y', errors='coerce')
        
        # Strip whitespace from string columns
        df['Sales Person'] = df['Sales Person'].str.strip()
        df['Geography'] = df['Geography'].str.strip()
        df['Product'] = df['Product'].str.strip()
        df['Status'] = df['Status'].str.strip()
        
        # Create additional time features
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Month Name'] = df['Date'].dt.strftime('%b')
        df['Quarter'] = df['Date'].dt.quarter
        df['Weekday'] = df['Date'].dt.day_name()
        df['Week'] = df['Date'].dt.isocalendar().week
        
        # Calculate delivery time (days)
        df['Delivery Time'] = (df['Delivered On'] - df['Date']).dt.days
        df['Delivery Time'] = df['Delivery Time'].fillna(0)
        
        # Flag late deliveries (assuming >15 days is late)
        df['Is Late'] = df['Delivery Time'] > 15
        
        # Create status categories
        df['Is Active'] = df['Status'] == 'Active'
        df['Is Completed'] = df['Status'] == 'Completed'
        df['Is Returned'] = df['Status'] == 'Returned'
        
        self.shipment_df = df
        print(f"✓ Shipment: {len(df)} records cleaned\n")
        return df
    
    def clean_country_data(self):
        """Clean and preprocess country data"""
        print("Cleaning Country data...")
        df = self.country_df.copy()
        
        # Strip whitespace
        df['Geography'] = df['Geography'].str.strip()
        df['Region'] = df['Region'].str.strip()
        
        self.country_df = df
        print(f"✓ Country: {len(df)} records cleaned\n")
        return df
    
    def clean_product_data(self):
        """Clean and preprocess product data"""
        print("Cleaning Product data...")
        df = self.product_df.copy()
        
        # Strip whitespace
        df['Product'] = df['Product'].str.strip()
        df['Category'] = df['Category'].str.strip()
        
        # Ensure cost is numeric
        df['Cost per Box'] = pd.to_numeric(df['Cost per Box'], errors='coerce')
        
        self.product_df = df
        print(f"✓ Product: {len(df)} records cleaned\n")
        return df
    
    def create_master_dataset(self):
        """Merge all datasets into a master dataset"""
        print("Creating master dataset...")
        
        # Start with shipment data
        master = self.shipment_df.copy()
        
        # Merge with salesperson
        master = master.merge(
            self.salesperson_df,
            on='Sales Person',
            how='left'
        )
        
        # Merge with country
        master = master.merge(
            self.country_df,
            on='Geography',
            how='left'
        )
        
        # Merge with product
        master = master.merge(
            self.product_df,
            on='Product',
            how='left'
        )
        
        # Calculate revenue (Sales * Cost per Box)
        master['Revenue'] = master['Sales'] * master['Cost per Box']
        
        # Create profit margin (assuming 30% margin)
        master['Profit'] = master['Revenue'] * 0.30
        
        print(f"✓ Master dataset created: {len(master)} records\n")
        return master
    
    def create_aggregated_tables(self, master_df):
        """Create aggregated tables for Power BI"""
        print("Creating aggregated tables...")
        
        # Monthly aggregation
        monthly_agg = master_df.groupby(['Year', 'Month', 'Month Name']).agg({
            'Sales': 'sum',
            'Revenue': 'sum',
            'Profit': 'sum',
            'Shipment ID': 'count',
            'Delivery Time': 'mean'
        }).reset_index()
        monthly_agg.columns = ['Year', 'Month', 'Month Name', 'Total Sales', 
                               'Total Revenue', 'Total Profit', 'Shipment Count', 
                               'Avg Delivery Time']
        
        # Sales person performance
        salesperson_agg = master_df.groupby(['Sales Person', 'Team']).agg({
            'Sales': 'sum',
            'Revenue': 'sum',
            'Shipment ID': 'count',
            'Delivery Time': 'mean',
            'Is Completed': 'sum'
        }).reset_index()
        salesperson_agg.columns = ['Sales Person', 'Team', 'Total Sales', 
                                   'Total Revenue', 'Shipment Count', 
                                   'Avg Delivery Time', 'Completed Count']
        
        # Geography performance
        geography_agg = master_df.groupby(['Geography', 'Region']).agg({
            'Sales': 'sum',
            'Revenue': 'sum',
            'Shipment ID': 'count',
            'Delivery Time': 'mean'
        }).reset_index()
        geography_agg.columns = ['Geography', 'Region', 'Total Sales', 
                                'Total Revenue', 'Shipment Count', 
                                'Avg Delivery Time']
        
        # Product performance
        product_agg = master_df.groupby(['Product', 'Category']).agg({
            'Sales': 'sum',
            'Revenue': 'sum',
            'Shipment ID': 'count',
            'Delivery Time': 'mean'
        }).reset_index()
        product_agg.columns = ['Product', 'Category', 'Total Sales', 
                              'Total Revenue', 'Shipment Count', 
                              'Avg Delivery Time']
        
        # Status summary
        status_agg = master_df.groupby('Status').agg({
            'Shipment ID': 'count',
            'Sales': 'sum',
            'Revenue': 'sum'
        }).reset_index()
        status_agg.columns = ['Status', 'Shipment Count', 'Total Sales', 'Total Revenue']
        
        print("✓ Aggregated tables created\n")
        
        return {
            'monthly': monthly_agg,
            'salesperson': salesperson_agg,
            'geography': geography_agg,
            'product': product_agg,
            'status': status_agg
        }
    
    def validate_data_quality(self, df):
        """Validate data quality and print report"""
        print("\n" + "="*60)
        print("DATA QUALITY REPORT")
        print("="*60)
        
        print(f"\nTotal Records: {len(df)}")
        print(f"Total Columns: {len(df.columns)}")
        
        # Missing values
        print("\nMissing Values:")
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if len(missing) > 0:
            for col, count in missing.items():
                print(f"  - {col}: {count} ({count/len(df)*100:.2f}%)")
        else:
            print("  ✓ No missing values")
        
        # Duplicate records
        duplicates = df.duplicated(subset=['Shipment ID']).sum()
        print(f"\nDuplicate Shipment IDs: {duplicates}")
        
        # Data ranges
        print("\nData Ranges:")
        print(f"  - Date Range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"  - Sales Range: ${df['Sales'].min():.2f} to ${df['Sales'].max():.2f}")
        print(f"  - Avg Sales: ${df['Sales'].mean():.2f}")
        
        # Status distribution
        print("\nStatus Distribution:")
        status_dist = df['Status'].value_counts()
        for status, count in status_dist.items():
            print(f"  - {status}: {count} ({count/len(df)*100:.2f}%)")
        
        print("\n" + "="*60 + "\n")
    
    def export_data(self, master_df, aggregated_tables, output_dir='./processed_data/'):
        """Export all processed data"""
        print("Exporting processed data...")
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Export master dataset
        master_df.to_csv(f'{output_dir}master_dataset.csv', index=False)
        print(f"✓ Exported: master_dataset.csv")
        
        # Export individual cleaned tables
        self.salesperson_df.to_csv(f'{output_dir}salesperson_cleaned.csv', index=False)
        self.shipment_df.to_csv(f'{output_dir}shipment_cleaned.csv', index=False)
        self.country_df.to_csv(f'{output_dir}country_cleaned.csv', index=False)
        self.product_df.to_csv(f'{output_dir}product_cleaned.csv', index=False)
        print(f"✓ Exported: individual cleaned tables")
        
        # Export aggregated tables
        for name, df in aggregated_tables.items():
            df.to_csv(f'{output_dir}{name}_aggregated.csv', index=False)
            print(f"✓ Exported: {name}_aggregated.csv")
        
        print(f"\n✓ All files exported to: {output_dir}\n")
    
    def run_pipeline(self, salesperson_path, shipment_path, country_path, product_path):
        """Run the complete preprocessing pipeline"""
        print("\n" + "="*60)
        print("POWER BI DATA PREPROCESSING PIPELINE")
        print("="*60 + "\n")
        
        # Load data
        self.load_data(salesperson_path, shipment_path, country_path, product_path)
        
        # Clean individual tables
        self.clean_salesperson_data()
        self.clean_shipment_data()
        self.clean_country_data()
        self.clean_product_data()
        
        # Create master dataset
        master_df = self.create_master_dataset()
        
        # Create aggregated tables
        aggregated_tables = self.create_aggregated_tables(master_df)
        
        # Validate data quality
        self.validate_data_quality(master_df)
        
        # Export data
        self.export_data(master_df, aggregated_tables)
        
        print("="*60)
        print("PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        return master_df, aggregated_tables


# Example usage
if __name__ == "__main__":
    # Initialize preprocessor
    preprocessor = PowerBIDataPreprocessor()
    
    # Run pipeline
    master_data, agg_tables = preprocessor.run_pipeline(
        salesperson_path='SalesPerson.csv',
        shipment_path='Shipment.csv',
        country_path='Country.csv',
        product_path='Product.csv'
    )
    
    # Display summary statistics
    print("\nMASTER DATASET SUMMARY:")
    print(master_data.describe())
    
    print("\nMONTHLY AGGREGATION SAMPLE:")
    print(agg_tables['monthly'].head(10))
