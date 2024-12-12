import streamlit as st
import pandas as pd
from data import fetch_all_profiles, sort_by_ranking, sort_by_problems_solved, sort_by_badges
from visualization import create_bar_chart

# Cache data fetching for optimization
@st.cache_data
def fetch_and_sort_profiles(usernames):
    """Fetch profiles and sort by ranking."""
    profiles = fetch_all_profiles(usernames)
    return sort_by_ranking(profiles)

@st.cache_data
def filter_profiles(df, query):
    """Filter profiles based on a search query."""
    return df[df["Username"].str.contains(query, case=False, na=False)]

def ranking_table():
    st.write("### Ranking Table")
    upload_file = st.file_uploader("Upload a file with usernames (one per line)", type=["txt", "csv"])

    usernames = []

    # Fetch usernames from file or manual input
    if upload_file is not None:
        file_content = upload_file.read().decode("utf-8")
        usernames = [username.strip() for username in file_content.splitlines() if username.strip()]
        st.write(f"Fetched {len(usernames)} usernames from the uploaded file.")
        usernames = list(set(usernames))
        st.session_state.usernames = usernames
    else:
        usernames_input = st.text_area("Enter LeetCode usernames (comma separated):")
        if usernames_input:
            usernames = [username.strip() for username in usernames_input.split(",") if username.strip()]
            st.write(f"Fetching data for {len(usernames)} usernames...")
            usernames = list(set(usernames))
            st.session_state.usernames = usernames

    if usernames:
        with st.spinner("Fetching profiles..."):
            # Fetch and sort profiles
            profiles = fetch_and_sort_profiles(usernames)
            df = pd.DataFrame(profiles)

            # Add hyperlinks to usernames
            df["Username"] = df.apply(
                lambda row: f"<a href='{row['Profile URL']}' target='_blank' style='text-decoration:none; color:black;'>{row['Username']}</a>",
                axis=1
            )

            # Set index and drop unnecessary columns
            df.index = range(1, len(df) + 1)
            df.index.name = "Rank"
            df.drop(columns=["Profile URL"], inplace=True)

            # Search functionality
            st.write("#### Search for a Username")
            search_query = st.text_input("Enter a username to search:")
            if search_query:
                # Filter results only when the user submits the search query
                filtered_df = filter_profiles(df, search_query)

                if not filtered_df.empty:
                    st.write("### Filtered Results")
                    st.markdown(filtered_df.to_markdown(index=True), unsafe_allow_html=True)
                else:
                    st.warning("No matching usernames found.")
            else:
                st.write("### All User Profiles")
                st.markdown(df.to_markdown(index=True), unsafe_allow_html=True)

def compare_profiles():
    st.write("### Compare Profiles")
    if "usernames" not in st.session_state:
        st.write("Please upload a file or enter usernames in the Ranking Table page first.")
        return

    usernames = st.session_state.usernames
    with st.spinner("Fetching profiles for comparison..."):
        results = fetch_all_profiles(usernames)
        ranked_results = sort_by_ranking(results)
        df_comparison = pd.DataFrame(ranked_results)

        st.write("### Top 3 Users by LeetCode Ranking")
        st.dataframe(df_comparison[["Username", "LeetCode Ranking"]].head(3))

        st.write("### Top 3 Users by Problems Solved")
        sorted_by_problems = sort_by_problems_solved(ranked_results)
        st.dataframe(pd.DataFrame(sorted_by_problems)[["Username", "Total"]].head(3))

        st.write("### Top 3 Users by Number of Badges")
        sorted_by_badges = sort_by_badges(ranked_results)
        st.dataframe(pd.DataFrame(sorted_by_badges)[["Username", "Number of Badges"]].head(3))

        st.write("### Comparison Visualization")
        fig = create_bar_chart(df_comparison.head(100), "Username", "LeetCode Ranking", 
                               "Top Users by LeetCode Ranking", "Users", "Ranking")
        st.plotly_chart(fig)

        fig = create_bar_chart(df_comparison.head(100), "Username", "Total", 
                               "Top Users by Problems Solved", "Users", "Problems Solved")
        st.plotly_chart(fig)

        fig = create_bar_chart(df_comparison.head(100), "Username", "Number of Badges", 
                               "Top Users by Number of Badges", "Users", "Badges")
        st.plotly_chart(fig)

def about_page():
    st.write("""
    ### About This App

    The **LeetCode Profile Fetcher** allows you to fetch profile data for LeetCode users. You can either:
    - **Upload a file** with LeetCode usernames (one per line) to fetch their profile data.
    - **Manually input usernames** separated by commas.
    
    Once the data is fetched, the app displays:
    - **LeetCode ranking**
    - **Problems solved by difficulty (Easy, Medium, Hard)**
    - **Badges earned**

    ### Developer Information:
    - **Developed by:** Nischitha Vutla
    - **Contact me at:** 22951A6677@iare.ac.in
    """)

def main():
    st.title("LeetCode Profile Fetcher")
    page = st.sidebar.selectbox("Select a page", ["Ranking Table", "Compare Profiles", "About"])

    if page == "Ranking Table":
        ranking_table()
    elif page == "Compare Profiles":
        compare_profiles()
    elif page == "About":
        about_page()

if __name__ == "__main__":
    main()
