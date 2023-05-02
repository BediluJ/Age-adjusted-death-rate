import streamlit as st
import pandas as pd
import altair as alt

# Load the data from the CSV file
url = "https://data.cdc.gov/api/views/bi63-dtpu/rows.csv?accessType=DOWNLOAD"
df = pd.read_csv(url)

# Define the sidebar
st.sidebar.title("Select cause of death:")
#cause_of_death = st.sidebar.selectbox("Cause of death:", df["Cause Name"].unique())
cause_of_death = st.sidebar.selectbox("Cause of death:", df["Cause Name"].unique()[1:],key="cause_of_death_selector")




# Filter the data based on the selected cause of death and calculate the age-adjusted death rate
filtered_df = df[df["Cause Name"] == cause_of_death]
age_adjusted_rate = filtered_df["Age-adjusted Death Rate"].mean()

# Define the tabs
tabs = ["Overview", "AADR in US", "AADR in each specific States", "Descriptions of cause of death"]
active_tab = st.sidebar.radio("Select a tab", tabs)

#define dictionaries
cause_descriptions = {
    "All causes": "All causes of death combined.",
    "CLRD": "CLRD stands for Chronic Lower Respiratory Disease. According to World Health Organization(WHO), Chronic respiratory diseases (CRDs) affect the airways and other structures of the lungs. Some of the most common are chronic obstructive pulmonary disease (COPD), asthma, occupational lung diseases and pulmonary hypertension. In addition to tobacco smoke, other risk factors include air pollution, occupational chemicals and dusts, and frequent lower respiratory infections during childhood. CRDs are not curable; however, various forms of treatment that help open the air passages and improve shortness of breath can help control symptoms and improve daily  life for people living with these conditions. For more information please visit [who.int](https://www.who.int/health-topics/chronic-respiratory-diseases#tab=tab_1).",
    "Diabetes": "Diabetes is a chronic (long-lasting) health condition that affects how your body turns food into energy. Your body breaks down most of the food you eat into sugar (glucose) and releases it into your bloodstream. When your blood sugar goes up, it signals your pancreas to release insulin. Insulin acts like a key to let the blood sugar into your body’s cells for use as energy. With diabetes, your body doesn’t make enough insulin or can’t use it as well as it should. When there isn’t enough insulin or cells stop responding to insulin, too much blood sugar stays in your bloodstream. Over time, that can cause serious health problems, such as heart disease, vision loss, and kidney disease. Should you be interested to learn more click [cdc.gov](https://www.cdc.gov/diabetes/basics/diabetes.html). ",
    "Heart disease": "Heart disease is the leading cause of death in the United States. The term “heart disease” refers to several types of heart conditions. In the United States, the most common type of heart disease is coronary artery disease (CAD), which can lead to heart attack. You can greatly reduce your risk for heart disease through lifestyle changes and, in some cases, medicine. For more information please visit [cdc.gov](https://www.cdc.gov/heartdisease/) .",
    "Influenza and pneumonia": "According to American Lung Association, Influenza (flu) is a highly contagious viral infection that is one of the most severe illnesses of the winter season. Influenza is spread easily from person to person, usually when an infected person coughs or sneezes. Pneumonia is a serious infection or inflammation of the lungs.The air sacs fill with pus and other liquid, blocking oxygen from reaching the bloodstream. If there is too little oxygen in the blood, the body's cells cannot work properly, which can lead to death. For more information please [click here](https://www.lung.org/lung-health-diseases/lung-disease-lookup/pneumonia) .",
    "Suicide": "Suicide is the act of deliberately killing oneself. Risk factors for suicide include mental disorder, especially depression, and neurological disorders, cancer and HIV infection."+
            " Suicide is a serious public health problem that can have lasting harmful effects on individuals, families, and communities. There are many factors that contribute to suicide."+
            " The goal of suicide prevention is to reduce factors that increase risk and increase factors that promote resilience. For more information visit [cdc.gov](https://www.cdc.gov/suicide/) .",
    "Kidney disease": "Chronic kidney disease, also called chronic kidney failure, involves a gradual loss of kidney function. Your kidneys filter wastes and excess fluids from your blood, which are then removed in your urine. Advanced chronic kidney disease can cause dangerous levels of fluid, electrolytes and wastes to build up in your body.more information can be found at [mayoclinic.org](https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521).",
    "Unintentional injuries": "Unintentional injuries consist of that subset of injuries for which there is no evidence of predetermined intent. The cause-specific unintentional injuries include road traffic injuries (RTIs), poisonings, falls, burns, and drowning.",
    "Alzheimer's disease": "Alzheimer’s disease is a brain disorder that slowly destroys memory and thinking skills and, eventually, the ability to carry out the simplest tasks. Alzheimer’s disease is the most common cause of dementia among older adults. Estimates vary, but experts suggest that more than 6 million Americans age 65 and older may have Alzheimer’s. Many more under age 65 also have the disease. [Click here](https://www.nia.nih.gov/health/what-alzheimers-disease) for more information.",
    "Cancer": "Cancer is a large group of diseases that can start in almost any organ or tissue of the body when abnormal cells grow uncontrollably, go beyond their usual boundaries to invade adjoining parts of the body and/or spread to other organs. More info can be found at [who.int](https://www.who.int/health-topics/cancer#tab=tab_1)",
    "Stroke": "A stroke, sometimes called a brain attack, occurs when something blocks blood supply to part of the brain or when a blood vessel in the brain bursts. In either case, parts of the brain become damaged or die. A stroke can cause lasting brain damage, long-term disability, or even death. More information can be found at [cdc.gov](https://www.cdc.gov/stroke/).",
}

