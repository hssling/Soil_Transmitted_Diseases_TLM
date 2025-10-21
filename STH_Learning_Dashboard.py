#!/usr/bin/env python3
"""
Interactive STH Learning Dashboard
Comprehensive Streamlit application for Soil Transmitted Diseases education
Includes all medical aspects with special focus on prevention and control
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="STH Learning Dashboard",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure colors and styling
INDIAN_COLORS = ['#FF9933', '#138808', '#000080', '#FFFFFF', '#FF0000']
sns.set_palette(INDIAN_COLORS)

# Load data (use dummy data if real data unavailable)
@st.cache_data
def load_sth_data():
    """Load STH epidemiological data with fallback to dummy data"""
    try:
        data_path = Path("Visual_Assets_Indian_Context/Indian_STH_Data.xlsx")
        if data_path.exists():
            df = pd.read_excel(data_path, engine='openpyxl')
        else:
            df = pd.read_excel(data_path, engine='xlrd')
    except:
        # Generate comprehensive dummy data
        np.random.seed(42)
        states = ['Maharashtra', 'Uttar Pradesh', 'Bihar', 'West Bengal', 'Madhya Pradesh',
                 'Tamil Nadu', 'Rajasthan', 'Karnataka', 'Gujarat', 'Odisha',
                 'Telangana', 'Punjab', 'Chhattisgarh', 'Haryana', 'Delhi']
        districts_data = []
        for state in states:
            for i in range(10):  # 10 districts per state
                prevalence_base = np.random.uniform(8, 65)
                district_data = {
                    'State': state,
                    'District': f'{state[:3]}_{i+1:02d}',
                    'Prevalence_Ascaris': np.clip(prevalence_base + np.random.normal(0, 8), 0, 100),
                    'Prevalence_Trichuris': np.clip(prevalence_base * 0.75 + np.random.normal(0, 5), 0, 100),
                    'Prevalence_Hookworm': np.clip(prevalence_base * 0.85 + np.random.normal(0, 7), 0, 100),
                    'Prevalence_Children': np.clip(prevalence_base + np.random.normal(0, 12), 0, 100),
                    'Total_Population': int(np.random.uniform(300000, 3000000)),
                    'Children_1_14': int(np.random.uniform(60000, 600000)),
                    'Risk_Category': np.random.choice(['High', 'Moderate', 'Low'], p=[0.35, 0.45, 0.2]),
                    'Sanitation_Index': np.random.uniform(0.3, 0.95),
                    'Treatment_Coverage': np.random.uniform(0.4, 0.9)
                }
                districts_data.append(district_data)
        df = pd.DataFrame(districts_data)
    return df

# Load content from markdown files
@st.cache_data
def load_content():
    """Load content from various markdown files"""
    content = {}
    files_to_load = [
        'Student_Notes_STH.md',
        'Presentation_Slides_STH.md'
    ]

    for filename in files_to_load:
        filepath = Path(filename)
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                content[filename] = f.read()
        else:
            content[filename] = f"# {filename}\nContent not found."

    return content

def main():
    """Main dashboard application"""
    # Load data
    sth_data = load_sth_data()
    content = load_content()

    # Sidebar navigation
    with st.sidebar:
        st.title("🦟 STH Learning Dashboard")
        st.markdown("---")

        # User progress tracking
        if 'progress' not in st.session_state:
            st.session_state.progress = {
                'introduction': False,
                'epidemiology': False,
                'etiology': False,
                'clinical': False,
                'diagnosis': False,
                'treatment': False,
                'prevention': False,
                'quiz': False
            }

        # Navigation menu
        selected_page = st.selectbox(
            "📚 Learning Modules",
            ["🏠 Dashboard Overview",
             "📊 Epidemiology & Burden",
             "🦠 Etiology & Life Cycles",
             "🏥 Clinical Manifestations",
             "🔬 Diagnosis Methods",
             "💊 Treatment & Management",
             "🛡️ Prevention & Control",  # Special emphasis
             "🇮🇳 Indian Context",
             "📝 Assessment Quiz",
             "📚 References"]
        )

        st.markdown("---")
        st.subheader("📈 Your Progress")

        # Progress indicators
        total_modules = len([k for k in st.session_state.progress.keys() if k != 'introduction'])
        completed_modules = sum(st.session_state.progress.values())

        progress_bar = st.progress(completed_modules / total_modules)
        st.write(f"**{completed_modules}/{total_modules}** modules completed")

        # Quick stats
        st.markdown("---")
        st.subheader("📊 Key Statistics")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Global Burden", "1.5B", "infected")
            st.metric("India", "225M", "cases")
        with col2:
            st.metric("DALYs", "4.98M", "annually")
            st.metric("Prevention", "MDA + WASH", "strategy")

    # Main content area
    if selected_page == "🏠 Dashboard Overview":
        render_dashboard_overview(sth_data)
    elif selected_page == "📊 Epidemiology & Burden":
        render_epidemiology(sth_data)
        st.session_state.progress['epidemiology'] = True
    elif selected_page == "🦠 Etiology & Life Cycles":
        render_etiology()
        st.session_state.progress['etiology'] = True
    elif selected_page == "🏥 Clinical Manifestations":
        render_clinical()
        st.session_state.progress['clinical'] = True
    elif selected_page == "🔬 Diagnosis Methods":
        render_diagnosis()
        st.session_state.progress['diagnosis'] = True
    elif selected_page == "💊 Treatment & Management":
        render_treatment()
        st.session_state.progress['treatment'] = True
    elif selected_page == "🛡️ Prevention & Control":
        render_prevention_control(sth_data)  # Special emphasis
        st.session_state.progress['prevention'] = True
    elif selected_page == "🇮🇳 Indian Context":
        render_indian_context(sth_data)
    elif selected_page == "📝 Assessment Quiz":
        render_quiz()
        st.session_state.progress['quiz'] = True
    elif selected_page == "📚 References":
        render_references(content)

def render_dashboard_overview(sth_data):
    """Render main dashboard overview"""
    st.title("🦟 Soil Transmitted Diseases (STH)")
    st.subheader("Interactive Learning Dashboard for MBBS 3rd Year Students")

    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Global Infected Population",
            value="1.5 Billion",
            delta="24% of world population"
        )

    with col2:
        st.metric(
            label="India Burden",
            value="225 Million",
            delta="Highest absolute burden"
        )

    with col3:
        st.metric(
            label="Annual DALYs",
            value="4.98 Million",
            delta="Economic impact: $7-12B"
        )

    with col4:
        st.metric(
            label="Prevention Success",
            value="MDA + WASH",
            delta="WHO strategy"
        )

    st.markdown("---")

    # Interactive overview
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📊 Epidemiological Overview")

        # State-wise prevalence chart
        fig = px.bar(
            sth_data.groupby('State')['Prevalence_Ascaris'].mean().reset_index().sort_values('Prevalence_Ascaris', ascending=False).head(10),
            x='State',
            y='Prevalence_Ascaris',
            color='State',
            color_discrete_sequence=INDIAN_COLORS,
            title='Top 10 States by Ascaris Prevalence'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🦠 Major Parasites")
        parasite_data = pd.DataFrame({
            'Parasite': ['Ascaris lumbricoides', 'Trichuris trichiura', 'Hookworms'],
            'Global Cases (M)': [807-1221, 604-795, 576-740],
            'Size': ['20-35 cm', '3-5 cm', '0.7-1.3 cm']
        })

        for _, row in parasite_data.iterrows():
            with st.expander(f"**{row['Parasite'].split()[0]}**"):
                st.write(f"**Scientific Name:** {row['Parasite']}")
                st.write(f"**Size:** {row['Size']}")
                st.write(f"**Global Cases:** {row['Global Cases (M)']} million")

    st.markdown("---")

    # Learning path
    st.subheader("🎓 Learning Path")
    learning_modules = [
        {"name": "Epidemiology & Burden", "icon": "📊", "status": "📖 15 min"},
        {"name": "Etiology & Life Cycles", "icon": "🦠", "status": "📖 20 min"},
        {"name": "Clinical Manifestations", "icon": "🏥", "status": "📖 18 min"},
        {"name": "Diagnosis Methods", "icon": "🔬", "status": "📖 12 min"},
        {"name": "Treatment & Management", "icon": "💊", "status": "📖 15 min"},
        {"name": "Prevention & Control", "icon": "🛡️", "status": "📖 25 min"},  # Special emphasis
        {"name": "Indian Context", "icon": "🇮🇳", "status": "📖 10 min"},
        {"name": "Assessment Quiz", "icon": "📝", "status": "🧠 15 min"}
    ]

    cols = st.columns(4)
    for i, module in enumerate(learning_modules):
        with cols[i % 4]:
            if st.button(f"{module['icon']} {module['name']}\n{module['status']}",
                        key=f"module_{i}"):
                st.rerun()
                # Navigation would happen here

    st.markdown("---")

    # Recent activity placeholder
    st.subheader("📈 Recent Activity")
    st.info("Complete modules in order to track your learning progress!")

def render_epidemiology(sth_data):
    """Render epidemiology section with interactive visualizations"""
    st.title("📊 Epidemiology & Global Burden")

    # Interactive filters
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_states = st.multiselect(
            "Select States",
            options=sorted(sth_data['State'].unique()),
            default=sorted(sth_data['State'].unique())[:5],
            help="Choose states to visualize"
        )

    with col2:
        selected_parasites = st.multiselect(
            "Select Parasites",
            options=['Prevalence_Ascaris', 'Prevalence_Trichuris', 'Prevalence_Hookworm'],
            default=['Prevalence_Ascaris'],
            format_func=lambda x: x.replace('Prevalence_', '').replace('_', ' '),
            help="Choose parasites to display"
        )

    with col3:
        chart_type = st.selectbox(
            "Chart Type",
            options=["Bar Chart", "Heatmap", "Scatter Plot", "Box Plot"],
            help="Select visualization type"
        )

    filtered_data = sth_data[sth_data['State'].isin(selected_states)]

    st.markdown("---")

    if chart_type == "Bar Chart":
        # Comparative bar chart
        fig = go.Figure()

        for parasite in selected_parasites:
            state_means = filtered_data.groupby('State')[parasite].mean().sort_values(ascending=False)

            fig.add_trace(go.Bar(
                name=parasite.replace('Prevalence_', '').replace('_', ' '),
                x=state_means.index,
                y=state_means.values,
                marker_color=INDIAN_COLORS[len(fig.data)]
            ))

        fig.update_layout(
            title="State-wise Parasite Prevalence Comparison",
            xaxis_title="States",
            yaxis_title="Prevalence (%)",
            barmode='group',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Heatmap":
        # Correlation heatmap
        pivot_data = filtered_data.groupby('State')[selected_parasites].mean()

        fig = px.imshow(
            pivot_data.T,
            color_continuous_scale='YlOrRd',
            title="Parasite Prevalence Heatmap by State"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Key epidemiological facts
    st.markdown("---")
    st.subheader("📋 Key Epidemiological Facts")

    facts_col1, facts_col2 = st.columns(2)

    with facts_col1:
        st.markdown("""
        **🌍 Global Burden:**
        - 1.5 billion people infected (24% world population)
        - Children: Highest intensity and burden
        - Rural areas: 2-3x higher prevalence than urban

        **💰 Economic Impact:**
        - $7-12 billion annual global cost
        - Lost productivity and healthcare expenses
        - Prevention cost-effective: $0.02-0.50/treatment
        """)

    with facts_col2:
        st.markdown("""
        **🇮🇳 India Specific:**
        - 225 million cases (highest global burden)
        - Rural prevalence: 40-60%
        - School-aged children: 18-25% infected

        **🎯 Risk Factors:**
        - Open defecation (OR: 2.3)
        - Poverty and poor sanitation
        - Geophagia in children
        - Tropical climate conditions
        """)

def render_etiology():
    """Render parasite information and life cycles"""
    st.title("🦠 Etiology & Life Cycles")

    st.markdown("""
    Soil Transmitted Helminthiases (STH) are caused by three main nematode parasites:
    intestinal roundworms, whipworms, and hookworms.
    """)

    # Interactive parasite selector
    parasite = st.selectbox(
        "Select Parasite for Detailed Information",
        ["Ascaris lumbricoides", "Trichuris trichiura", "Hookworms (Necator americanus & Ancylostoma duodenale)"]
    )

    if parasite == "Ascaris lumbricoides":
        st.subheader("🪱 Ascaris lumbricoides (Roundworm)")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **📐 Biology:**
            - Size: 20-35 cm (females), 15-30 cm (males)
            - Lifespan: 12-18 months
            - Egg size: 45-75 μm × 35-50 μm
            - Egg appearance: Oval, golden-brown, mamillated shell

            **🔄 Transmission:** Fecal-oral route
            - Eggs ingested via contaminated food/water
            - Eggs embryonate in soil (3-4 weeks)
            - Infective stage: Embryonated eggs
            """)

        with col2:
            st.markdown("""
            **🌀 Life Cycle Stages:**

            1. **Ingestion:** Embryonated eggs in contaminated food
            2. **Hatching:** Larvae released in small intestine
            3. **Migration:** Through blood to liver → lungs → trachea
            4. **Swallowing:** Reach small intestine again
            5. **Maturation:** Develop into adult worms (6-8 weeks)

            **🌡️ Environmental Requirements:**
            - Temperature: 22-33°C (optimal 28°C)
            - Moisture: >20% soil humidity
            - pH: 5.5-7.0
            """)

    elif parasite == "Trichuris trichiura":
        st.subheader("🪱 Trichuris trichiura (Whipworm)")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **📐 Biology:**
            - Size: Females 3-5 cm, males 3-4 cm
            - Lifespan: 1-3 years
            - Appearance: Whip-like shape (thicker posterior)
            - Egg size: 50-55 μm × 22-24 μm
            - Egg appearance: Barrel-shaped with bipolar plugs

            **🔄 Transmission:** Fecal-oral route
            - Eggs excreted in feces
            - Develop in soil (3-6 weeks)
            - Infective stage: Embryonated eggs
            """)

        with col2:
            st.markdown("""
            **🌀 Life Cycle Stages:**

            1. **Ingestion:** Embryonated eggs in contaminated food
            2. **Hatching:** Larvae released in small intestine
            3. **Penetration:** Local tissue invasion (no migration)
            4. **Maturation:** Adults in cecum/colon
            5. **Egg Production:** Females produce 5,000-10,000 eggs/day

            **🌡️ Environmental Requirements:**
            - Temperature: 25-30°C optimal
            - Moisture: High humidity required
            - Survival: Resistant to environmental stress
            """)

    elif "Hookworms" in parasite:
        st.subheader("🪝 Hookworms (Necator americanus & Ancylostoma duodenale)")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **📐 Biology:**
            - Size: Females 0.7-1.3 cm, males smaller
            - Lifespan: Necator (1-5 years), Ancylostoma (1 year)
            - Appearance: C-shaped, cutting plates (Necator) or teeth (Ancylostoma)
            - Egg size: 65-75 μm × 35-40 μm
            - Egg appearance: Oval, thin-shelled, 4-8 celled larva

            **🔄 Transmission:** Percutaneous
            - Larvae penetrate skin (feet/hands)
            - Migrate through bloodstream
            - Infective stage: Filariform larvae
            """)

        with col2:
            st.markdown("""
            **🌀 Life Cycle Stages:**

            1. **Egg Excretion:** In feces to soil
            2. **Development:** Eggs → rhabditiform → filariform larvae (5-8 days)
            3. **Skin Penetration:** Filariform larvae through skin
            4. **Migration:** Bloodstream → lungs → swallowed
            5. **Maturation:** Adults attach to small intestine mucosa
            6. **Blood Feeding:** Daily blood loss 0.1-0.3 ml per worm

            **🌡️ Environmental Requirements:**
            - Temperature: 24-30°C optimal
            - Soil type: Sandy, well-drained
            - Moisture: Essential for larval development
            """)

    # Comparative table
    st.markdown("---")
    st.subheader("📊 Comparative Analysis")

    comparison_data = pd.DataFrame({
        'Aspect': ['Average Length', 'Lifespan', 'Egg Shape', 'Transmission', 'Development Time', 'Infective Stage'],
        'Ascaris lumbricoides': ['20-35 cm (♀)', '12-18 months', 'Oval, mamillated', 'Fecal-oral', '3-4 weeks', 'Embryonated egg'],
        'Trichuris trichiura': ['3-5 cm (♀)', '1-3 years', 'Barrel, bipolar plugs', 'Fecal-oral', '3-6 weeks', 'Embryonated egg'],
        'Hookworms': ['0.7-1.3 cm (♀)', '1-5 years', 'Oval, thin shell', 'Percutaneous', '5-8 days', 'Filariform larva']
    })

    st.dataframe(comparison_data.set_index('Aspect'), use_container_width=True)

