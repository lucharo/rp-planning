import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


st.set_page_config(layout='wide')

# Reference data from Dr. Mike Israetel
reference_df = pd.read_csv('ref.csv')

workout_df = pd.DataFrame({
        "Exercise Name": ["T-Bar row", "Lat Pulldown", "Face Pull", "Lateral Raise", "Upright row", "OH Press", "Chest press"],
        "Sets": [3, 3, 4, 3, 3, 3, 3],
        "Target Muscle": ["Back", "Back", "Rear Delts", "Side Delts", "Side Delts", "Front Delts", "Chest"],
    })

st.title("Renaissance Periodization Workout Planner")

st.header("Your Workout Plan")

num_sessions = st.number_input('How many times do you do this workout per week?',
                                min_value = 0, step = 1, value = 2)

workout_df = pd.merge(
    workout_df, reference_df[['Body Part', 'MEV', 'MRV']], 
    left_on='Target Muscle', right_on='Body Part', how='left'
    )

def calculate_volumes(row, num_sessions):
    total_weekly_sets = row['Sets'] * num_sessions
    achieved_mev = (total_weekly_sets / row['MEV']) if row['MEV'] else 0
    achieved_mrv = (total_weekly_sets / row['MRV']) if row['MRV'] else 0
    return achieved_mev, achieved_mrv

# Applying the calculation to each row
workout_df[['%MEV per week', '%MRV per week']] = workout_df.apply(
    lambda row: calculate_volumes(row, num_sessions), axis=1, result_type='expand'
    )

# Data editor for the workout table with dynamic rows
edited_df = st.data_editor(
    workout_df[['Exercise Name', 'Sets', 'Target Muscle',
                '%MEV per week', '%MRV per week']], 
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "Sets": st.column_config.NumberColumn(
            "Sets",
            help="Number of set per workout session",
            default=3,
            min_value=1,
            step=1,
            required=True,
        ),
        "Target Muscle": st.column_config.SelectboxColumn(
            "Target Muscle",
            help="Main muscle for this exercise",
            options=reference_df['Body Part'],
            required=True,
        ),
        "%MEV per week": st.column_config.ProgressColumn(
            "%MEV per week",
            help="Percent of sets completed relative to MEV for this muscle group",
        ),
        "%MRV per week": st.column_config.ProgressColumn(
            "%MRV per week",
            help="Percent of sets completed relative to MRV for this muscle group",
        ),
    },
)

# Checkbox to show all target groups
show_all_groups = st.checkbox('Show all target muscle groups', value=False)


# Prepare data for plotting
plot_data = workout_df.groupby('Target Muscle', sort = False).agg({
    'Sets': 'sum',
    'MEV': 'first',  # Assuming MEV is the same for each exercise targeting the same muscle
    'MRV': 'first'   # Assuming MRV is the same for each exercise targeting the same muscle
}).reset_index()

if show_all_groups:
    # Use reference_df to include all target muscle groups
    all_groups_plot_data = reference_df[['Body Part', 'MEV', 'MRV']].drop_duplicates()
    all_groups_plot_data.rename(columns={'Body Part': 'Target Muscle'}, inplace=True)
    all_groups_plot_data['Sets'] = 0  # Default to 0 sets for muscle groups not in the workout
    all_groups_plot_data['Weekly Volume'] = 0  # Default to 0 as well

    # Append the workout data to include in the plot
    all_groups_plot_data = pd.concat([all_groups_plot_data.set_index('Target Muscle'), plot_data.set_index('Target Muscle')], axis=0)
    all_groups_plot_data.reset_index(inplace=True)
    all_groups_plot_data.drop_duplicates(subset='Target Muscle', keep='last', inplace=True)
    
    plot_data = all_groups_plot_data


