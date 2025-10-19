# Overview

This is a Streamlit web application that integrates with the Jow API to provide a recipe discovery platform focused on African-European fusion cuisine. The application allows users to browse recipes from both Jow.fr and a curated database of traditional African recipes, view detailed information, save favorites, apply advanced filters, and export shopping lists. All user data is persisted in a PostgreSQL database.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit - chosen for rapid prototyping and Python-native web development
- **Layout**: Wide layout with expanded sidebar for navigation and filtering
- **Rationale**: Streamlit enables quick development of data-driven applications with minimal frontend code, ideal for recipe browsing interfaces

## Backend Architecture
- **Language**: Python
- **API Integration**: Custom Jow API client (`jow_api.py` module)
- **Session Management**: Streamlit's built-in session state for user interactions
- **Rationale**: Python provides seamless integration between Streamlit, API calls, and database operations

## Data Storage
- **Database**: PostgreSQL
- **Connection**: Direct psycopg2 driver using environment variable `DATABASE_URL`
- **Schema Design**:
  - `favorites` table: Stores user's favorite recipes with full ingredient data
    - Columns: recipe_id (unique), recipe_name, recipe_url, recipe_description
    - Times: preparation_time, cooking_time, covers_count
    - ingredients_data: Serialized ingredient list (pipe-separated format)
    - created_at timestamp for tracking when favorited
  - `search_history` table: Tracks all user searches for recommendation system
    - Columns: search_query, search_date, results_count
    - Indexed by search_date for fast retrieval
  - `african_recipes` table: Curated traditional African recipes
    - Columns: name, description, ingredients, preparation_steps
    - Times and serves data, country_origin
    - Pre-populated with 10 traditional recipes (Thiéboudienne, Mafé, Jollof, etc.)
- **Initialization**: Database tables auto-created on first app launch
- **Rationale**: PostgreSQL chosen for robust relational data storage with ACID compliance, essential for maintaining data integrity across favorites, history, and recipe collections

## Key Features

### Search & Discovery
- **Dual Search**: Searches both Jow API and local African recipes database simultaneously
- **Smart Substitution**: Automatically suggests European ingredient alternatives for African ingredients
- **Fusion Mode**: Generates creative suggestions for combining African and European cooking styles

### Personalization
- **Favorites System**: Save recipes with heart button, includes full ingredient data
- **Search Recommendations**: Shows frequently searched terms based on 30-day history
- **Advanced Filters**: Filter by prep time, cook time, and number of servings

### Shopping & Planning
- **Shopping List Export**: Generates downloadable text file with:
  - All favorited recipes and their ingredients
  - Consolidated ingredient list aggregating quantities across all recipes
- **Recipe Details**: Full ingredient lists, preparation steps, cooking times

### African Recipe Integration
- **Curated Database**: 10 traditional African recipes pre-loaded
- **Full Details**: Each includes ingredients, preparation steps, origin country
- **Mixed Results**: African recipes appear alongside Jow results in searches

## Authentication & Authorization
- Single-user application (no login required)
- Database access controlled via environment variables
- All data persists across sessions via PostgreSQL

# External Dependencies

## Third-Party APIs
- **Jow API**: Primary recipe data source providing African-European fusion recipes
  - Custom client implementation in `jow_api.py`
  - Provides recipe search, details, and metadata

## Database Services
- **PostgreSQL**: Cloud-hosted or local PostgreSQL instance
  - Connection string via `DATABASE_URL` environment variable
  - Requires database provisioning before application launch

## Python Packages
- `streamlit`: Web application framework
- `psycopg2`: PostgreSQL database adapter
- `typing`: Type hints for better code clarity

## Environment Configuration
- `DATABASE_URL`: PostgreSQL connection string (required)
- Application expects environment variables to be configured in Replit secrets or similar mechanism