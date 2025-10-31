import pandas as pd
import numpy as np

# --- Configuration ---
INPUT_FILE = 'customers-100.xlsx' 
OUTPUT_FILE = 'cleaned_customers-100.csv'

try:
    # --- Step 1: Data Ingestion ---
    # Use pd.read_excel for .xlsx files (requires 'openpyxl' to be installed)
    df = pd.read_excel(INPUT_FILE)

    print("--- 1. Initial Data Info (Before Cleaning) ---")
    df.info()
    print(f"\nOriginal row count: {len(df)}")

    # --- Step 2: Deduplication ---
    print("\n--- 2. Deduplication ---")

    # Check for and remove any 100% identical rows
    initial_duplicates = df.duplicated().sum()
    if initial_duplicates > 0:
        print(f"Found and removed {initial_duplicates} fully duplicate rows.")
        df = df.drop_duplicates(keep='first')
    else:
        print("No fully duplicate rows found.")

    # Check for and remove duplicates based on the 'Customer Id'
    id_duplicates = df.duplicated(subset=['Customer Id']).sum()
    if id_duplicates > 0:
        print(f"Found and removed {id_duplicates} rows with duplicate Customer IDs.")
        df = df.drop_duplicates(subset=['Customer Id'], keep='first')
    else:
        print("No duplicate Customer IDs found.")


    # --- Step 3: Column Management ---
    print("\n--- 3. Column Management ---")
    
    # A) Drop the 'Index' column, as it's not needed
    if 'Index' in df.columns:
        df = df.drop(columns=['Index'])
        print("Dropped 'Index' column.")

    # B) Standardize all column names to lowercase_with_underscores
    print("Standardizing column names (e.g., 'Customer Id' -> 'customer_id').")
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')


    # --- Step 4: Missing Value Handling ---
    print("\n--- 4. Missing Value Handling ---")
    
    # Your info showed 100 non-null values, but this is good practice.
    original_rows = len(df)
    df = df.dropna(subset=['customer_id']) # 'Customer Id' is now 'customer_id'
    rows_dropped = original_rows - len(df)
    if rows_dropped > 0:
        print(f"Dropped {rows_dropped} rows with a missing 'customer_id'.")
    else:
        print("No rows with missing customer_id found.")

    if 'email' in df.columns:
        missing_emails = df['email'].isna().sum()
        if missing_emails > 0:
            print(f"Filled {missing_emails} missing 'email' values with 'N/A'.")
            df['email'] = df['email'].fillna('N/A')


    # --- Step 5: Data Type Correction ---
    print("\n--- 5. Data Type Correction ---")
    
    # Your df.info() showed 'subscription_date' was already correct. This will just confirm.
    if 'subscription_date' in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df['subscription_date']):
            print("Column 'subscription_date' is already in the correct datetime format.")
        else:
            print("Converting 'subscription_date' to datetime.")
            df['subscription_date'] = pd.to_datetime(df['subscription_date'], errors='coerce')


    # --- Step 6: Format Standardization ---
    print("\n--- 6. Format Standardization ---")
    
    # A) Standardize all text columns to lowercase and strip whitespace
    text_columns = ['first_name', 'last_name', 'company', 'city', 'country', 
                    'phone_1', 'phone_2', 'email', 'website']

    print(f"Standardizing text columns (lowercase, strip whitespace)...")
    for col in text_columns:
        if col in df.columns:
            # Convert to string type first to be safe
            df[col] = df[col].astype(str).str.lower().str.strip()
            
    # B) Clean phone number columns by removing all non-numeric characters
    print("Standardizing phone number columns (removing non-numeric characters)...")
    phone_cols = ['phone_1', 'phone_2']
    for col in phone_cols:
        if col in df.columns:
            # Replace anything that is NOT a digit (\d) with an empty string
            df[col] = df[col].astype(str).str.replace(r'[^\d]', '', regex=True)


    # --- Final Review ---
    print(f"\n--- 7. Final Data Info (After Cleaning) ---")
    df.info()
    print(f"\nOriginal row count: {pd.read_excel(INPUT_FILE).shape[0]}")
    print(f"Cleaned row count: {len(df)}")

    # --- Save the Cleaned Data ---
    # We save the clean file as a CSV, which is a standard, easy-to-use format.
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSuccessfully cleaned data and saved to '{OUTPUT_FILE}'")
    
    print("\n--- First 5 Rows of Cleaned Data (Note the clean phone numbers) ---")
    print(df.head())


except FileNotFoundError:
    print(f"Error: The file '{INPUT_FILE}' was not found.")
    print(f"Please make sure the file is in the same folder as your script.")
except ModuleNotFoundError:
    print("\n--- ERROR ---")
    print("You are missing the 'openpyxl' library, which is needed to read Excel files.")
    print("Please install it by running this command in your terminal:")
    print("pip install openpyxl")
except Exception as e:
    print(f"\nAn error occurred: {e}")
    print("Please check your column names and file contents.")
