"""
Advanced visualization module for pumping lemma demonstrations
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
from typing import List, Dict, Any
import streamlit as st

class PumpingVisualizer:
    def __init__(self):
        self.colors = {
            'x': '#1f77b4', 'y': '#ff7f0e', 'z': '#2ca02c',
            'u': '#d62728', 'v': '#9467bd', 'w': '#8c564b',
            'x_cfl': '#e377c2', 'y_cfl': '#7f7f7f',
            'pumped': '#ffff00', 'background': '#f0f0f0'
        }
    
    def create_regular_pumping_visualization(self, decomposition: Dict, iterations: List[Dict], result: Dict) -> plt.Figure:
        """
        Create visualization for regular language pumping
        """
        if not iterations:
            # Create a simple error figure
            fig, ax = plt.subplots(figsize=(10, 2))
            ax.text(0.5, 0.5, "No iterations to visualize", ha='center', va='center', fontsize=12)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_xticks([])
            ax.set_yticks([])
            return fig
        
        fig, axes = plt.subplots(1, len(iterations), figsize=(15, 4))
        if len(iterations) == 1:
            axes = [axes]
        
        fig.suptitle(f'Regular Pumping Lemma - {result["language_type"]}', fontsize=16, fontweight='bold')
        
        for idx, iteration in enumerate(iterations):
            ax = axes[idx]
            self._plot_regular_iteration(ax, iteration, idx)
        
        plt.tight_layout()
        return fig
    
    def create_cfl_pumping_visualization(self, decomposition: Dict, iterations: List[Dict], result: Dict) -> plt.Figure:
        """
        Create visualization for CFL pumping
        """
        if not iterations:
            # Create a simple error figure
            fig, ax = plt.subplots(figsize=(10, 2))
            ax.text(0.5, 0.5, "No iterations to visualize", ha='center', va='center', fontsize=12)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_xticks([])
            ax.set_yticks([])
            return fig
        
        fig, axes = plt.subplots(1, len(iterations), figsize=(18, 4))
        if len(iterations) == 1:
            axes = [axes]
        
        fig.suptitle(f'CFL Pumping Lemma - {result["language_type"]}', fontsize=16, fontweight='bold')
        
        for idx, iteration in enumerate(iterations):
            ax = axes[idx]
            self._plot_cfl_iteration(ax, iteration, idx)
        
        plt.tight_layout()
        return fig
    
    def _plot_regular_iteration(self, ax, iteration: Dict, iteration_idx: int):
        """
        Plot a single iteration for regular pumping
        """
        parts = iteration['parts']
        x = parts['x']
        y = parts['y']
        z = parts['z']
        y_repetitions = parts['y_repetitions']  # This is an integer
        
        # Create the pumped string - FIXED: Use string repetition, not integer addition
        pumped_y = y * y_repetitions  # This correctly repeats the string
        full_string = x + pumped_y + z
        
        # Calculate positions
        x_pos = 0
        y_pos = len(x)
        z_pos = y_pos + len(pumped_y)
        
        # Plot background for entire string
        ax.add_patch(patches.Rectangle((0, 0.4), len(full_string), 0.2, 
                                     facecolor='lightgray', alpha=0.3))
        
        # Plot x part
        if x:
            ax.add_patch(patches.Rectangle((x_pos, 0.4), len(x), 0.2, 
                                         facecolor=self.colors['x'], alpha=0.7))
            ax.text(x_pos + len(x)/2, 0.5, f'x\n"{x}"', 
                   ha='center', va='center', fontweight='bold')
        
        # Plot y part (may be pumped)
        if pumped_y:
            color = self.colors['pumped'] if iteration_idx > 1 else self.colors['y']
            ax.add_patch(patches.Rectangle((y_pos, 0.4), len(pumped_y), 0.2, 
                                         facecolor=color, alpha=0.7))
            y_label = f'y^{iteration["i"]}\n"{pumped_y}"' if iteration["i"] != 1 else f'y\n"{y}"'
            ax.text(y_pos + len(pumped_y)/2, 0.5, y_label, 
                   ha='center', va='center', fontweight='bold')
        
        # Plot z part
        if z:
            ax.add_patch(patches.Rectangle((z_pos, 0.4), len(z), 0.2, 
                                         facecolor=self.colors['z'], alpha=0.7))
            ax.text(z_pos + len(z)/2, 0.5, f'z\n"{z}"', 
                   ha='center', va='center', fontweight='bold')
        
        # Set up the plot
        ax.set_xlim(0, len(full_string))
        ax.set_ylim(0, 1)
        ax.set_title(f'i = {iteration["i"]}\n"{full_string}"\n'
                    f'{"✓" if iteration["in_language"] else "✗"}', 
                    color='green' if iteration["in_language"] else 'red')
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
    
    def _plot_cfl_iteration(self, ax, iteration: Dict, iteration_idx: int):
        """
        Plot a single iteration for CFL pumping
        """
        parts = iteration['parts']
        u = parts['u']
        v = parts['v']
        w = parts['w']
        x = parts['x']
        y = parts['y']
        v_reps = parts['v_repetitions']  # integer
        x_reps = parts['x_repetitions']  # integer
        
        # Create pumped strings - FIXED: Use string repetition
        pumped_v = v * v_reps
        pumped_x = x * x_reps
        full_string = u + pumped_v + w + pumped_x + y
        
        # Calculate positions
        positions = {
            'u': 0,
            'v': len(u),
            'w': len(u) + len(pumped_v),
            'x': len(u) + len(pumped_v) + len(w),
            'y': len(u) + len(pumped_v) + len(w) + len(pumped_x)
        }
        
        # Plot background
        ax.add_patch(patches.Rectangle((0, 0.3), len(full_string), 0.4, 
                                     facecolor='lightgray', alpha=0.3))
        
        # Plot each part
        parts_data = [
            ('u', u, self.colors['u']),
            ('v', pumped_v, self.colors['pumped'] if iteration_idx > 1 else self.colors['v']),
            ('w', w, self.colors['w']),
            ('x', pumped_x, self.colors['pumped'] if iteration_idx > 1 else self.colors['x_cfl']),
            ('y', y, self.colors['y_cfl'])
        ]
        
        for part_name, part_text, color in parts_data:
            pos = positions[part_name]
            if part_text:
                ax.add_patch(patches.Rectangle((pos, 0.3), len(part_text), 0.4, 
                                             facecolor=color, alpha=0.7))
                
                label = part_name
                if part_name in ['v', 'x'] and iteration_idx > 1:
                    rep_count = v_reps if part_name == 'v' else x_reps
                    label = f'{part_name}^{rep_count}'
                
                ax.text(pos + len(part_text)/2, 0.5, f'{label}\n"{part_text}"', 
                       ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Set up the plot
        ax.set_xlim(0, len(full_string))
        ax.set_ylim(0, 1)
        ax.set_title(f'i = {iteration["i"]}\n"{full_string}"\n'
                    f'{"✓" if iteration["in_language"] else "✗"}', 
                    color='green' if iteration["in_language"] else 'red',
                    fontsize=10)
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
    
    def create_comparison_chart(self, results: List[Dict]) -> plt.Figure:
        """
        Create comparison chart for multiple language analyses
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        languages = [r.get('language_type', 'Unknown') for r in results]
        lemma_holds = [r.get('lemma_holds', False) for r in results]
        
        # Bar chart for lemma results
        colors = ['red' if not holds else 'green' for holds in lemma_holds]
        bars = ax1.bar(range(len(languages)), lemma_holds, color=colors, alpha=0.7)
        ax1.set_xticks(range(len(languages)))
        ax1.set_xticklabels(languages, rotation=45)
        ax1.set_ylabel('Pumping Lemma Holds')
        ax1.set_title('Pumping Lemma Results by Language Type')
        
        # Add value labels on bars
        for bar, holds in zip(bars, lemma_holds):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    'Holds' if holds else 'Fails',
                    ha='center', va='bottom')
        
        # Pie chart for language classification
        lang_types = {}
        for lang_type in languages:
            lang_types[lang_type] = lang_types.get(lang_type, 0) + 1
        
        if lang_types:
            ax2.pie(lang_types.values(), labels=lang_types.keys(), autopct='%1.1f%%',
                   startangle=90, colors=plt.cm.Set3(np.linspace(0, 1, len(lang_types))))
            ax2.set_title('Language Type Distribution')
        
        plt.tight_layout()
        return fig
    
    def create_animation(self, iterations: List[Dict], lemma_type: str = "regular"):
        """
        Create animated visualization (simplified for Streamlit)
        """
        st.warning("Full animation requires matplotlib animation support. Showing static progression instead.")
        
        # Create a multi-step visualization
        if lemma_type == "regular":
            return self.create_regular_pumping_visualization(
                iterations[0]['parts'] if iterations else {}, iterations, {"language_type": "Animation"}
            )
        else:
            return self.create_cfl_pumping_visualization(
                iterations[0]['parts'] if iterations else {}, iterations, {"language_type": "Animation"}
            )