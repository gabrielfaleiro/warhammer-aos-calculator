import os
import json
import matplotlib.pyplot as plt
from libs.base import BaseData
from libs.spreadsheet import SpreadsheetWarscroll, SpreadsheetArmies


def main():
    exit_code = 0

    # Load the base data
    BaseData.load_base()

    ########## Warscroll calculations ##########

    # Path to the directory containing the JSON files
    directory_path = 'data/warscrolls/skaven/'  # Update this to your directory

    # # Create figure and axis
    # fig, ax = plt.subplots()

    sp = SpreadsheetWarscroll('out/warscrolls.csv')
    sp.init_file()

    # Loop through all the files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):  # Only process JSON files
            file_path = os.path.join(directory_path, filename)

            # Open and load the JSON content
            with open(file_path, 'r') as json_file:
                try:
                    sp.append_ws(json.load(json_file))

                    ####### Plotting #######
                    # point_x_base = mean_received_damage
                    # point_y_base = mean_delivered_damage_per_points
                    # # point_y_base = mean_delivered_damage
                    #
                    # # Plot a single point for comparison
                    # sc = ax.scatter(point_x_base, point_y_base, label=ws.get('name_en'))
                    # point_color = sc.get_facecolors()[-1]
                    #
                    # point_x_improved = improved_mean_received_damage
                    # point_y_improved = improved_mean_delivered_damage_per_points
                    # # point_y_improved = improved_mean_delivered_damage
                    #
                    # ax.scatter(point_x_improved, point_y_improved, color=point_color)
                    #
                    # # Draw an arrow between the two points
                    # ax.annotate('', xy=(point_x_improved, point_y_improved),
                    #             xytext=(point_x_base, point_y_base),
                    #             arrowprops=dict(facecolor='black', arrowstyle='->', lw=2))

                except json.JSONDecodeError as e:
                    print(f"Error parsing {file_path}: {e}")
                    exit_code = 1

    # # Add labels and legend
    # ax.set_xlabel('Mean received damage')
    # ax.set_ylabel('Mean delivered damage per 100 points')
    # ax.set_title('Skaven Army')
    # ax.legend()
    #
    # # Show the plot
    # plt.grid(True)
    # plt.savefig('out/plot.png')

    ########## Army calculations ##########

    # Path to the directory containing the JSON files
    directory_path = 'data/armies/'  # Update this to your directory

    sp_armies = SpreadsheetArmies('out/armies.csv')
    sp_armies.init_file()

    # Loop through all the files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):  # Only process JSON files
            file_path = os.path.join(directory_path, filename)

            # Open and load the JSON content
            with open(file_path, 'r') as json_file:
                sp_armies.append_army(json.load(json_file))

    return exit_code


if __name__ == '__main__':
    exit(main())