# Define the contents of each tab
if active_tab == "Overview":
    st.markdown('''
# Age-Adjusted Death Rates in the United States, 1999-2017
''')
    st.write("Age-adjusted death rate (AADR) is a measure of mortality that takes into account the differences in age distribution between populations. It is calculated by adjusting the crude death rate (total number of deaths per 100,000 population) to account for differences in age distribution across populations.")
    st.write("By adjusting the death rate for differences in age distribution, the age-adjusted death rate provides a more accurate estimate of the true risk of death in a population and can help identify differences in mortality rates due to age, rather than other factors such as lifestyle, socioeconomic status, or access to healthcare.")
    st.write("Additional information about AADR can be found [here](https://schs.dph.ncdhhs.gov/schs/pdf/primer13_2.pdf).")
    st.write ("The age-adjusted death rate in the United States has decreased over time, but it can vary depending on the cause of death and the state. In this interactive app, by selecting different causes of death and different states, we can observe differences in the age-adjusted death rate. Therefore, it is important to understand these variations in order to address the underlying health issues and improve overall health outcomes in the United States.")
    st.write("Select a cause of death from the sidebar to view the age-adjusted death rate.")
elif active_tab == "AADR in US":
    # Display the line chart
    chart_data = filtered_df.groupby("Year")["Age-adjusted Death Rate"].mean().reset_index()
    chart = alt.Chart(chart_data).mark_line(color="red").encode(
        x=alt.X ("Year", axis=alt.Axis(format="")),
        y=alt.Y("Age-adjusted Death Rate", scale=alt.Scale(zero=False))
    )
    st.write("# Age-Adjusted Death Rate over Time")
    st.write(f"This line chart shows the age-adjusted death rate for {cause_of_death} in the United States over time.")
    st.write("The age-adjusted death rate is the number of deaths per 100,000 people, adjusted for differences in age distribution across the population.")
    st.write("Use the sidebar to select a different cause of death.")
    st.altair_chart(chart, use_container_width=True)
    st.write(f"Age-adjusted death rate for {cause_of_death} in the United States : {age_adjusted_rate:.2f}")
elif active_tab == "AADR in each specific States":
    # display Bar Chart  by State
    st.write("# Age-Adjusted Death Rate over Time in Each States")
    states = df['State'].unique().tolist()
    selected_state = st.selectbox('Select a state:', states) 
    filtered_df = df.loc[(df['State'] == selected_state) & (df['Cause Name'] == cause_of_death)]
    avg_rate = filtered_df['Age-adjusted Death Rate'].mean()
    bar_data = filtered_df.groupby(["Year"])[["Age-adjusted Death Rate"]].mean().reset_index()
    chart = alt.Chart(bar_data).mark_area(color="green").encode(
        x=alt.X("Year", axis=alt.Axis(format="")),
        y= alt.Y("Age-adjusted Death Rate", scale=alt.Scale(zero=False))        
    ).properties(
    title=f'Age-Adjusted Death Rates by {cause_of_death} as Cause of Death for {selected_state}.'
    )
    # Display chart
    st.altair_chart(chart, use_container_width=True)
    
    #avg_rate = filtered_df['Age-adjusted Death Rate'].mean()
    st.write(f"Age-adjusted death rate for {cause_of_death} in {selected_state}: {avg_rate:.2f}")

    
else:
    # Display the descriptions
    if active_tab == "Descriptions of cause of death":
        st.write(f"# Description of cause of death: {cause_of_death} ")
        st.write(cause_descriptions.get(cause_of_death, "No description available."))

        st.write("In this app, you can select a cause of death from the sidebar to view the age-adjusted death rate for that cause of death.")
        st.write(f"Age-adjusted death rate for {cause_of_death} in the United States : {age_adjusted_rate:.2f}")