def render_clinical():
    """Render clinical manifestations section"""
    st.title("🏥 Clinical Manifestations")

    # Symptom categories
    symptom_categories = st.tabs(["Asymptomatic Infection", "Pulmonary Phase", "Intestinal Phase", "Complications"])

    with symptom_categories[0]:
        st.subheader("🤫 Asymptomatic Infection")
        st.markdown("""
        **Incidence:** 60-80% of infected individuals show no symptoms

        **Hidden Impact:**
        - Subclinical morbidity in apparently healthy individuals
        - Growth retardation and nutritional deficiencies
        - Impaired cognitive development in children
        - Reservoir for ongoing transmission

        **Public Health Significance:**
        - Silent carrier state maintains community transmission
        - Economic impact through reduced productivity
        - Long-term developmental consequences
        """)

    with symptom_categories[1]:
        st.subheader("🫁 Pulmonary Phase (Loeffler's Syndrome)")
        st.markdown("""
        **Timing:** 2-4 weeks post-infection (Ascaris migration)

        **Symptoms:**
        - Dry cough and wheezing
        - Chest pain and shortness of breath
        - Low-grade fever (37.5-38.5°C)
        - Blood eosinophilia (20-50%)

        **Radiological Findings:**
        - Transient pulmonary infiltrates
        - Ground-glass opacities
        - Usually resolves within 10-14 days

        **Cause:** Larval migration through lung capillaries
        """)

    with symptom_categories[2]:
        st.subheader("🫄 Intestinal Phase")
        st.markdown("""
        **Ascaris lumbricoides:**
        - Abdominal pain and discomfort
        - Nausea, vomiting, irregular bowel movements
        - Malnutrition and growth retardation
        - Subclinical protein-energy malnutrition

        **Trichuris trichiura (Heavy infection):**
        - Chronic diarrhea with mucus and blood
        - Rectal prolapse (especially in children <5 years)
        - Iron-deficiency anemia
        - Failure to thrive

        **Hookworm Disease:**
        - Ground itch (pruritic dermatitis at penetration sites)
        - Iron deficiency anemia (classic triad: anemia + edema + hypoproteinemia)
        - General malaise and fatigue
        - Increased susceptibility to other infections
        """)

    with symptom_categories[3]:
        st.subheader("⚠️ Complications")
        st.markdown("""
        **High Worm Burden:**
        - Intestinal obstruction (Ascaris volvulus)
        - Severe anemia (<8 g/dL hemoglobin)
        - Rectal prolapse with secondary infection

        **Rare but Serious:**
        - Biliary ascariasis (worms in bile ducts)
        - Pancreatic ascariasis
        - Perforation and peritonitis
        - Toxic megacolon (Trichuris)

        **Pregnancy Complications:**
        - Severe anemia in pregnant women
        - Low birth weight infants
        - Increased maternal morbidity

        **Secondary Infections:**
        - Bacterial superinfection of damaged mucosa
        - Viral gastroenteritis complications
        - Helminth co-infections
        """)

