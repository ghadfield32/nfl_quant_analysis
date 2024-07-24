# File: src/features/next_gen_data.py

import pandas as pd
import requests 
from bs4 import BeautifulSoup 
import re
import json
import os
import urllib.request
import cv2
import numpy as np
from skimage.morphology import skeletonize
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment

def scrape_next_gen_data(teams, seasons, weeks):
    pattern = re.compile("charts")
    all_charts = []

    print("Scraping images and html data...")

    for team in teams:
        for season in seasons:
            print(f"Processing {team} for season {season}")
            for week in weeks:
                URL = f"https://nextgenstats.nfl.com/charts/list/route/{team}/{season}/{week}"
                try:
                    r = requests.get(URL)
                    soup = BeautifulSoup(r.content, "html.parser")
                    script = soup.find_all("script", string=pattern)  # Use 'string' instead of 'text'
                    
                    if len(script) == 0:
                        print(f"No chart data found for {team} in {season} week {week}")
                        continue
                    
                    # Print the first 200 characters of the script content for debugging
                    print(f"Script content preview for {team} {season} week {week}: {script[0].string[:200]}")
                    
                    contains_charts = json.loads(str(script[0].string)[33:-131])

                    if len(contains_charts["charts"]["charts"]) != 0:
                        print(f"Found {len(contains_charts['charts']['charts'])} charts for {team} in {season} week {week}")
                        for chart in contains_charts["charts"]["charts"]:
                            chart["team"] = team
                            chart["season"] = season
                            chart["week"] = week
                            all_charts.append(chart)
                    else:
                        print(f"No charts found for {team} in {season} week {week}")

                except Exception as e:
                    print(f"Error processing {URL}: {str(e)}")
                    continue

    print(f"Done scraping. Total charts found: {len(all_charts)}")
    return all_charts

def save_chart_images(charts, base_folder="Route_Charts"):
    print("Saving chart images...")
    for chart in charts:
        team = chart["team"]
        season = chart["season"]
        week = chart["week"]
        name = f"{chart['lastName']}_{chart['firstName']}_{chart['position']}"

        folder = os.path.join(base_folder, team, season, week)
        img_folder = os.path.join(folder, "images")
        os.makedirs(img_folder, exist_ok=True)

        img_file = os.path.join(img_folder, f"{name}.jpeg")
        url = "https:" + chart["extraLargeImg"]
        
        try:
            urllib.request.urlretrieve(url, img_file)
        except Exception as e:
            print(f"Error saving image for {name}: {str(e)}")
    
    print("Done saving images.")

def clean_chart_image(image_path, clean_path="Cleaned_Route_Charts"):
    img_name = os.path.basename(image_path).split(".")[0]
    img = cv2.imread(image_path)

    if img.shape[0:2] == (1200, 1200):
        crop_img = img[0:680, 0:1200]
        temp_name = f"{img_name}_temp.jpg"
        cv2.imwrite(temp_name, crop_img)
        
        # Assume clean_field function is defined elsewhere
        clean_img = clean_field(temp_name)
        
        write_path = os.path.join(clean_path, *image_path.split(os.sep)[1:-1])
        os.makedirs(write_path, exist_ok=True)

        if clean_img is not None:
            write_name = os.path.join(write_path, f"{img_name}.jpeg")
            cv2.imwrite(write_name, clean_img)
        
        os.remove(temp_name)
    else:
        print(f"Image {image_path} must be of size (1200, 1200)")

