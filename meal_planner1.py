# -*- coding: utf-8 -*-
"""
Created on Sat Jun  7 15:21:14 2025

@author: hp
"""

import streamlit as st # Import Streamlit for creating web applications
import sqlite3 # Import SQLite for database management
import random # Import random for generating random meal plans
import matplotlib.pyplot as plt # Import Matplotlib for plotting graphs
import pandas as pd # Import Pandas for data manipulation
import time # Import time for adding delays

#Name of the page
st.set_page_config(
    page_title="Meal Planner", #Website name
    page_icon="🍽", #Emoji Icon
    layout="wide") #Page will wide open  

#Establish a connection to SQLite database
conn = sqlite3.connect("meal_planner.db", check_same_thread=False)
cursor = conn.cursor()

#Create a table for storing user data if it doesn't already exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS meal_plans (
    id INTEGER PRIMARY KEY, 
    day TEXT, 
    meal TEXT, 
    calories INTEGER, 
    protein INTEGER, 
    carbs INTEGER, 
    fats INTEGER
)
''')
conn.commit()

#Create table for user registrations
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT
)
''')
conn.commit()

#Recipe database
recipe_database = {
    #Vegetarian Recipes
    "Salad": {"ingredients": ["Pasta", "Tomato", "Cucumber", "Oregano", "Olive Oil"], 
              "calories": 400, "protein": 10, "carbs": 50, "fats": 15, "diet": "Vegetarian",
              "youtube_link": "https://m.youtube.com/watch?v=7k6CKTYZbp0"},
    
    "Veggie Stir-fry": {"ingredients": ["Carrot", "Broccoli", "Soy Sauce", "Tofu"], 
                         "calories": 350, "protein": 20, "carbs": 30, "fats": 10, "diet": "Vegetarian",
                         "youtube_link": "https://www.youtube.com/watch?v=UMPOIuq23Aw"},
    
    "Fruit Smoothie": {"ingredients": ["Banana", "Milk", "Honey", "Yogurt"], 
                        "calories": 200, "protein": 8, "carbs": 35, "fats": 5, "diet": "Vegetarian",
                        "youtube_link": "https://www.youtube.com/playlist?list=PLziprGSUFGYQkRGiC9i2Q3DQL7XIszhsf"},
    
    "Caprese Sandwich": {"ingredients": ["Bread", "Tomato", "Basil", "Mozzarella", "Olive Oil"], 
                          "calories": 320, "protein": 14, "carbs": 40, "fats": 12, "diet": "Vegetarian",
                          "youtube_link": "https://www.youtube.com/watch?v=TGltPhd0EQU"},
    
    "Vegetable Curry": {"ingredients": ["Potato", "Carrot", "Peas", "Coconut Milk", "Curry Paste"], 
                         "calories": 450, "protein": 12, "carbs": 55, "fats": 18, "diet": "Vegetarian",
                         "youtube_link": "https://www.youtube.com/watch?v=-7MrKfR1E8w"},
    
    "Paneer Tikka": {"ingredients": ["Paneer", "Yogurt", "Spices", "Lemon"], 
                      "calories": 300, "protein": 20, "carbs": 10, "fats": 20, "diet": "Vegetarian",
                      "youtube_link": "https://www.youtube.com/watch?v=pgnFBet5pbo"},
    
    "Lentil Soup": {"ingredients": ["Lentils", "Onion", "Tomato", "Garlic", "Cumin"], 
                     "calories": 290, "protein": 22, "carbs": 40, "fats": 5, "diet": "Vegetarian",
                     "youtube_link": "https://www.youtube.com/watch?v=mdT3tFEug00"},
    
    "Vegetable Biryani": {"ingredients": ["Rice", "Carrot", "Peas", "Onion", "Spices"], 
                           "calories": 500, "protein": 15, "carbs": 60, "fats": 15, "diet": "Vegetarian",
                           "youtube_link": "https://www.youtube.com/watch?v=Do7ZdUodDdw"},
    
    "Spinach Pasta": {"ingredients": ["Pasta", "Spinach", "Garlic", "Olive Oil", "Parmesan"], 
                       "calories": 480, "protein": 16, "carbs": 55, "fats": 20, "diet": "Vegetarian",
                       "youtube_link": "https://www.youtube.com/watch?v=Nz4bD2KxTg8"},
    
    #Non-Vegetarian Recipes
    "Chicken Soup": {"ingredients": ["Chicken", "Carrot", "Onion", "Garlic"], 
                      "calories": 300, "protein": 25, "carbs": 10, "fats": 8, "diet": "Non-Vegetarian",
                      "youtube_link": "https://www.youtube.com/watch?v=0xR2cC6Tea8"},
    
    "Grilled Chicken Breast": {"ingredients": ["Chicken Breast", "Olive Oil", "Garlic", "Lemon"], 
                                "calories": 220, "protein": 40, "carbs": 0, "fats": 8, "diet": "Non-Vegetarian",
                                "youtube_link": "https://www.youtube.com/watch?v=n2BrIfa3S0k"},
    
    "Beef Steak": {"ingredients": ["Beef", "Olive Oil", "Salt", "Pepper"], 
                   "calories": 400, "protein": 45, "carbs": 0, "fats": 25, "diet": "Non-Vegetarian",
                   "youtube_link": "https://www.youtube.com/watch?v=l9hUGbg0Ljo"},
    
    "Shrimp Stir-fry": {"ingredients": ["Shrimp", "Broccoli", "Soy Sauce", "Garlic"], 
                         "calories": 300, "protein": 35, "carbs": 20, "fats": 10, "diet": "Non-Vegetarian",
                         "youtube_link": "https://www.youtube.com/watch?v=fx_FljxGU58"},
    
    "Salmon With Veggies": {"ingredients": ["Salmon", "Olive Oil", "Lemon", "Broccoli"], 
                             "calories": 450, "protein": 42, "carbs": 10, "fats": 30, "diet": "Non-Vegetarian",
                             "youtube_link": "https://www.youtube.com/watch?v=qvfCWVh31Mg"}
}
# Function to register a new user
def register_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError: # Handle duplicate username error
        return False
    
