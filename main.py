import os
import json
from libs.base import BaseData
from libs.warscroll import WarScroll

import matplotlib.pyplot as plt
import numpy as np


def main():
    exit_code = 0

    BaseData.load_base()
    # Path to the directory containing the JSON files
    directory_path = './data/warscrolls/skaven-units/'  # Update this to your directory

    # Create figure and axis
    fig, ax = plt.subplots()

    # # Create data for the diagonal line y = x
    # x = np.linspace(0, 10, 100)  # 100 points from 0 to 10
    # y = x  # Diagonal line
    #
    # # Plot the diagonal line
    # ax.plot(x, y, label='Diagonal', color='blue')

    # Loop through all the files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):  # Only process JSON files
            file_path = os.path.join(directory_path, filename)

            # Open and load the JSON content
            with open(file_path, 'r') as json_file:
                try:
                    ws = WarScroll(json.load(json_file))
                    # Base calculations
                    ws.do_calculations()

                    point_x_base = ws.calculations['mean_received_damage']
                    point_y_base = ws.calculations['mean_delivered_damage_per_points']
                    # point_y_base = ws.calculations['mean_delivered_damage']

                    # Plot a single point for comparison
                    sc = ax.scatter(point_x_base, point_y_base, label=ws.get('name'))
                    point_color = sc.get_facecolors()[-1]
                    # Improved calculations
                    ws.do_calculations(True)

                    point_x_improved = ws.calculations['mean_received_damage']
                    point_y_improved = ws.calculations['mean_delivered_damage_per_points']
                    # point_y_improved = ws.calculations['mean_delivered_damage']

                    ax.scatter(point_x_improved, point_y_improved, color=point_color)

                    # Draw an arrow between the two points
                    ax.annotate('', xy=(point_x_improved, point_y_improved),
                                xytext=(point_x_base, point_y_base),
                                arrowprops=dict(facecolor='black', arrowstyle='->', lw=2))

                except json.JSONDecodeError as e:
                    print(f"Error parsing {file_path}: {e}")
                    exit_code = 1

    # Add labels and legend
    ax.set_xlabel('Mean received damage')
    ax.set_ylabel('Mean delivered damage per 100 points')
    ax.set_title('Skaven Army')
    ax.legend()

    # Show the plot
    plt.grid(True)
    plt.show()

    return exit_code


if __name__ == '__main__':
    exit(main())
