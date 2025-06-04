# Running the App with Streamlit

Follow these steps to run the app locally using Streamlit:


## App Overview

The interface consists of four main pages:

1. **Tournaments**: View all existing tournaments.
2. **Players**: Select a tournament to see the current standings in that tournament.
3. **Matches**: View ongoing matches.
4. **Admin**: Manage tournaments by selecting a winner for a match and overwriting the wins, losses, and draws of a player in a tournament.

## Prerequisites

1. Ensure you have Python installed (version 3.7 or higher).
2. Install Streamlit if not already installed. You can do this by running:
    ```bash
    pip install streamlit
    ```

## Steps to Run the App

1. Navigate to the directory where the app file is located. For example:
    ```bash
    cd ~/uvg-othello-server/frontend
    ```

2. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

3. Open your browser and go to the following URL:
    ```
    http://localhost:8501
    ```

    ## Environment Configuration

    4. Create a `.env` file in the same directory as the app. Add the following line to specify the backend URL:
        ```
        BASE_URL=http://your-backend-url
        ```

       Replace `http://your-backend-url` with the actual URL of your backend server.

## Troubleshooting

- If you encounter issues, ensure all required dependencies are installed.
- Check the terminal for error messages and resolve them accordingly.

Enjoy using the app!