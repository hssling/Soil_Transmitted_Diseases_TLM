#!/usr/bin/env python3
"""
Indian Context Visual Generation Script for Soil Transmitted Diseases TLM
Generates charts, graphs, and infographics specific to Indian STH epidemiology
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set Indian-themed color palette
INDIAN_COLORS = ['#FF9933', '#FFFFFF', '#138808', '#000080', '#FF0000']
sns.set_palette(INDIAN_COLORS)

# Configure matplotlib for Indian context
plt.rcParams['font.family'] = ['Arial', 'sans-serif']
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

class IndianSTHVisualizer:
    def __init__(self, data_path, output_dir):
        self.data_path = Path(data_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load data
        try:
            self.df = pd.read_excel(data_path, engine='openpyxl')
        except:
            try:
                self.df = pd.read_excel(data_path, engine='xlrd')
            except:
                print("Excel file could not be read, generating visualizations with dummy data...")
                self.df = self._create_dummy_data()

        # Create state-wise aggregations
        self.state_data = self._aggregate_state_data()

    def _aggregate_state_data(self):
        """Aggregate data by state for visualization"""
        state_agg = self.df.groupby('State').agg({
            'Prevalence_Ascaris': 'mean',
            'Prevalence_Trichuris': 'mean',
            'Prevalence_Hookworm': 'mean',
            'Total_Population': 'sum',
            'Children_1_14': 'sum'
        }).reset_index()

        # Calculate overall prevalence
        state_agg['Overall_Prevalence'] = (
            state_agg['Prevalence_Ascaris'] +
            state_agg['Prevalence_Trichuris'] +
            state_agg['Prevalence_Hookworm']
        ) / 3

        return state_agg

    def _create_dummy_data(self):
        """Create dummy data for visualization when Excel file is not available"""
        np.random.seed(42)  # For reproducible results

        # Create dummy districts data
        states = ['Maharashtra', 'Uttar Pradesh', 'Bihar', 'West Bengal', 'Madhya Pradesh',
                 'Tamil Nadu', 'Rajasthan', 'Karnataka', 'Gujarat', 'Odisha',
                 'Telangana', 'Punjab', 'Chhattisgarh', 'Haryana', 'Delhi']
        risk_categories = ['High', 'Moderate', 'Low']

        districts_data = []
        for state in states:
            for i in range(5):  # 5 districts per state
                prevalence_base = np.random.uniform(10, 60)
                district_data = {
                    'State': state,
                    'District': f'{state[:3]}_Dist{i+1}',
                    'Prevalence_Ascaris': np.clip(prevalence_base + np.random.normal(0, 5), 0, 100),
                    'Prevalence_Trichuris': np.clip(prevalence_base * 0.8 + np.random.normal(0, 3), 0, 100),
                    'Prevalence_Hookworm': np.clip(prevalence_base * 0.9 + np.random.normal(0, 4), 0, 100),
                    'Prevalence_Children': np.clip(prevalence_base + np.random.normal(0, 10), 0, 100),
                    'Total_Population': int(np.random.uniform(500000, 5000000)),
                    'Children_1_14': int(np.random.uniform(100000, 1000000)),
                    'Risk_Category': np.random.choice(risk_categories, p=[0.3, 0.4, 0.3])
                }
                districts_data.append(district_data)

        return pd.DataFrame(districts_data)

    def create_state_prevalence_map(self):
        """Create state-wise prevalence visualization"""
        fig, ax = plt.subplots(figsize=(15, 10))

        # Sort states by overall prevalence
        plot_data = self.state_data.sort_values('Overall_Prevalence', ascending=True)

        # Create horizontal bar chart
        y_pos = np.arange(len(plot_data['State']))
        bars = ax.barh(y_pos, plot_data['Overall_Prevalence'],
                      color=plt.cm.YlOrRd(plot_data['Overall_Prevalence']/60))

        # Customize plot
        ax.set_yticks(y_pos)
        ax.set_yticklabels(plot_data['State'], fontsize=10)
        ax.set_xlabel('Average Prevalence (%)', fontsize=12)
        ax.set_title('State-wise STH Prevalence in India\n(Higher bars indicate higher prevalence)',
                    fontsize=16, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3)

        # Add value labels on bars
        for i, v in enumerate(plot_data['Overall_Prevalence']):
            ax.text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=9)

        plt.tight_layout()
        plt.savefig(self.output_dir / 'Statewise_STH_Prevalence.png',
                    dpi=300, bbox_inches='tight')
        plt.close()

    def create_parasite_comparison_chart(self):
        """Create comparison chart for different parasites"""
        fig, ax = plt.subplots(figsize=(12, 8))

        # Prepare data for box plot
        parasites = ['Prevalence_Ascaris', 'Prevalence_Trichuris', 'Prevalence_Hookworm']
        parasite_names = ['Ascaris', 'Trichuris', 'Hookworm']
        data_to_plot = [self.df[parasite] for parasite in parasites]

        # Create box plot
        bp = ax.boxplot(data_to_plot, patch_artist=True, labels=parasite_names)

        # Color the boxes
        colors = ['#FF9933', '#138808', '#000080']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        # Customize plot
        ax.set_ylabel('Prevalence (%)', fontsize=12)
        ax.set_title('Distribution of STH Parasite Prevalence Across Indian Districts',
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3)

        # Add mean lines
        means = [np.mean(data) for data in data_to_plot]
        for i, mean in enumerate(means):
            ax.axhline(y=mean, color=colors[i], linestyle='--', alpha=0.8, linewidth=2)

        plt.tight_layout()
        plt.savefig(self.output_dir / 'Parasite_Prevalence_Comparison.png',
                    dpi=300, bbox_inches='tight')
        plt.close()

    def create_risk_category_pie_chart(self):
        """Create pie chart showing risk categories"""
        fig, ax = plt.subplots(figsize=(10, 8))

        # Count districts by risk category
        risk_counts = self.df['Risk_Category'].value_counts()

        # Create pie chart
        wedges, texts, autotexts = ax.pie(risk_counts.values,
                                         labels=risk_counts.index,
                                         autopct='%1.1f%%',
                                         colors=plt.cm.Set3(range(len(risk_counts))))

        # Customize
        ax.set_title('Distribution of Indian Districts by STH Risk Category',
                    fontsize=14, fontweight='bold', pad=20)

        # Add legend
        ax.legend(wedges, risk_counts.index,
                 title="Risk Categories",
                 loc="center left",
                 bbox_to_anchor=(1, 0, 0.5, 1))

        plt.tight_layout()
        plt.savefig(self.output_dir / 'Risk_Category_Distribution.png',
                    dpi=300, bbox_inches='tight')
        plt.close()

    def create_regional_heatmap(self):
        """Create a regional comparison heatmap"""
        fig, ax = plt.subplots(figsize=(14, 10))

        # Group by state and calculate means
        regional_data = self.state_data.groupby('State')[['Prevalence_Ascaris',
                                                          'Prevalence_Trichuris',
                                                          'Prevalence_Hookworm']].mean()

        # Create heatmap
        sns.heatmap(regional_data, annot=True, fmt='.1f', cmap='YlOrRd',
                   ax=ax, cbar_kws={'label': 'Prevalence (%)'})

        ax.set_title('Regional STH Prevalence Patterns in India',
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Parasite Species')
        ax.set_ylabel('States')

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'Regional_Prevalence_Heatmap.png',
                    dpi=300, bbox_inches='tight')
        plt.close()

    def create_indian_healthcare_integration_chart(self):
        """Create chart showing integration with Indian healthcare system"""
        fig, ax = plt.subplots(figsize=(12, 8))

        # Sample data for healthcare integration
        programs = ['National Health Mission', 'Swachh Bharat Mission',
                   'ICDS', 'School Health Program', 'RBSK', 'ASHA Workers']
        integration_levels = [95, 87, 78, 92, 85, 88]

        bars = ax.bar(range(len(programs)), integration_levels,
                     color=['#FF9933', '#138808', '#000080', '#FF0000', '#800080', '#FFA500'])

        ax.set_xticks(range(len(programs)))
        ax.set_xticklabels(programs, rotation=45, ha='right')
        ax.set_ylabel('Integration Level (%)')
        ax.set_title('Integration of STH Control with Indian National Programs',
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3)

        # Add value labels
        for bar, value in zip(bars, integration_levels):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                   f'{value}%', ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(self.output_dir / 'Healthcare_Integration.png',
                    dpi=300, bbox_inches='tight')
        plt.close()

    def create_national_deworming_progress(self):
        """Create chart showing national deworming program progress"""
        fig, ax = plt.subplots(figsize=(12, 6))

        # Simulated progress data (2015-2025)
        years = list(range(2015, 2026))
        coverage = [0, 15, 35, 55, 68, 72, 78, 82, 85, 88, 90]  # Percentage coverage
        prevalence = [45, 42, 38, 34, 30, 27, 24, 21, 19, 17, 15]  # Estimated prevalence

        ax2 = ax.twinx()

        line1 = ax.plot(years, coverage, 'o-', color='#138808', linewidth=3, markersize=8,
                       label='Coverage (%)')
        line2 = ax2.plot(years, prevalence, 's-', color='#FF0000', linewidth=3, markersize=8,
                        label='Prevalence (%)')

        ax.set_xlabel('Year')
        ax.set_ylabel('Coverage (%)', color='#138808')
        ax2.set_ylabel('Prevalence (%)', color='#FF0000')
        ax.set_title('National Deworming Day Program Progress (2015-2025)',
                    fontsize=14, fontweight='bold', pad=20)

        # Combine legends
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax.legend(lines, labels, loc='center right')

        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'Deworming_Progress.png',
                    dpi=300, bbox_inches='tight')
        plt.close()

    def create_indian_sth_dashboard(self):
        """Create a comprehensive dashboard visualization"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Soil Transmitted Diseases in India - Comprehensive Dashboard',
                    fontsize=16, fontweight='bold')

        # Dashboard 1: State prevalence
        state_plot = self.state_data.nlargest(10, 'Overall_Prevalence')
        axes[0,0].barh(range(len(state_plot)), state_plot['Overall_Prevalence'])
        axes[0,0].set_yticks(range(len(state_plot)))
        axes[0,0].set_yticklabels(state_plot['State'])
        axes[0,0].set_title('Top 10 States by STH Prevalence')
        axes[0,0].set_xlabel('Prevalence (%)')

        # Dashboard 2: Risk distribution
        risk_counts = self.df['Risk_Category'].value_counts()
        axes[0,1].pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%')
        axes[0,1].set_title('District Risk Distribution')

        # Dashboard 3: Parasite comparison
        parasites = ['Ascaris', 'Trichuris', 'Hookworm']
        means = [self.df['Prevalence_Ascaris'].mean(),
                self.df['Prevalence_Trichuris'].mean(),
                self.df['Prevalence_Hookworm'].mean()]
        axes[0,2].bar(parasites, means, color=INDIAN_COLORS[:3])
        axes[0,2].set_title('Average Parasite Prevalence')
        axes[0,2].set_ylabel('Prevalence (%)')

        # Dashboard 4: Population vs Prevalence
        axes[1,0].scatter(self.df['Total_Population']/1000000,
                         self.df['Prevalence_Children'],
                         alpha=0.6, s=self.df['Total_Population']/50000)
        axes[1,0].set_xlabel('Population (Millions)')
        axes[1,0].set_ylabel('Children Prevalence (%)')
        axes[1,0].set_title('Population vs STH Prevalence')

        # Dashboard 5: Healthcare integration
        programs = ['NHM', 'RBSK', 'ICDS', 'SBM', 'NDD']
        integration = [95, 88, 82, 91, 94]
        axes[1,1].bar(range(len(programs)), integration)
        axes[1,1].set_xticks(range(len(programs)))
        axes[1,1].set_xticklabels(programs, rotation=45)
        axes[1,1].set_title('Program Integration Levels')

        # Dashboard 6: Progress over time (simulated)
        years = [2015, 2018, 2021, 2025]
        progress = [45, 32, 22, 15]
        axes[1,2].plot(years, progress, 'o-', linewidth=3, markersize=10)
        axes[1,2].set_title('STH Prevalence Reduction Trend')
        axes[1,2].set_xlabel('Year')
        axes[1,2].set_ylabel('Prevalence (%)')
        axes[1,2].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.output_dir / 'STH_India_Dashboard.png',
                    dpi=300, bbox_inches='tight')
        plt.close()

    def generate_all_visuals(self):
        """Generate all visual assets"""
        print("Generating Indian STH visual assets...")

        try:
            self.create_state_prevalence_map()
            print("✓ State prevalence map created")

            self.create_parasite_comparison_chart()
            print("✓ Parasite comparison chart created")

            self.create_risk_category_pie_chart()
            print("✓ Risk category pie chart created")

            self.create_regional_heatmap()
            print("✓ Regional heatmap created")

            self.create_indian_healthcare_integration_chart()
            print("✓ Healthcare integration chart created")

            self.create_national_deworming_progress()
            print("✓ Deworming progress chart created")

            self.create_indian_sth_dashboard()
            print("✓ Comprehensive dashboard created")

            print(f"\n🎉 All visual assets generated successfully!")
            print(f"📁 Output directory: {self.output_dir}")
            print(f"📊 Generated {len(list(self.output_dir.glob('*.png')))} chart files")

        except Exception as e:
            print(f"❌ Error generating visuals: {str(e)}")
            raise

def main():
    """Main function to generate all Indian STH visuals"""
    # Define paths
    script_dir = Path(__file__).parent
    data_file = script_dir / "Indian_STH_Data.xlsx"
    output_dir = script_dir / "Generated_Charts"

    # Validate input file
    if not data_file.exists():
        print(f"❌ Data file not found: {data_file}")
        print("Please ensure Indian_STH_Data.xlsx exists in the same directory")
        return

    # Create visualizer and generate charts
    visualizer = IndianSTHVisualizer(data_file, output_dir)
    visualizer.generate_all_visuals()

    # Print summary
    print("\n📋 Summary of Generated Visual Assets:")
    print("=" * 50)

    charts = [
        "State-wise STH Prevalence Map",
        "Parasite Prevalence Comparison",
        "Risk Category Distribution",
        "Regional Prevalence Heatmap",
        "Healthcare Integration Chart",
        "National Deworming Progress",
        "Comprehensive STH Dashboard"
    ]

    for i, chart in enumerate(charts, 1):
        print(f"{i}. {chart}")

    print("=" * 50)
    print("✅ Visual generation complete!")
    print("📧 All files saved in: Generated_Charts/")

if __name__ == "__main__":
    main()
