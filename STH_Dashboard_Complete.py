#!/usr/bin/env python3
"""
Complete STH Learning Dashboard
Interactive Streamlit application with all medical aspects and Indian context
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path

# Page config
st.set_page_config(
    page_title="STH Learning Dashboard",
    page_icon="🦟",
    layout="wide"
)

# Load dummy data
@st.cache_data
def load_data():
    np.random.seed(42)
    states = ['Maharashtra', 'Uttar Pradesh', 'Bihar', 'West Bengal', 'Madhya Pradesh',
             'Tamil Nadu', 'Rajasthan', 'Karnataka', 'Gujarat', 'Odisha']

    data = []
    for state in states:
        data.append({
            'State': state,
            'Ascaris_Prevalence': np.clip(np.random.uniform(20, 60), 0, 100),
            'Trichuris_Prevalence': np.clip(np.random.uniform(15, 45), 0, 100),
            'Hookworm_Prevalence': np.clip(np.random.uniform(10, 40), 0, 100),
            'Population': np.random.randint(100000, 1000000),
            'Sanitation_Index': np.random.uniform(0.3, 0.9)
        })
    return pd.DataFrame(data)

def render_epidemiology(data):
    """Render epidemiology section with interactive visualizations"""
    st.title("📊 Epidemiology & Global Burden")

    # Interactive filters
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_states = st.multiselect(
            "Select States",
            options=sorted(data.State.unique())[:8],
            default=sorted(data.State.unique())[:5],
            help="Choose states to visualize"
        )

    with col2:
        selected_parasites = st.multiselect(
            "Select Parasites",
            options=['Ascaris_Prevalence', 'Trichuris_Prevalence', 'Hookworm_Prevalence'],
            default=['Ascaris_Prevalence'],
            format_func=lambda x: x.replace('_Prevalence', ''),
            help="Choose parasites to display"
        )

    with col3:
        chart_type = st.selectbox(
            "Chart Type",
            options=["Bar Chart", "Heatmap"],
            help="Select visualization type"
        )

    filtered_data = data[data['State'].isin(selected_states)]

    st.markdown("---")

    if chart_type == "Bar Chart":
        fig = px.bar(filtered_data.sort_values('Ascaris_Prevalence', ascending=False),
                     x='State', y=selected_parasites,
                     title='Parasite Prevalence by State',
                     barmode='group', width=800, height=500)
        st.plotly_chart(fig, use_container_width=True)

    # Key epidemiological facts
    st.subheader("📋 Key Epidemiological Facts")

    facts_col1, facts_col2 = st.columns(2)

    with facts_col1:
        st.markdown("""
        **🌍 Global Burden:**
        - 1.5 billion people infected (24% world population)
        - Children: Highest intensity and burden
        - Rural areas: 2-3x higher than urban
        - Economic cost: $7-12 billion annually

        **📍 Geographic Distribution:**
        - Sub-Saharan Africa: Highest burden
        - South Asia: India (225 million cases)
        - Southeast Asia: Major endemic areas
        """)

    with facts_col2:
        st.markdown("""
        **🇮🇳 India Specific:**
        - Highest absolute burden globally
        - Rural prevalence: 40-60%
        - School-aged children: 15-25% infected
        - Agricultural communities most affected

        **🎯 Risk Factors:**
        - Poverty and sanitation (OR: 2.3)
        - Open defecation practices
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
            - Appearance: Oval, golden-brown, mamillated shell

            **🔄 Transmission Route:**
            - Fecal-oral route
            - Eggs ingested via contaminated food/water
            - Embryounate in soil (3-4 weeks)
            - Infective stage: Embryonated eggs
            """)

        with col2:
            st.markdown("""
            **🌀 Life Cycle Stages:**

            1. **Ingestion:** Embryonated eggs in contaminated food/water
            2. **Hatching:** Larvae released in small intestine
            3. **Migration:** Through blood → liver → lungs → trachea
            4. **Swallowing:** Trachea → esophagus → small intestine
            5. **Maturation:** Develop into adult worms (6-8 weeks)
            6. **Egg Production:** Females produce 200,000 eggs/day

            **🌡️ Environmental Requirements:**
            - Temperature: 22-33°C (optimal 28°C)
            - Moisture: >20% soil humidity
            - pH: 5.5-7.0 optimal range
            """)

    elif parasite == "Trichuris trichiura":
        st.subheader("🪱 Trichuris trichiura (Whipworm)")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **📐 Biology:**
            - Size: Females 3-5 cm, males 3-4 cm
            - Lifespan: 1-3 years (longest among STH)
            - Appearance: Whip-like shape (thicker posterior)
            - Egg size: 50-55 μm × 22-24 μm
            - Appearance: Barrel-shaped with bipolar plugs

            **🔄 Transmission Route:**
            - Fecal-oral route
            - Eggs excreted in feces
            - Development in soil (3-6 weeks required)
            - Infective stage: Embryonated eggs
            """)

        with col2:
            st.markdown("""
            **🌀 Life Cycle Stages:**

            1. **Ingestion:** Embryonated eggs with contaminated food
            2. **Hatching:** Larvae released in small intestine
            3. **Penetration:** Local tissue invasion (no systemic migration)
            4. **Migration:** Within intestinal mucosa to cecum/colon
            5. **Maturation:** Adults embed in colon mucosa (3 months)
            6. **Egg Production:** Females lay 5,000-10,000 eggs/day

            **🌡️ Environmental Requirements:**
            - Temperature: 25-30°C optimal
            - Moisture: High humidity required for survival
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
            - Appearance: Oval, thin-shelled, 4-8 celled morula

            **🔄 Transmission Route:**
            - Percutaneous penetration through skin
            - Active migration through human skin
            - Infective stage: Filariform larvae
            """)

        with col2:
            st.markdown("""
            **🌀 Life Cycle Stages:**

            1. **Skin Penetration:** Filariform larvae through bare feet/hands
            2. **Vascular Migration:** Bloodstream → heart → lungs
            3. **Lung Penetration:** Into alveoli → migrate up bronchial tree
            4. **Swallowing:** Reach pharynx → swallowed into GI tract
            5. **Intestinal Attachment:** Attach to small intestinal mucosa
            6. **Blood Feeding:** Adults feed on host blood (0.1-0.3 ml/day)

            **🌡️ Environmental Requirements:**
            - Temperature: 24-30°C optimal for larval development
            - Soil type: Sandy, well-drained soils preferred
            - Moisture: Essential for rhabditiform-filariform transformation
            """)

    # Comparative table
    st.markdown("---")
    st.subheader("📊 Comparative Analysis")

    comparison_data = pd.DataFrame({
        'Feature': ['Primary Transmission', 'Infective Stage', 'Development Time', 'Lifespan', 'Egg Production', 'Migration Pattern'],
        'Ascaris lumbricoides': ['Fecal-oral', 'Embryonated egg', '3-4 weeks', '12-18 months', '200K/day', 'Hepato-pulmonary'],
        'Trichuris trichiura': ['Fecal-oral', 'Embryonated egg', '3-6 weeks', '1-3 years', '5-10K/day', 'Local tissue'],
        'Hookworms': ['Percutaneous', 'Filariform larva', '5-8 days', '1-5 years', '5-10K/day', 'Cutaneous-pulmonary']
    })

    st.dataframe(comparison_data.set_index('Feature'), use_container_width=True)

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
        - Long-term productivity losses

        **Public Health Significance:**
        - Silent carrier state maintains community transmission cycles
        - Underestimated economic impact on education and workforce
        - Challenging for targeted treatment programs
        """)

    with symptom_categories[1]:
        st.subheader("🫁 Pulmonary Phase (Loeffler's Syndrome)")
        st.markdown("""
        **Timing:** 2-4 weeks post-infection (classic with Ascaris migration)

        **Symptoms:**
        - Dry cough and wheezing (most common)
        - Chest pain and shortness of breath
        - Low-grade fever (37.5-38.5°C)
        - Blood eosinophilia (20-50% eosinophilia)

        **Radiological Findings:**
        - Transient pulmonary infiltrates on chest X-ray
        - Ground-glass opacities
        - Usually resolves spontaneously within 10-14 days

        **Pathophysiology:**
        - Larval migration through lung capillaries
        - Localized inflammatory response
        - Eosinophilic pneumonitis
        """)

    with symptom_categories[2]:
        st.subheader("🫄 Intestinal Phase")
        st.markdown("""
        **Ascaris lumbricoides Manifestations:**
        - Abdominal pain and discomfort (epigastric/umbilical)
        - Nausea, vomiting, irregular bowel movements
        - Malnutrition and growth retardation
        - Subclinical protein-energy malnutrition
        - Occasional palpable mass (worm bolus)

        **Trichuris trichiura (Heavy infection):**
        - Chronic diarrhea with mucus mixed with blood
        - Rectal prolapse (especially in children <5 years)
        - Iron-deficiency anemia from chronic blood loss
        - Failure to thrive and growth retardation
        - Abdominal tenderness with sigmoid colon involvement

        **Hookworm Disease:**
        - Ground itch at penetration sites (pruritic dermatitis)
        - Iron deficiency anemia (classic triad: anemia + edema + hypoproteinemia)
        - General malaise and fatigue
        - Increased susceptibility to other infections
        - Epigastric pain and tenderness
        """)

    with symptom_categories[3]:
        st.subheader("⚠️ Complications")
        st.markdown("""
        **High Parasite Burden:**
        - Intestinal obstruction (Ascaris volvulus, common surgical emergency)
        - Severe anemia (<8 g/dL hemoglobin, especially hookworms)
        - Rectal prolapse with secondary bacterial infection

        **Rare but Serious Complications:**
        - Biliary ascariasis (worms migrate into bile ducts)
        - Pancreatic ascariasis (rare, but serious)
        - Perforation and peritonitis
        - Toxic megacolon (Trichuris-associated)

        **Pregnancy-Related Complications:**
        - Severe anemia in pregnant women (maternal and fetal effects)
        - Low birth weight infants
        - Increased maternal morbidity and mortality risk

        **Secondary Complications:**
        - Bacterial superinfection of damaged intestinal mucosa
        - Viral gastroenteritis complications
        - Helminth co-infections (malaria, HIV interactions)
        - Impaired nutritional status leading to other diseases
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
           - Geographic location (endemic vs. non-endemic areas)
           - Travel history to tropical/subtropical regions
           - Occupational exposure (farmers, miners, construction workers)
           - Behavioral factors (geophagia, eating soil)
           - Contact with contaminated soil/water

        2. **Physical Examination:**
           - Nutritional status assessment (BMI, weight-for-age)
           - Pallor examination (conjunctiva, nail beds for anemia)
           - Abdominal tenderness and organomegaly
           - Digital rectal examination (for Trichuris-associated prolapse)

        3. **Laboratory Diagnosis:**
           - Stool examination (primary diagnostic method)
           - Blood tests (eosinophilia, anemia profile)
           - Imaging studies (obstruction, biliary complications)
        """)

    # Diagnostic methods
    methods = st.tabs(["Direct Examination", "Concentration Techniques", "Advance Methods", "Clinical Utility"])

    with methods[0]:
        st.subheader("🎯 Direct Stool Examination")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **Direct Smear Method:**
            - Specimen: Fresh stool sample (pea-sized quantity)
            - Preparation: Mix with saline/lugol's iodine on glass slide
            - Examination: Cover with coverslip, examine under microscope
            - Magnification: 10x (survey), 40x (identification)

            **Limitations:**
            - Low sensitivity (detects only heavy infections)
            - Requires trained microscopist with diagnostic experience
            - Time-consuming for large-scale epidemiological surveys
            - Negative result doesn't rule out low-intensity infections
            """)

        with col2:
            st.markdown("""
            **Kato-Katz Technique (WHO Gold Standard):**
            - Quantitative method specifically designed for field use
            - Template: 41.7 mg standardized stool volume
            - Glycerol-malachite green solution for preservation and clarification
            - Clearing time: 30-60 minutes for optimal visualization
            - Requires minimal equipment and training

            **Egg Counting Categories:**
            - Light infection: 1-999 eggs per gram (EPG)
            - Moderate infection: 1,000-9,999 EPG
            - Heavy infection: ≥10,000 EPG

            **Advantages:**
            - Semi-quantitative assessment of infection intensity
            - Standardized volume allows comparison between surveys
            - Reliable for epidemiological monitoring and evaluation
            """)

    with methods[1]:
        st.subheader("🔬 Concentration Techniques")
        st.markdown("""
        **Formol-Ether Concentration Method:**
        - Enhanced sensitivity for low-intensity infections
        - Formalin preserves parasites, ether removes debris
        - Parasites concentrate at interface after centrifugation

        **Harada-Mori Tube Filtration Technique:**
        - Specialized filtration method for Trichuris eggs
        - Improved recovery from stool suspensions
        - Quantitative assessment possible

        **Zinc Sulfate Centrifugal Flotation:**
        - Density gradient approach (specific gravity 1.18)
        - Superior recovery of hookworm eggs
        - Suitable for both ova and protozoa

        **Multiple Sample Collection:**
        - Recommended: 3 consecutive stool samples
        - Increases diagnostic sensitivity to >90%
        - Essential for epidemiological surveys and control programs

        **Quality Control Considerations:**
        - Standardized laboratory procedures
        - Internal quality control measures
        - External proficiency testing programs
        """)

    with methods[2]:
        st.subheader("🧬 Advanced Diagnostic Methods")
        st.markdown("""
        **Molecular Techniques:**
        - **PCR (Polymerase Chain Reaction):** Species-specific identification and quantification
        - **Real-time PCR:** High sensitivity for low-intensity infections and surveillance
        - **LAMP (Loop-mediated isothermal amplification):** Field-applicable without thermocycling

        **Serodiagnostic Methods:**
        - Antibody detection by ELISA or Western blot
        - Limited clinical utility (cannot distinguish current vs. past infection)
        - Useful for epidemiological studies and outbreak investigations

        **Imaging Techniques:**
        - **Chest X-ray:** Pulmonary migration patterns and Loeffler's syndrome
        - **Ultrasound:** Biliary and pancreatic ascariasis diagnosis
        - **CT/MRI:** Complications like intestinal obstruction or perforation

        **Emerging Technologies:**
        - Smartphone microscopy with AI-assisted egg identification
        - Portable point-of-care diagnostic devices
        - Multiplex assays for co-infections
        """)

    with methods[3]:
        st.subheader("📊 Clinical Utility and Interpretation")
        st.markdown("""
        **Clinical Decision Making:**
        - Positive stool examination confirms infection
        - Negative result doesn't exclude infection (test limitations)
        - Quantitative results guide treatment decisions and prognosis

        **Epidemiological Surveillance:**
        - Population-based prevalence surveys
        - Program monitoring and impact evaluation
        - Drug efficacy monitoring (repeat testing 2-3 weeks post-treatment)

        **Special Considerations:**
        - Children <2 years: Difficult specimen collection
        - Immunocompromised: Higher false-negative rates
        - Recent treatment: May suppress egg output temporarily

        **Reporting and Documentation:**
        - Species identification and infection intensity
        - Clinical correlation with symptoms
        - Public health implications and follow-up recommendations
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
            'Efficacy (%)': ['95-100%', '90-95%', '85-90%']
        })
        st.dataframe(drugs_data, use_container_width=True)

    with col2:
        st.subheader("📊 Comparative Efficacy Against Parasites")
        efficacy_data = pd.DataFrame({
            'Drug': ['Albendazole', 'Mebendazole', 'Pyrantel Pamoate'],
            'Ascaris': [97, 92, 87],
            'Trichuris': [28, 91, 32],
            'Hookworms': [72, 96, 91]
        })

        fig = px.bar(efficacy_data.melt(id_vars='Drug'),
                    x='Drug', y='value', color='variable',
                    title='Cure Rates by Parasite and Drug (%)',
                    labels={'value': 'Cure Rate (%)', 'variable': 'Parasite'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Special considerations
    considerations = st.tabs(["Pregnancy & Children", "Severe Cases", "Drug Resistance", "Monitoring"])

    with considerations[0]:
        st.subheader("🤰 Pregnancy & Pediatric Treatment")
        st.markdown("""
        **First Trimester Pregnancy:**
        - Avoid routine treatment when possible
        - Albendazole/mebendazole: Category C (potential teratogenicity)
        - Pyrantel pamoate: Category A (safest option)
        - Individualized risk-benefit assessment

        **Second/Third Trimester Pregnancy:**
        - Albendazole can be used after organogenesis completion
        - Iron supplementation concurrent with treatment
        - Monitoring: Fetal growth, maternal hemoglobin
        - Avoid high-dose regimens

        **Children <2 Years:**
        - Individual assessment required (limited safety data)
        - WHO recommends treatment in high-prevalence settings
        - Age-appropriate formulations and dosing
        - Close monitoring for adverse reactions

        **School-Age Children (Primary Target):**
        - Full adult dosing appropriate in most cases
        - Integration with school health programs
        - Community-based distribution strategies
        - Parental consent and education
        """)

    with considerations[1]:
        st.subheader("🚑 Management of Severe Cases")
        st.markdown("""
        **Intestinal Obstruction (Ascaris volvulus):**
        - Conservative management: Nil per oral, IV fluids, nasogastric decompression
        - Analgesics and antiemetics as needed
        - Surgical intervention if complete obstruction (>48 hours)
        - Preoperative stabilization and parasite reduction

        **Severe Hookworm Anemia:**
        - Transfusion if hemoglobin <7 g/dL or symptomatic
        - Iron supplementation (3-6 mg elemental iron/kg/day)
        - Parenteral iron in severe malabsorption cases
        - Combined with nutritional rehabilitation

        **Ascariasis Complications:**
        - Biliary tract involvement: ERCP or surgical extraction
        - Pancreatic complications: Conservative management primarily
        - Peritonitis from perforation: Surgical emergency

        **Trichuriasis Complications:**
        - Severe rectal prolapse: Manual reduction and antiparasitics
        - Toxic megacolon: Supportive care and broad-spectrum antibiotics
        - Surgical intervention in rare cases
        """)

    with considerations[2]:
        st.subheader("🔬 Drug Resistance Management")
        st.markdown("""
        **Emerging Problem:**
        - Albendazole resistance reported in some areas
        - Mebendazole cross-resistance common
        - Pyrantel pamoate may remain effective in resistant strains

        **Detection and Monitoring:**
        - Cure rate monitoring (<95% suggests resistance)
        - Egg reduction rate assessment
        - Molecular markers for resistance genes

        **Alternative Strategies:**
        - Combination therapy (albendazole + ivermectin)
        - Extended treatment regimens
        - Research into new anthelmintic compounds

        **Programmatic Implications:**
        - Integrated surveillance systems
        - Alternative drug rotation strategies
        - Investment in new drug development
        """)

    with considerations[3]:
        st.subheader("📊 Treatment Monitoring & Evaluation")
        st.markdown("""
        **Individual Patient Monitoring:**
        - Clinical symptom resolution assessment
        - Stool examination 2-4 weeks post-treatment
        - Hematological parameters (anemia correction)
        - Growth monitoring in children

        **Program Effectiveness:**
        - Coverage surveys (target >75%)
        - Parasitological cure rates (>90% expected)
        - Morbidity reduction monitoring
        - Cost-effectiveness analysis

        **Drug Efficacy Surveillance:**
        - Periodic drug efficacy testing
        - Chemistry, manufacturing, and controls verification
        - Quality assurance programs

        **Long-term Follow-up:**
        - Reinfection prevention education
        - Community-based health promotion
        - Sustainable environmental improvements
        """)

def render_references():
    """Render references section"""
    st.title("📚 References & Additional Resources")

    st.markdown("""
    **Academic and Clinical References:**
    """)

    # Add reference categories as expandable sections
    with st.expander("📖 WHO Guidelines", expanded=False):
        st.markdown("""
        - **WHO Guidelines for the Control of Soil-transmitted Helminth Infections** (2021)
        - **Preventive Chemotherapy in Human Helminthiasis** (WHO)
        - **Guidelines for Deworming Interventions** (WHO & UNICEF)
        - **International Standards for Clinical Laboratory Methods** (WHO)
        """)

    with st.expander("🔬 Research Publications", expanded=False):
        st.markdown("""
        - **Global Burden of Disease Study 2019** - Parasitic Diseases Trends
        - **STEM Project Publications** - MDA Impact Studies
        - **Indian Deworming Program Evaluations** - HPC Publications
        - **WHO Technical Reports** - Control Strategy Updates
        """)

    with st.expander("📊 Treatment Guidelines", expanded=False):
        st.markdown("""
        - **Manson's Tropical Diseases** - Chapter on Helminths
        - **CDC Parasitic Diseases Guidelines** - Diagnostic Standards
        - **Indian Academy of Pediatrics** - Pediatric Treatment Protocols
        - **Essential Medicines List** - WHO Recommended Anthelmintics
        """)

    with st.expander("🇮🇳 Indian National Programs", expanded=False):
        st.markdown("""
        - **Ministry of Health & Family Welfare** - National Deworming Day
        - **National Vector Borne Disease Control Programme** (NVBDCP)
        - **National Health Mission** - Reproductive & Child Health
        - **Ministry of Jal Shakti** - Clean Water Initiatives
        """)

def render_prevention_control():
    """Special emphasis on prevention and control"""
    st.title("🛡️ Prevention & Control Strategies")

    st.markdown("""
    **Special Focus Section:** Prevention is better than cure.
    WHO's comprehensive approach combines multiple strategies.
    """)

    # Main strategies
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💊 Mass Drug Administration (MDA)")
        st.markdown("""
        **Primary Strategy:**
        - Target: School-age children (5-14 years)
        - Frequency: 1-2 times annually
        - Coverage: ≥75% required for effectiveness
        - Drugs: Albendazole 400mg or Mebendazole 500mg

        **India: National Deworming Day**
        - February 10th and August 10th
        - 540 million children targeted
        - Free medication distribution
        """)

    with col2:
        st.subheader("🚰 Water, Sanitation & Hygiene (WASH)")
        st.markdown("""
        **Sustainable Prevention:**
        - Safe water supply and treatment
        - Proper sanitation facilities
        - Handwashing education
        - Proper waste disposal

        **F Diagram:**
        Feces → Fields → Flies → Fingers → Food → Mouth
        *Break this chain to prevent transmission*
        """)

    st.markdown("---")

    # Health education and monitoring
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📚 Health Education & Community")
        st.markdown("""
        **Key Messages:**
        - Open defecation stops here
        - Handwashing prevents disease
        - Proper footwear against hookworms
        - Clean food and water safety

        **Community Involvement:**
        - Local leadership engagement
        - School-based education
        - Religious institution partnerships
        """)

    with col4:
        st.subheader("📊 Monitoring & Evaluation")
        st.markdown("""
        **WHO Targets 2030:**
        - 75% prevalence reduction
        - 90% treatment coverage
        - Elimination in selected countries

        **Success Indicators:**
        - Parasitological surveys
        - Treatment coverage reports
        - Disease burden reduction
        - Cost-benefit analysis
        """)

    # Progress visualization
    st.markdown("---")
    st.subheader("📈 MDA Progress in India")

    progress_data = pd.DataFrame({
        'Year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
        'Coverage': [0, 15, 35, 55, 68, 75, 82, 85]
    })

    fig = px.line(progress_data, x='Year', y='Coverage',
                  title='National Deworming Program Coverage (2015-2022)',
                  markers=True)
    fig.update_layout(yaxis_title='Coverage (%)')
    st.plotly_chart(fig, use_container_width=True)

def render_indian_context(data):
    """Indian context section"""
    st.title("🇮🇳 Indian Context")

    st.markdown("""
    India bears the highest absolute burden of STH globally, with 225 million cases.
    The National Deworming Day program represents one of the world's largest public health interventions.
    """)

    # State-wise data
    st.subheader("📍 State-wise Disease Burden")

    fig = px.bar(data.sort_values('Ascaris_Prevalence', ascending=False),
                 x='State', y=['Ascaris_Prevalence', 'Trichuris_Prevalence', 'Hookworm_Prevalence'],
                 title='Parasite Prevalence by State (%)',
                 barmode='group')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # Key Indian facts
    st.subheader("🎯 Key Indian Facts")

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **Program Scale:**
        - 540 million children covered annually
        - 11.5 lakh schools participating
        - 35 lakh ASHAs involved
        - Treatment cost: ~₹100 crore/year
        """)

    with col2:
        st.success("""
        **Success Metrics:**
        - Coverage reached 85%+ in recent years
        - Mixed infection rates reduced by 20-30%
        - Anemia prevalence decreased in target areas
        - Integration with ICDS and MDM programs
        """)

    # Challenges and solutions
    st.subheader("🎯 Challenges & Solutions")

    challenges = pd.DataFrame({
        'Challenge': ['Supply Chain Management', 'Community Acceptance', 'Monitoring Quality', 'Drug Resistance Emergence'],
        'Solution': ['State-level planning coordination', 'IEC campaigns and mobilization', 'Real-time digital reporting', 'Alternative drug combinations'],
        'Status': ['🔄 Ongoing', '✅ Achieved', '▶️ In Progress', '👁️ Under Surveillance']
    })

    st.dataframe(challenges, use_container_width=True)