#Function to validate user login
def login_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return cursor.fetchone() is not None # Return True if user exists

#Function to check existing users.
def fetch_existing_data(username):
    cursor.execute("SELECT day, meal, calories FROM meal_plans WHERE day IN (SELECT day FROM meal_plans)")
    data = cursor.fetchall()
    return pd.DataFrame(data, columns=["Day", "Meal", "Calories"])


# Function to suggest recipes based on ingredients and dietary preference
def suggest_recipes(user_ingredients, dietary_preference):
    suggested_recipes = []
    grocery_list = set()

    for recipe, details in recipe_database.items():
        if details["diet"] == dietary_preference:  # Apply dietary preference filter
            required_ingredients = set(details["ingredients"])
            available = required_ingredients.intersection(user_ingredients) # Find common ingredients
            missing = required_ingredients - user_ingredients # Find missing ingredients

    # Suggest recipes with available ingredients
            if available:
                suggested_recipes.append((recipe, details, missing))
                grocery_list.update(missing)

    return suggested_recipes, grocery_list

# Function to generate meal plan
def generate_meal_plan(suggested_recipes, days=1):
    with st.spinner("Loading your meal plan!"):
     time.sleep(3) 
    meal_plan = {} #Initialize an empty dictionary to store the meal plan for each day.

    #Loop to generate a plan for each day.
    for day in range(1, days + 1):
        daily_plan = random.sample(suggested_recipes, min(3, len(suggested_recipes))) #Randomly select up to 3 unique recipes.

        meal_plan[f"Day {day}"] = {
            "Breakfast": daily_plan[0] if len(daily_plan) > 0 else None,
            "Lunch": daily_plan[1] if len(daily_plan) > 1 else None,
            "Dinner": daily_plan[2] if len(daily_plan) > 2 else None,
        }

        for meal_type, recipe_data in meal_plan[f"Day {day}"].items():  #Insert each meal into the database if it exists.
            if recipe_data:
                recipe, details, _ = recipe_data
                cursor.execute('''
                INSERT INTO meal_plans (day, meal, calories, protein, carbs, fats)
                VALUES (?, ?, ?, ?, ?, ?)''',
                (f"Day {day}", recipe, details["calories"], details["protein"], details["carbs"], details["fats"]))
    
    conn.commit()
    return meal_plan

# Function to plot nutrition comparison
def plot_nutrition_comparison(meal_plan):
    days = []
    total_calories = []
    total_protein = []
    total_carbs = []
    total_fats = []

    for day, meals in meal_plan.items():
        # Iterate through each day and its corresponding meals.
        total_cals, total_protein_amt, total_carbs_amt, total_fats_amt = 0, 0, 0, 0
        for meal_type, recipe_data in meals.items():# Iterate through the meals (Breakfast, Lunch, Dinner).
            if recipe_data:
                _, details, _ = recipe_data
                total_cals += details["calories"]
                total_protein_amt += details["protein"]
                total_carbs_amt += details["carbs"]
                total_fats_amt += details["fats"]
        
        days.append(day)
        total_calories.append(total_cals)
        total_protein.append(total_protein_amt)
        total_carbs.append(total_carbs_amt)
        total_fats.append(total_fats_amt)

    df = pd.DataFrame({"Days": days, "Protein": total_protein, "Carbs": total_carbs, "Fats": total_fats})
    df.set_index("Days", inplace=True)

    st.write("## Nutrition Comparison Chart")
    st.bar_chart(df)

    # Line chart for Calories
    df_calories = pd.DataFrame({"Days": days, "Calories": total_calories})
    df_calories.set_index("Days", inplace=True)
    
    st.write("## Calories Trend Over Days")
    st.line_chart(df_calories)