def map_route_locations(image,td):
    lower_green = np.array([40,100, 100])
    upper_green = np.array([80, 255, 255])

    lower_white = np.array([230, 230, 230])
    upper_white = np.array([255, 255, 255])

    lower_gray = np.array([126, 126, 126])
    upper_gray = np.array([132, 132, 132])
    col_names = ["route_type", "x", "y"]
    route_locations = pd.DataFrame(columns = col_names)

    image = cv2.imread(image)
    row, col = image.shape[0:2]
    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask2 = cv2.inRange(image, lower_white, upper_white)
    mask3 = cv2.inRange(image, lower_gray, upper_gray)

    # Bitwise-AND mask and original image
    c_pixels = cv2.bitwise_and(image, image, mask=mask2)
    c_pixels = c_pixels.clip(0,1)
    ske_c = skeletonize(c_pixels[:,:,1]).astype(np.uint8)
    
    yac_pixels = cv2.bitwise_and(image, image, mask=mask)
    yac_pixels = cv2.cvtColor(yac_pixels, cv2.COLOR_HSV2BGR).clip(0,1)
    ske_yac = skeletonize(yac_pixels[:,:,2]).astype(np.uint8)
    
    inc_pixels = cv2.bitwise_and(image, image, mask=mask3)
    inc_pixels = inc_pixels.clip(0,1)
    ske_inc = skeletonize(inc_pixels[:,:,1]).astype(np.uint8)
    

    x,y = np.where(ske_c != 0)
    X = np.stack((x,y),axis=1 )
    c_routes = X
   
    x,y = np.where(ske_yac != 0)
    X = np.stack((x,y),axis=1 )
    yac_routes = X

    x,y = np.where(ske_inc != 0)
    X = np.stack((x,y),axis=1 )
    inc_routes = X


    sideline = 40 # pixels
    width = 53.33 # standard width of football field
    center_x = col/2

    if col > 1370:
        _75_yd_line = 0
        LOS = 596

        _1_yd_x = float(col - sideline*2)/width
        _1_yd_y = float(LOS - _75_yd_line)/75

    else:
        _55_yd_line = 5
        LOS = 572
        _1_yd_x = float(col - sideline*2)/width
        _1_yd_y = float(LOS - _55_yd_line)/55

    route_type='COMPLETE'
    y = c_routes[:,0]
    x = c_routes[:,1]
    y_loc = (LOS - y)/_1_yd_y
    x_loc = (x - center_x)/_1_yd_x
    loc = [x_loc,y_loc]
    t_loc = np.transpose(loc)
    
    # TOUCHDOWN REMOVAL CODE
    # - Very very crude method of removing TD annotations from
    # the charts. If anyone has better ideas (computer vision is likely the way to go here),
    #please do not hesitate to reach out
    for t in range(0,td):
        old_minimum=20
        new_points = np.zeros(shape=(102,2))
        final_points = new_points.copy()
        for i in range(0,275):
        #     print(i*.5)
            for j in range(0,275):
                new_points[:,0] = td_points[:,0]-i*.2
                new_points[:,1] = td_points[:,1]+j*.2
                C = cdist(t_loc, new_points)
                minimum = sum(C.min(axis=0))
                if minimum < old_minimum:
                    old_minimum=minimum
                    td_row, td_col = linear_sum_assignment(C)
                    final_points = new_points.copy()
        try:
            td_row

        except:
            print('couldn''t find TD')
            break

        td_rows =list(td_row)
        mask = np.ones(len(t_loc), dtype=bool)
        mask[td_rows] = False
        t_loc = t_loc[mask]
    
    df = pd.DataFrame(t_loc,columns=['x','y'])
    df['route_type'] = route_type
    route_locations = route_locations.append(df, ignore_index=True)

    route_type='YAC'
    y = yac_routes[:,0]
    x = yac_routes[:,1]
    y_loc = (LOS - y)/_1_yd_y
    x_loc = (x - center_x)/_1_yd_x
    loc = [x_loc,y_loc]
    t_loc = np.transpose(loc)
    df = pd.DataFrame(t_loc,columns=['x','y'])
    df['route_type'] = route_type
    route_locations = route_locations.append(df, ignore_index=True)

    route_type='INCOMPLETE'
    y = inc_routes[:,0]
    x = inc_routes[:,1]
    y_loc = (LOS - y)/_1_yd_y
    x_loc = (x - center_x)/_1_yd_x
    loc = [x_loc,y_loc]
    t_loc = np.transpose(loc)
    df = pd.DataFrame(t_loc,columns=['x','y'])
    df['route_type'] = route_type
    route_locations = route_locations.append(df, ignore_index=True)
    
    return route_locations

def process_next_gen_data(charts, base_folder="Route_Charts", clean_folder="Cleaned_Route_Charts"):
    print("Processing Next Gen data...")
    routes = pd.DataFrame(columns=["game_id", "team", "week", "name", "position", "route_type", "x", "y"])

    for chart in charts:
        team = chart["team"]
        season = chart["season"]
        week = chart["week"]
        name = f"{chart['lastName']}_{chart['firstName']}_{chart['position']}"

        image_path = os.path.join(base_folder, team, season, week, "images", f"{name}.jpeg")
        clean_chart_image(image_path, clean_folder)

        clean_image_path = os.path.join(clean_folder, team, season, week, "images", f"{name}.jpeg")
        
        if os.path.exists(clean_image_path):
            route_data = map_route_locations(clean_image_path, chart["touchdowns"])
            
            game_data = pd.DataFrame({
                "game_id": [chart["gameId"]],
                "team": [team],
                "week": [week],
                "name": [f"{chart['firstName']} {chart['lastName']}"],
                "position": [chart["position"]]
            })
            
            game_data = pd.concat([game_data] * len(route_data), ignore_index=True)
            route_df = pd.concat([game_data, route_data], axis=1)
            routes = routes.append(route_df, ignore_index=True)

    print("Done processing.")
    return routes

def load_next_gen_data():
    try:
        pass_data = pd.read_csv('../data/next_gen/all_pass_locations.csv')
        game_data = pd.read_csv('../data/next_gen/pass_and_game_data.csv')
        return pass_data, game_data
    except FileNotFoundError:
        print("Next Gen data files not found. Please run the scraping and processing functions first.")
        return None, None

def analyze_next_gen_data(pass_data, game_data, player_name):
    if pass_data is None or game_data is None:
        return None, None
    player_passes = pass_data[pass_data['name'] == player_name]
    player_games = game_data[game_data['name'] == player_name]
    return player_passes, player_games

def main():
    teams = ["arizona-cardinals", "atlanta-falcons", ..., "washington-redskins"]  # Add all teams
    seasons = ['2023']  # Update with the desired seasons
    weeks = ["1", "2", "3", ..., "17", "wild-card", "divisional", "conference", "super-bowl"]  # Add all weeks

    charts = scrape_next_gen_data(teams, seasons, weeks)
    save_chart_images(charts)
    routes = process_next_gen_data(charts)

    # Save the processed data
    routes.to_csv("../data/next_gen/all_pass_locations.csv", index=False)
    
    # You may want to create game_data separately or extract it from the routes DataFrame
    game_data = routes[["game_id", "team", "week", "name", "position"]].drop_duplicates()
    game_data.to_csv("../data/next_gen/pass_and_game_data.csv", index=False)

if __name__ == "__main__":
    main()