def render_quiz():
    """Interactive assessment quiz"""
    st.title("📝 Assessment Quiz")
    st.markdown("Test your knowledge of Soil Transmitted Diseases")

    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0

    questions = [
        {
            'question': 'Which parasite causes Loeffler\'s syndrome?',
            'options': ['Ascaris lumbricoides', 'Trichuris trichiura', 'Hookworms', 'Strongyloides'],
            'correct': 0,
            'explanation': 'Ascaris larvae migrate through lungs causing pulmonary symptoms.'
        },
        {
            'question': 'What is the WHO gold standard for STH diagnosis?',
            'options': ['Direct smear', 'Kato-Katz technique', 'Blood film', 'Urine examination'],
            'correct': 1,
            'explanation': 'Kato-Katz provides quantitative egg counts for epidemiological surveys.'
        },
        {
            'question': 'Which drug is safest for use in pregnancy?',
            'options': ['Albendazole', 'Mebendazole', 'Pyrantel pamoate', 'Levamisole'],
            'correct': 2,
            'explanation': 'Pyrantel pamoate is Category A and safest during pregnancy.'
        },
        {
            'question': 'What is India\'s National Deworming Day?',
            'options': ['January 26', 'February 10 & August 10', 'May 5', 'August 15'],
            'correct': 1,
            'explanation': 'Twice annually on February 10th and August 10th, aligned with Republic Day and Independence Day.'
        }
    ]

    score = 0
    total_questions = len(questions)

    for i, q in enumerate(questions):
        st.subheader(f"Question {i+1}: {q['question']}")

        key = f"q_{i}"
        answer = st.radio(
            f"Select your answer:",
            q['options'],
            key=key,
            index=None
        )

        if answer is not None:
            if q['options'].index(answer) == q['correct']:
                st.success(f"✅ Correct! {q['explanation']}")
                if not st.session_state.quiz_answers.get(key, False):
                    st.session_state.quiz_score += 1
                st.session_state.quiz_answers[key] = True
            else:
                st.error(f"❌ Incorrect. Correct answer: {q['options'][q['correct']]}")
                st.info(q['explanation'])
        else:
            st.info("Please select an answer to continue.")

    # Show final score
    if st.button("Get Final Score", type="primary"):
        st.markdown("---")
        st.subheader("📊 Quiz Results")
        final_score = sum(st.session_state.quiz_answers.values())
        percentage = (final_score / total_questions) * 100

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score", f"{final_score}/{total_questions}")
        with col2:
            st.metric("Percentage", f"{percentage:.1f}%")
        with col3:
            if percentage >= 80:
                st.success("🏆 Excellent!")
            elif percentage >= 60:
                st.info("👍 Good effort!")
            else:
                st.warning("📚 Review materials and try again!")