# Function to plot pie chart for selected meal
def plot_pie_chart(meal_name):
    if meal_name in recipe_database:
        meal_data = recipe_database[meal_name]
        labels = ["Protein", "Carbs", "Fats"]
        sizes = [meal_data["protein"], meal_data["carbs"], meal_data["fats"]]
        colors = ["#FF6F61", "#6B5B95", "#88B04B"]  # Coral, Indigo, Lime Green

        fig, ax = plt.subplots() # Create a figure and axis 
        ax.set_facecolor("black")  # Set background to black
        fig.patch.set_facecolor("black")  # Set figure background to black
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct='%1.1f%%', startangle=140,
            colors=colors, textprops={'color': "white"}
        )

        # Customize font size and weight
        for text in texts + autotexts:
            text.set_fontsize(12)
            text.set_fontweight('bold')

        ax.set_title(f"Macronutrient Breakdown: {meal_name}", color="white")
        st.pyplot(fig)
        
# Main program
def main():
   st.title("Smart Recipe Generator & Meal Planner") # Set the title of the app.
   tab1, tab2, tab3 = st.tabs(["Signup/Login", "Recipe Suggestions", "Meal Planner and Analysis"])
   with tab1:
    menu = ["Login", "Signup"]
    choice = st.sidebar.selectbox("Choose an option:", menu)

    if choice == "Signup":
        st.subheader("Create a New Account")
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        if st.button("Signup"):
            if register_user(new_username, new_password):
                st.success("Account created successfully! You can now log in.")
            else:
                st.error("Username already exists. Please choose a different one.")
    
    elif choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(username, password):
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid credentials. Please try again.")

   with tab2:
    st.subheader("Recipes List")
    dietary_preference = st.radio("Select your dietary preference:", ["Vegetarian", "Non-Vegetarian"])

    # Filter ingredients based on dietary preference
    filtered_ingredients = sorted({i for recipe, details in recipe_database.items() 
                                    if details["diet"] == dietary_preference 
                                    for i in details["ingredients"]})

    # Select ingredients
    user_ingredients = st.multiselect("Select available ingredients:", filtered_ingredients)

    if user_ingredients:
        user_ingredients_set = set(user_ingredients)
        suggested_recipes, grocery_list = suggest_recipes(user_ingredients_set, dietary_preference)

        if suggested_recipes:
            st.write("## Suggested Recipes")
            for recipe, details, missing in suggested_recipes:
                st.write(f"- {recipe} ({details['calories']} kcal) | Missing: {', '.join(missing) if missing else 'None'}")

   with tab3:  
    st.subheader("Meal Planner & Analysis")        
    days = st.slider("Generate meal plan for how many days?", 1, 7, 1)

    # Ensure that suggested_recipes and grocery_list are correctly available
    if "suggested_recipes" not in locals() or "grocery_list" not in locals():
        st.warning("❌ No matching recipes found. Go to 'Recipe Suggestions' and select ingredients first!")
    else:
        if st.button("Generate Meal Plan"):
            meal_plan = generate_meal_plan(suggested_recipes, days)

            # Display meal plan in a table
            df_meal_plan = pd.DataFrame({
                day: {
                    "Breakfast": meals["Breakfast"][0] if meals["Breakfast"] else "N/A",
                    "Lunch": meals["Lunch"][0] if meals["Lunch"] else "N/A",
                    "Dinner": meals["Dinner"][0] if meals["Dinner"] else "N/A",
                }
                for day, meals in meal_plan.items()
            }).T #transposes the dataframe

            st.write("### Your Meal Plan")
            st.table(df_meal_plan)

            # Show YouTube links for suggested recipes
            st.write("## Watch Recipe Videos")
            for day, meals in meal_plan.items():
                for meal_type, recipe_data in meals.items():
                    if recipe_data:
                        recipe_name, details, _ = recipe_data
                        youtube_link = details.get("youtube_link", "")
                        st.markdown(f" [{recipe_name} - {meal_type}]({youtube_link})")

            # Plot nutrition comparison
            plot_nutrition_comparison(meal_plan)

            # Use st.expander for Grocery List
            with st.expander("View Missing Ingredients (Grocery List)"):

                if grocery_list:
                    st.write(", ".join(grocery_list))
                else:
                    st.success("🎉 You have all the required ingredients!")

    # Move Pie Chart inside tab3 only
    st.write("## Macronutrients for a Dish")
    meal_to_compare = st.selectbox("Select a meal to visualize macronutrient distribution:", 
                                    [recipe for recipe, details in recipe_database.items() if details["diet"] == dietary_preference])
    if meal_to_compare:
        plot_pie_chart(meal_to_compare)

if __name__ == "__main__":
    main()

