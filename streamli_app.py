# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie!")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The Name on your Smoothie will be...", name_on_order)

# Snowflake Session
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
st.dataframe(data=my_dataframe, use_container_width=True)

# Convert Snowpark DataFrame to a list
fruit_options = my_dataframe.to_pandas()["FRUIT_NAME"].tolist()

# Allow selection of up to 5 ingredients
ingredients_lists = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5  # Enforce a maximum of 5 selections
)

# Construct ingredients string
ingredients_string = " ".join(ingredients_lists) if ingredients_lists else ""

# Submit order button
if st.button("Submit Order"):
    if ingredients_string and name_on_order:
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered! {name_on_order}", icon="✅")
    else:
        st.error("Please enter a name and select at least one ingredient.")