# Calculate total current weekly volume (Sets * num_sessions)
plot_data['Weekly Volume'] = plot_data['Sets'] * num_sessions
plot_data['Training Status'] = plot_data.apply(lambda row: 'Undertraining' if row['Weekly Volume'] < row['MEV'] else ('Overtraining' if row['Weekly Volume'] > row['MRV'] else 'Productive')
, axis=1)

# Creating the Plotly figure
fig = px.scatter(plot_data, x = "Target Muscle", y = "Weekly Volume", color = "Training Status") 

fig.update_traces(hovertemplate = "Current volume: %{y} sets<extra></extra>")

for index, row in plot_data.iterrows():
    # Adding MEV and MRV lines
    fig.add_trace(go.Scatter(
        x=[row['Target Muscle'], row['Target Muscle']],
        y=[row['MEV'], row['MRV']],
        text = ["MEV", "MRV"],
        hoverinfo = ["text+y", "text+y"],
        hovertemplate = "%{text}: %{y} sets<extra></extra>",
        mode='lines',
        line=dict(color='grey', dash='dash'),
        showlegend=False
    ))

fig.update_layout(
    title='Current Volume per Muscle Group',
    xaxis_title='Muscle Group',
    yaxis_title='% Volume',
    barmode='group'
)

# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

with st.expander("**Note:** Aim to increase volume week by week in your mesocycle until hitting the MRV. Expand for an example", expanded=False):
    st.markdown("""
    ###### Example Mesocycle Table
    - Week 1: 12 sets **(MEV)**
    - Week 2: 14 sets
    - Week 3: 16 sets
    - Week 4: 18 sets
    - Week 5: 20 sets **(MRV)**
    - Week 6: 6 sets **(deload)**
    """)

    # Example scheduling data
    scheduling_data = {
        "Week": ["1", "2", "3", "4", "5", "6<br>(Deload)"],
        "Sets": [12, 14, 16, 18, 20, 6]
    }

    schedule_df = pd.DataFrame(scheduling_data)

    # Creating the Plotly figure for scheduling
    schedule_fig = go.Figure(data=[
        go.Scatter(x=schedule_df['Week'], y=schedule_df['Sets'])
    ])

    schedule_fig.update_layout(
        title='Example Mesocycle Graph',
        xaxis_title='Week Number',
        yaxis_title='Number of Sets',
        xaxis = {'type' : 'category'}
    )

    # Display the scheduling plot in Streamlit
    st.plotly_chart(schedule_fig)




# Expandable section for the reference table
with st.expander("Reference Table and Sources", expanded=False):
        st.table(reference_df)
        st.markdown("### Sources")
        st.markdown("- [Dr. Mike Israetel's Training Tips for Hypertrophy from Reddit](https://www.reddit.com/r/weightroom/comments/6674a4/dr_mike_israetels_training_tips_for_hypertrophy/)")
        st.markdown("- [Google Sheets Link to the Volume Recommendations](https://docs.google.com/spreadsheets/d/14eG45XqAG8e-_bE8jq-yjh2Vd_orwRHo4hcbWPhzpvE/edit#gid=0)")
        st.markdown("- [RP's Main Article on Volume Landmarks](https://rpstrength.com/blogs/articles/training-volume-landmarks-muscle-growth)")

        st.markdown("### Glossary [[source]](https://rpstrength.com/blogs/articles/bicep-hypertrophy-training-tips)")
        st.markdown("""
        **MV** - Maintenance Volume = The amount you need to train in order to keep the muscle you have in the context of a whole body training program.
                    
        **MEV** - Minimum Effective Volume = The amount you need to train in order to make any measurable improvements in muscle mass over time in the context of a whole body training program.
        
        **MAV** - Maximum Adaptive Volume = The average amount of training volume over time that is likely to lead to your best long term gains in muscle mass in the context of a whole body training program.
        
        **MRV** - Maximum Recoverable Volume = The maximum amount of volume you can train with regularly and still barely recover from in the context of a whole body training program. Doing more than this would cause worse results than doing less.
        """)