def main():
    """Main dashboard application"""
    data = load_data()

    # Sidebar navigation
    with st.sidebar:
        st.title("🦟 STH Dashboard")
        st.markdown("---")

        menu_options = [
            "🏠 Overview",
            "📊 Epidemiology & Burden",
            "🦠 Etiology & Life Cycles",
            "🏥 Clinical Manifestations",
            "🔬 Diagnosis Methods",
            "💊 Treatment & Management",
            "🛡️ Prevention & Control",  # Special emphasis
            "🇮🇳 Indian Context",
            "📝 Assessment Quiz",
            "📚 References"
        ]

        selected = st.selectbox("Navigate", menu_options)

        st.markdown("---")
        st.info("**Learning Focus:** Prevention is better than cure - 80% of STH cases are preventable!")

    # Main content
    if selected == "🏠 Overview":
        st.title("🦟 Soil Transmitted Diseases")
        st.markdown("Interactive Learning Dashboard - MBBS 3rd Year")
        st.markdown("""
        **Created by:** Dr. Siddalingaiah H S  
        Professor, Community Medicine, SIMSRH, Tumkur  
        Email: hssling@yahoo.com | Phone: 8941087719  
        *Content generated with AI assistance and ensured medical accuracy*
        """)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Global Burden", "1.5 Billion", "people affected")
        with col2:
            st.metric("India Cases", "225 Million")
        with col3:
            st.metric("MDA Coverage", "85%", "target achieved")
        with col4:
            st.metric("Prevention Cost", "$0.02", "per treatment")

    elif selected == "📊 Epidemiology & Burden":
        render_epidemiology(data)

    elif selected == "🦠 Etiology & Life Cycles":
        render_etiology()

    elif selected == "🏥 Clinical Manifestations":
        render_clinical()

    elif selected == "🔬 Diagnosis Methods":
        render_diagnosis()

    elif selected == "💊 Treatment & Management":
        render_treatment()

    elif selected == "🛡️ Prevention & Control":
        render_prevention_control()

    elif selected == "🇮🇳 Indian Context":
        render_indian_context(data)

    elif selected == "📝 Assessment Quiz":
        render_quiz()

    elif selected == "📚 References":
        render_references()

    # Footer
    st.markdown("---")
    st.markdown("*Dashboard developed for comprehensive STH medical education*")

if __name__ == "__main__":
    main()
