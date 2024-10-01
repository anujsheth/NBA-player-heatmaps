import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import numpy as np
import pandas as pd
from user_input import collect_data
from draw_court import draw_court

shots_df, title = collect_data()

num_shots = len(shots_df)

grouped_dfs = {region: group for region, group in shots_df.groupby('SHOT_ZONE_BASIC')}
Paint = grouped_dfs.get('In The Paint (Non-RA)', pd.DataFrame())
Paint_RA = grouped_dfs.get('Restricted Area', pd.DataFrame())
Left_Corner_3 = grouped_dfs.get('Left Corner 3', pd.DataFrame())
Right_Corner_3 = grouped_dfs.get('Right Corner 3', pd.DataFrame())

Other_3s = grouped_dfs['Above the Break 3']
grouped_dfs_3s = {region: group for region, group in Other_3s.groupby('SHOT_ZONE_AREA')}
Left_Center_3 = grouped_dfs_3s.get('Left Side Center(LC)', pd.DataFrame())
Right_Center_3 = grouped_dfs_3s.get('Right Side Center(RC)', pd.DataFrame())
Center_3 = grouped_dfs_3s.get('Center(C)', pd.DataFrame())

Midranges = grouped_dfs['Mid-Range']
grouped_dfs_mid = {region: group for region, group in Midranges.groupby('SHOT_ZONE_AREA')}
Left_Mid = grouped_dfs_mid.get('Left Side(L)', pd.DataFrame())
Left_Center_Mid = grouped_dfs_mid.get('Left Side Center(LC)', pd.DataFrame())
Right_Mid = grouped_dfs_mid.get('Right Side(R)', pd.DataFrame())
Right_Center_Mid = grouped_dfs_mid.get('Right Side Center(RC)', pd.DataFrame())
Center_Mid = grouped_dfs_mid.get('Center(C)', pd.DataFrame())

regions_dfs = {
    'Paint': Paint,
    'Paint_RA': Paint_RA,
    'Left_Corner_3': Left_Corner_3,
    'Right_Corner_3': Right_Corner_3,
    'Left_Center_3': Left_Center_3,
    'Right_Center_3': Right_Center_3,
    'Center_3': Center_3,
    'Left_Mid': Left_Mid,
    'Left_Center_Mid': Left_Center_Mid,
    'Right_Mid': Right_Mid,
    'Right_Center_Mid': Right_Center_Mid,
    'Center_Mid': Center_Mid
}

cmap = plt.get_cmap('coolwarm')
cmaps_values = {}

percents = {}
for region, df in regions_dfs.items():
    if len(df) > 0:
        percents[region] = df['SHOT_MADE_FLAG'].sum() / len(df)
    else:
        percents[region] = 0
    if "3" in region:
        percents[region] *= 1.5

max_per = max(percents.values())
min_per = min(percents.values())
for region, percent in percents.items():
    percents[region] = (percent - min_per) / (max_per - min_per)
    cmaps_values[region] = cmap(percents[region])

def get_hex_data(region_df, num_shots):
    if len(region_df) > 0:
        region_hex = plt.hexbin(x = region_df["LOC_X"], y = region_df["LOC_Y"], gridsize = 25 , bins = "log", extent = (-250, 250, -47.5, 422.5))
        region_points = region_hex.get_offsets()
        region_quantities = region_hex.get_array()
        region_sizes = region_quantities / num_shots
        plt.close()
        return region_points, region_sizes
    else:
        region_points = np.empty((0, 2))
        region_sizes = np.empty(0)
        return region_points, region_sizes

hex_data_points = {}
hex_data_sizes = {}
for region, df in regions_dfs.items():
    points, sizes = get_hex_data(df, num_shots)
    hex_data_points[region] = points
    hex_data_sizes[region] = sizes

max_size = np.max(np.concatenate([arr for arr in hex_data_sizes.values()]))
multiplier = 100 / max_size

for region in hex_data_sizes:
    hex_data_sizes[region] *= multiplier

def custom_log_round(array):

    rounded_array = np.empty_like(array)

    for i, value in enumerate(array):
        
        if value == 0:
            rounded_array[i] = 0
        else:
            log_value = np.log(value) / np.log(2.5)
            if log_value <= 1:
                rounded_array[i] = 0
            elif log_value <= 2:
                rounded_array[i] = 25
            elif log_value <= 3:
                rounded_array[i] = 50
            elif log_value <= 4:
                rounded_array[i] = 75
            else:
                rounded_array[i] = 100

    return rounded_array

for region in hex_data_sizes:
    hex_data_sizes[region] = custom_log_round(hex_data_sizes[region])

for region in regions_dfs:
    plt.scatter(x = hex_data_points[region][:, 0], y = hex_data_points[region][:, 1], s = hex_data_sizes[region], color = cmaps_values[region], marker = 'h')

plt.scatter(x = -110, y = 375, s = 100, color = cmap(0.5), marker = 'h')
plt.scatter(x = -131.5, y = 375, s = 75, color = cmap(0.5), marker = 'h')
plt.scatter(x = -152, y = 375, s = 50, color = cmap(0.5), marker = 'h')
plt.scatter(x = -170, y = 375, s = 25, color = cmap(0.5), marker = 'h')

plt.title(title)
plt.axis('off')
plt.xlim(-250, 250)
plt.ylim(-47.5, 422.5)
draw_court(outer_lines=True)

norm = Normalize(vmin = 0, vmax = 1)
sm = ScalarMappable(norm = norm, cmap = cmap)
sm.set_array([])

cbar_ax = plt.gcf().add_axes([0.65, 0.8, 0.1, 0.02])  # [left, bottom, width, height]

cbar = plt.colorbar(sm, cax = cbar_ax, orientation = 'horizontal')
cbar.ax.set_xticks([])
cbar.outline.set_edgecolor('none')
plt.text(-0.5, 0.15, "~" + str(int(round(100 * min_per, 0))) + "%", fontsize = "x-small")
plt.text(1.05, 0.15, "~" + str(int(round(100 * max_per, 0))) + "%", fontsize = "x-small")
plt.text(0.25, 1.5, "eFG%", fontsize = "small")

plt.text(-3.75, 1.5, "Shot Quantity", fontsize = "small")
plt.text(-4.15, -0.15, "Low", fontsize = "x-small")
plt.text(-2.45, -0.15, "High", fontsize = "x-small")

plt.show()