def render_diagnosis():
    """Render diagnosis section with laboratory methods"""
    st.title("🔬 Diagnosis Methods")

    # Interactive diagnostic workflow
    st.subheader("🔍 Diagnostic Approach")

    diagnosis_steps = st.expander("📋 Step-by-Step Diagnostic Process", expanded=True)
    with diagnosis_steps:
        st.markdown("""
        1. **Clinical History:**
           - Geographic location (endemic areas)
           - Travel to tropical/subtropical regions
           - Occupational exposure (farmers, miners)
           - Behavioral factors (geophagia, poor hygiene)

        2. **Physical Examination:**
           - Nutritional status assessment
           - Pallor (anemia)
           - Abdominal tenderness
           - Digital rectal examination for Trichuris

        3. **Laboratory Diagnosis:**
           - Stool examination (primary method)
           - Blood tests (eosinophilia)
           - Imaging (obstruction, biliary parasites)
        """)

    # Diagnostic methods
    methods = st.tabs(["Stool Examination", "Concentration Techniques", "Advanced Methods"])

    with methods[0]:
        st.subheader("🎯 Direct Stool Examination")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **Direct Smear Method:**
            - Fresh stool sample (pea-sized)
            - Mix with saline on glass slide
            - Cover with coverslip
            - Examine under microscope (10x, 40x)

            **Limitations:**
            - Low sensitivity (detects heavy infections only)
            - Requires experienced microscopist
            - Time-consuming for population surveys
            """)

        with col2:
            st.markdown("""
            **Kato-Katz Technique (WHO Gold Standard):**
            - Quantitative method for field surveys
            - Template (41.7 mg stool) for volume standardization
            - Glycerol-malachite green preserves eggs
            - Increases sensitivity by 2-3 fold

            **Egg Count Categories:**
            - Light: 1-999 EPG (eggs per gram)
            - Moderate: 1,000-9,999 EPG
            - Heavy: ≥10,000 EPG
            """)

    with methods[1]:
        st.subheader("🔬 Concentration Techniques")
        st.markdown("""
        **Formol-Ether Concentration:**
        - Enhances detection sensitivity
        - Suitable for low-intensity infections
        - Requires laboratory equipment

        **Harada-Mori Method:**
        - Filtration technique
        - Good for Trichuris detection
        - Quantitative assessment possible

        **Zinc Sulfate Flotation:**
        - Density gradient method
        - Superior for hookworm eggs
        - Quick and reliable technique

        **Multiple Samples Recommended:**
        - Examine 3 consecutive stool samples
        - Increases sensitivity to >90%
        - Required for epidemiological surveys
        """)

    with methods[2]:
        st.subheader("🧬 Advanced Diagnostic Methods")
        st.markdown("""
        **Molecular Diagnostics:**
        - PCR for species identification
        - Real-time PCR for quantitative assays
        - LAMP (Loop-mediated isothermal amplification) for field use

        **Serological Tests:**
        - Antibody detection (limited clinical use)
        - Not recommended for routine diagnosis
        - Useful for epidemiological studies

        **Imaging Techniques:**
        - X-ray for pulmonary migration
        - Ultrasound for biliary ascariasis
        - CT/MRI for complications

        **Emerging Technologies:**
        - Smartphone microscopy
        - Artificial intelligence for egg identification
        - Portable molecular diagnostics
        """)

def render_treatment():
    """Render treatment and management section"""
    st.title("💊 Treatment & Management")

    # Principal drugs
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🛡️ First-Line Anthelmintics")
        drugs_data = pd.DataFrame({
            'Drug': ['Albendazole', 'Mebendazole', 'Pyrantel Pamoate'],
            'Adult Dose': ['400 mg single', '500 mg single', '10 mg/kg single'],
            'Pregnancy Safety': ['Category C', 'Category C', 'Category A'],
            'Efficacy': ['95-100%', '90-95%', '85-90%']
        })
        st.dataframe(drugs_data, use_container_width=True)

    with col2:
        st.subheader("📊 Comparative Efficacy")
        efficacy_data = pd.DataFrame({
            'Drug': ['Albendazole', 'Mebendazole', 'Pyrantel'],
            'Ascaris': [95, 90, 85],
            'Trichuris': [30, 90, 40],
            'Hookworm': [70, 95, 90]
        })

        fig = px.bar(efficacy_data.melt(id_vars='Drug', var_name='Parasite', value_name='Efficacy'),
                    x='Drug', y='Efficacy', color='Parasite',
                    title='Anthelmintic Efficacy by Parasite',
                    text_auto='.0f')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Special considerations
    considerations = st.tabs(["Pregnancy", "Children", "Severe Cases", "Drug Resistance"])

    with considerations[0]:
        st.subheader("🤰 Treatment in Pregnancy")
        st.markdown("""
        **First Trimester:**
        - Avoid routine treatment
        - Treat only if symptomatic and benefits outweigh risks
        - Mebendazole and albendazole: Category C (teratogenic potential)

        **Second/Third Trimester:**
        - Albendazole can be used after first trimester
        - Pyrantel pamoate: Safest option (Category A)
        - Iron supplementation essential alongside anthelmintic treatment

        **WHO Recommendations:**
        - Individualized risk-benefit assessment
        - Focus on iron supplementation for anemia
        - Delay elective treatment until after delivery when possible
        """)

    with considerations[1]:
        st.subheader("👶 Pediatric Treatment")
        st.markdown("""
        **Children <2 Years:**
        - Individual assessment required
        - WHO recommends treatment in high-prevalence areas
        - Age-appropriate dosing critical
        - Close monitoring for adverse reactions

        **School-Age Children:**
        - Target population for MDA programs
        - Regular deworming alongside other interventions
        - Educational component essential
        - Monitor growth and development

        **Adolescent
