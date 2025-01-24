import pandas as pd
import numpy as np
import json

# Initialize the rating system
class FRCRatingSystem:
    def __init__(self, k_factor=32, initial_rating=1500):
        self.k_factor = k_factor
        self.initial_rating = initial_rating
        self.team_ratings = {}
        
    def get_team_rating(self, team_number):
        return self.team_ratings.get(team_number, self.initial_rating)
    
    def calculate_alliance_rating(self, teams):
        return sum(self.get_team_rating(team) for team in teams)
    
    def update_elo(self, winning_teams, losing_teams, margin_of_victory=0):
        winning_rating = self.calculate_alliance_rating(winning_teams)
        losing_rating = self.calculate_alliance_rating(losing_teams)
        
        expected_win = 1 / (1 + 10 ** ((losing_rating - winning_rating) / 400))
        k_multiplier = 1 + (margin_of_victory / 100)
        rating_change = self.k_factor * k_multiplier * (1 - expected_win)
        
        for team in winning_teams:
            current_rating = self.get_team_rating(team)
            self.team_ratings[team] = current_rating + (rating_change / 3)
            
        for team in losing_teams:
            current_rating = self.get_team_rating(team)
            self.team_ratings[team] = current_rating - (rating_change / 3)
    
    def predict_match(self, red_alliance, blue_alliance):
        red_rating = self.calculate_alliance_rating(red_alliance)
        blue_rating = self.calculate_alliance_rating(blue_alliance)
        
        rating_diff = red_rating - blue_rating
        win_probability = 1 / (1 + 10 ** (-rating_diff / 400))
        
        return {
            'red_win_probability': win_probability,
            'blue_win_probability': 1 - win_probability,
            'red_alliance_rating': red_rating,
            'blue_alliance_rating': blue_rating
        }

# Example usage with sample match data
def main():
    try:
        with open('team_ratings.json', 'r') as f:
            saved_ratings = json.load(f)
        rating_system = FRCRatingSystem(k_factor=32)
        rating_system.team_ratings = saved_ratings
        print("Loaded existing team ratings")
    except FileNotFoundError:
        rating_system = FRCRatingSystem(k_factor=32)
        print("Starting with fresh ratings")

    # Print initial ratings for teams we care about
    print("\nInitial Ratings:")
    for team in [1676, 1640, 2590, 9015, 293, 2191]:
        print(f"Team {team}: {rating_system.get_team_rating(team):.1f}")

    # Real match data from competition
    match_data = [
        {'match_number': 1, 'red_alliance': [2607, 4573, 3142], 'blue_alliance': [1257, 321, 1640], 'red_score': 65, 'blue_score': 90},
        {'match_number': 2, 'red_alliance': [341, 2191, 8513], 'blue_alliance': [272, 3314, 7045], 'red_score': 68, 'blue_score': 77},
        {'match_number': 3, 'red_alliance': [1676, 834, 5181], 'blue_alliance': [2539, 2720, 1089], 'red_score': 82, 'blue_score': 64},
        {'match_number': 4, 'red_alliance': [5401, 9027, 1218], 'blue_alliance': [1923, 1807, 2495], 'red_score': 58, 'blue_score': 110},
        {'match_number': 5, 'red_alliance': [103, 293, 1279], 'blue_alliance': [555, 5438, 7110], 'red_score': 60, 'blue_score': 49},
        {'match_number': 6, 'red_alliance': [1403, 4361, 1391], 'blue_alliance': [11, 9094, 6226], 'red_score': 71, 'blue_score': 63},
        {'match_number': 7, 'red_alliance': [316, 3637, 427], 'blue_alliance': [1811, 9015, 219], 'red_score': 91, 'blue_score': 69},
        {'match_number': 8, 'red_alliance': [4285, 4342, 75], 'blue_alliance': [5992, 714, 56], 'red_score': 83, 'blue_score': 75},
        {'match_number': 9, 'red_alliance': [5684, 7414, 102], 'blue_alliance': [1168, 365, 2590], 'red_score': 77, 'blue_score': 107},
        {'match_number': 10, 'red_alliance': [484, 2722, 6921], 'blue_alliance': [223, 5895, 222], 'red_score': 73, 'blue_score': 91},
        {'match_number': 11, 'red_alliance': [1807, 834, 4573], 'blue_alliance': [1923, 3142, 7045], 'red_score': 95, 'blue_score': 86},
        {'match_number': 12, 'red_alliance': [3314, 1640, 2191], 'blue_alliance': [9027, 1676, 103], 'red_score': 87, 'blue_score': 92},
        {'match_number': 13, 'red_alliance': [9094, 272, 293], 'blue_alliance': [2607, 5401, 7110], 'red_score': 56, 'blue_score': 65},
        {'match_number': 14, 'red_alliance': [1279, 219, 2539], 'blue_alliance': [9015, 1391, 1257], 'red_score': 79, 'blue_score': 58},
        {'match_number': 15, 'red_alliance': [4285, 11, 1403], 'blue_alliance': [2720, 8513, 427], 'red_score': 83, 'blue_score': 92},
        {'match_number': 16, 'red_alliance': [3637, 1218, 56], 'blue_alliance': [5181, 102, 4361], 'red_score': 58, 'blue_score': 62},
        {'match_number': 17, 'red_alliance': [7414, 2590, 5438], 'blue_alliance': [484, 1811, 4342], 'red_score': 67, 'blue_score': 63},
        {'match_number': 18, 'red_alliance': [1168, 2495, 714], 'blue_alliance': [5895, 321, 1089], 'red_score': 88, 'blue_score': 69},
        {'match_number': 19, 'red_alliance': [555, 5684, 2722], 'blue_alliance': [6921, 75, 316], 'red_score': 80, 'blue_score': 93},
        {'match_number': 20, 'red_alliance': [5992, 222, 6226], 'blue_alliance': [341, 223, 365], 'red_score': 47, 'blue_score': 103},
        {'match_number': 21, 'red_alliance': [219, 1923, 2191], 'blue_alliance': [2539, 1640, 9094], 'red_score': 84, 'blue_score': 102},
        {'match_number': 22, 'red_alliance': [103, 7110, 9015], 'blue_alliance': [2607, 1807, 11], 'red_score': 61, 'blue_score': 108},
        {'match_number': 23, 'red_alliance': [3314, 1218, 2720], 'blue_alliance': [7045, 56, 1279], 'red_score': 96, 'blue_score': 66},
        {'match_number': 24, 'red_alliance': [1676, 1257, 8513], 'blue_alliance': [7414, 834, 1811], 'red_score': 71, 'blue_score': 67},
        {'match_number': 25, 'red_alliance': [5181, 4285, 1168], 'blue_alliance': [484, 3637, 5438], 'red_score': 96, 'blue_score': 79},
        {'match_number': 26, 'red_alliance': [2722, 2590, 321], 'blue_alliance': [4361, 9027, 293], 'red_score': 77, 'blue_score': 73},
        {'match_number': 27, 'red_alliance': [3142, 365, 5401], 'blue_alliance': [4342, 714, 6921], 'red_score': 60, 'blue_score': 62},
        {'match_number': 28, 'red_alliance': [6226, 555, 75], 'blue_alliance': [341, 427, 102], 'red_score': 74, 'blue_score': 72},
        {'match_number': 29, 'red_alliance': [5992, 2495, 1391], 'blue_alliance': [1403, 316, 222], 'red_score': 57, 'blue_score': 89},
        {'match_number': 30, 'red_alliance': [272, 223, 1089], 'blue_alliance': [5895, 4573, 5684], 'red_score': 85, 'blue_score': 69},
        {'match_number': 31, 'red_alliance': [1923, 8513, 1811], 'blue_alliance': [7110, 56, 2720], 'red_score': 100, 'blue_score': 44},
        {'match_number': 32, 'red_alliance': [2539, 11, 484], 'blue_alliance': [1640, 1279, 1807], 'red_score': 64, 'blue_score': 102},
        {'match_number': 33, 'red_alliance': [9015, 7414, 3314], 'blue_alliance': [293, 2722, 4285], 'red_score': 78, 'blue_score': 63},
        {'match_number': 34, 'red_alliance': [2590, 9094, 219], 'blue_alliance': [365, 5181, 2607], 'red_score': 84, 'blue_score': 77},
        {'match_number': 35, 'red_alliance': [555, 341, 1168], 'blue_alliance': [4361, 714, 1676], 'red_score': 107, 'blue_score': 103},
        {'match_number': 36, 'red_alliance': [3637, 7045, 2495], 'blue_alliance': [1257, 6226, 6921], 'red_score': 79, 'blue_score': 54},
        {'match_number': 37, 'red_alliance': [4573, 316, 5992], 'blue_alliance': [5401, 2191, 5438], 'red_score': 91, 'blue_score': 46},
        {'match_number': 38, 'red_alliance': [1403, 9027, 5895], 'blue_alliance': [222, 102, 834], 'red_score': 86, 'blue_score': 58},
        {'match_number': 39, 'red_alliance': [5684, 223, 427], 'blue_alliance': [3142, 1391, 1218], 'red_score': 76, 'blue_score': 80},
        {'match_number': 40, 'red_alliance': [321, 4342, 272], 'blue_alliance': [1089, 75, 103], 'red_score': 55, 'blue_score': 86},
        {'match_number': 41, 'red_alliance': [219, 1807, 365], 'blue_alliance': [8513, 4285, 1279], 'red_score': 55, 'blue_score': 76},
        {'match_number': 42, 'red_alliance': [1811, 2607, 56], 'blue_alliance': [1676, 555, 11], 'red_score': 68, 'blue_score': 68},
        {'match_number': 43, 'red_alliance': [2720, 1640, 341], 'blue_alliance': [2590, 2495, 293], 'red_score': 117, 'blue_score': 62},
        {'match_number': 44, 'red_alliance': [714, 7110, 3314], 'blue_alliance': [7414, 4361, 4573], 'red_score': 80, 'blue_score': 58},
        {'match_number': 45, 'red_alliance': [5992, 1403, 2539], 'blue_alliance': [6921, 9027, 3637], 'red_score': 74, 'blue_score': 49},
        {'match_number': 46, 'red_alliance': [1391, 5684, 1168], 'blue_alliance': [2191, 3142, 834], 'red_score': 134, 'blue_score': 66},
        {'match_number': 47, 'red_alliance': [7045, 427, 5895], 'blue_alliance': [316, 4342, 5181], 'red_score': 49, 'blue_score': 96},
        {'match_number': 48, 'red_alliance': [1089, 5438, 102], 'blue_alliance': [321, 9094, 223], 'red_score': 46, 'blue_score': 55},
        {'match_number': 49, 'red_alliance': [103, 1257, 272], 'blue_alliance': [2722, 1923, 222], 'red_score': 73, 'blue_score': 86},
        {'match_number': 50, 'red_alliance': [75, 5401, 484], 'blue_alliance': [1218, 6226, 9015], 'red_score': 63, 'blue_score': 69},
        {'match_number': 51, 'red_alliance': [555, 2495, 4361], 'blue_alliance': [4285, 4573, 365], 'red_score': 88, 'blue_score': 67},
        {'match_number': 52, 'red_alliance': [7414, 5992, 1640], 'blue_alliance': [1807, 1403, 3314], 'red_score': 60, 'blue_score': 83},
        {'match_number': 53, 'red_alliance': [2191, 3637, 1676], 'blue_alliance': [3142, 293, 5684], 'red_score': 88, 'blue_score': 73},
        {'match_number': 54, 'red_alliance': [9027, 1279, 2607], 'blue_alliance': [714, 341, 5181], 'red_score': 79, 'blue_score': 75},
        {'match_number': 55, 'red_alliance': [102, 7110, 1811], 'blue_alliance': [1089, 4342, 219], 'red_score': 38, 'blue_score': 55},
        {'match_number': 56, 'red_alliance': [222, 7045, 9094], 'blue_alliance': [11, 427, 321], 'red_score': 73, 'blue_score': 70},
        {'match_number': 57, 'red_alliance': [316, 1168, 1257], 'blue_alliance': [2720, 103, 223], 'red_score': 86, 'blue_score': 71},
        {'match_number': 58, 'red_alliance': [2722, 75, 1391], 'blue_alliance': [56, 8513, 5401], 'red_score': 109, 'blue_score': 73},
        {'match_number': 59, 'red_alliance': [6226, 2539, 1923], 'blue_alliance': [5895, 484, 2590], 'red_score': 53, 'blue_score': 103},
        {'match_number': 60, 'red_alliance': [834, 272, 9015], 'blue_alliance': [5438, 6921, 1218], 'red_score': 60, 'blue_score': 84},
        {'match_number': 61, 'red_alliance': [1640, 5684, 2495], 'blue_alliance': [5181, 555, 7414], 'red_score': 84, 'blue_score': 70},
        {'match_number': 62, 'red_alliance': [4361, 4285, 3142], 'blue_alliance': [219, 2607, 1403], 'red_score': 76, 'blue_score': 101},
        {'match_number': 63, 'red_alliance': [3637, 222, 321], 'blue_alliance': [7110, 1279, 2191], 'red_score': 79, 'blue_score': 52},
        {'match_number': 64, 'red_alliance': [4342, 2720, 9094], 'blue_alliance': [223, 3314, 9027], 'red_score': 112, 'blue_score': 53},
        {'match_number': 65, 'red_alliance': [1391, 102, 714], 'blue_alliance': [1811, 2722, 7045], 'red_score': 65, 'blue_score': 77},
        {'match_number': 66, 'red_alliance': [341, 1257, 75], 'blue_alliance': [11, 5895, 5401], 'red_score': 69, 'blue_score': 89},
        {'match_number': 67, 'red_alliance': [427, 272, 56], 'blue_alliance': [1807, 316, 2590], 'red_score': 85, 'blue_score': 124},
        {'match_number': 68, 'red_alliance': [6226, 484, 4573], 'blue_alliance': [6921, 834, 103], 'red_score': 52, 'blue_score': 92},
        {'match_number': 69, 'red_alliance': [9015, 5438, 1923], 'blue_alliance': [365, 1676, 1089], 'red_score': 62, 'blue_score': 98},
        {'match_number': 70, 'red_alliance': [1218, 2539, 8513], 'blue_alliance': [1168, 5992, 293], 'red_score': 114, 'blue_score': 70},
        {'match_number': 71, 'red_alliance': [1279, 2720, 222], 'blue_alliance': [9094, 7414, 3142], 'red_score': 97, 'blue_score': 100},
        {'match_number': 72, 'red_alliance': [1391, 2191, 5181], 'blue_alliance': [2495, 7110, 4285], 'red_score': 87, 'blue_score': 63},
        {'match_number': 73, 'red_alliance': [1811, 11, 4361], 'blue_alliance': [5401, 3314, 5684], 'red_score': 71, 'blue_score': 99},
        {'match_number': 74, 'red_alliance': [7045, 1403, 1257], 'blue_alliance': [9027, 555, 272], 'red_score': 65, 'blue_score': 74},
        {'match_number': 75, 'red_alliance': [3637, 223, 1807], 'blue_alliance': [834, 321, 75], 'red_score': 96, 'blue_score': 55},
        {'match_number': 76, 'red_alliance': [4573, 1640, 5438], 'blue_alliance': [56, 9015, 341], 'red_score': 86, 'blue_score': 80},
        {'match_number': 77, 'red_alliance': [8513, 365, 6921], 'blue_alliance': [427, 1089, 484], 'red_score': 55, 'blue_score': 80},
        {'match_number': 78, 'red_alliance': [4342, 2607, 1923], 'blue_alliance': [1168, 6226, 2722], 'red_score': 99, 'blue_score': 59},
        {'match_number': 79, 'red_alliance': [5895, 219, 1676], 'blue_alliance': [1218, 2590, 5992], 'red_score': 93, 'blue_score': 84},
        {'match_number': 80, 'red_alliance': [316, 103, 714], 'blue_alliance': [293, 102, 2539], 'red_score': 98, 'blue_score': 62},
        {'match_number': 81, 'red_alliance': [7045, 5684, 9027], 'blue_alliance': [272, 1403, 7110], 'red_score': 56, 'blue_score': 86},
        {'match_number': 82, 'red_alliance': [223, 5401, 555], 'blue_alliance': [222, 2191, 7414], 'red_score': 93, 'blue_score': 65},
        {'match_number': 83, 'red_alliance': [2495, 1279, 834], 'blue_alliance': [75, 9015, 4361], 'red_score': 78, 'blue_score': 63},
        {'match_number': 84, 'red_alliance': [5181, 6921, 2720], 'blue_alliance': [1391, 365, 1640], 'red_score': 89, 'blue_score': 133},
        {'match_number': 85, 'red_alliance': [4573, 1168, 321], 'blue_alliance': [4285, 427, 1811], 'red_score': 58, 'blue_score': 76},
        {'match_number': 86, 'red_alliance': [1807, 341, 1676], 'blue_alliance': [4342, 2722, 3637], 'red_score': 141, 'blue_score': 64},
        {'match_number': 87, 'red_alliance': [102, 5895, 1923], 'blue_alliance': [5438, 2539, 3314], 'red_score': 106, 'blue_score': 88},
        {'match_number': 88, 'red_alliance': [293, 1089, 6226], 'blue_alliance': [56, 1257, 219], 'red_score': 76, 'blue_score': 73},
        {'match_number': 89, 'red_alliance': [484, 1218, 316], 'blue_alliance': [714, 9094, 2607], 'red_score': 73, 'blue_score': 85},
        {'match_number': 90, 'red_alliance': [2590, 3142, 103], 'blue_alliance': [8513, 5992, 11], 'red_score': 87, 'blue_score': 73},
        {'match_number': 91, 'red_alliance': [7110, 5181, 7045], 'blue_alliance': [223, 9015, 1403], 'red_score': 59, 'blue_score': 92},
        {'match_number': 92, 'red_alliance': [9027, 222, 365], 'blue_alliance': [75, 1811, 4573], 'red_score': 73, 'blue_score': 70},
        {'match_number': 93, 'red_alliance': [427, 1168, 834], 'blue_alliance': [2722, 5401, 1640], 'red_score': 72, 'blue_score': 78},
        {'match_number': 94, 'red_alliance': [5684, 6921, 4285], 'blue_alliance': [1923, 341, 1279], 'red_score': 82, 'blue_score': 120},
        {'match_number': 95, 'red_alliance': [4361, 56, 4342], 'blue_alliance': [2495, 272, 2539], 'red_score': 70, 'blue_score': 70},
        {'match_number': 96, 'red_alliance': [1257, 293, 2191], 'blue_alliance': [102, 484, 1807], 'red_score': 33, 'blue_score': 78},
        {'match_number': 97, 'red_alliance': [1218, 1089, 7414], 'blue_alliance': [6226, 316, 3142], 'red_score': 74, 'blue_score': 76},
        {'match_number': 98, 'red_alliance': [11, 2720, 714], 'blue_alliance': [5438, 219, 5992], 'red_score': 71, 'blue_score': 78},
        {'match_number': 99, 'red_alliance': [9094, 5895, 555], 'blue_alliance': [8513, 103, 3637], 'red_score': 97, 'blue_score': 101},
        {'match_number': 100, 'red_alliance': [3314, 1676, 2590], 'blue_alliance': [321, 2607, 1391], 'red_score': 97, 'blue_score': 92},
        {'match_number': 101, 'red_alliance': [1640, 1923, 4285], 'blue_alliance': [75, 7045, 223], 'red_score': 102, 'blue_score': 58},
        {'match_number': 102, 'red_alliance': [365, 56, 2722], 'blue_alliance': [2539, 1168, 7110], 'red_score': 97, 'blue_score': 74},
        {'match_number': 103, 'red_alliance': [293, 1811, 5401], 'blue_alliance': [1279, 5181, 1403], 'red_score': 60, 'blue_score': 107},
        {'match_number': 104, 'red_alliance': [3142, 1807, 9027], 'blue_alliance': [1089, 4361, 316], 'red_score': 85, 'blue_score': 70},
        {'match_number': 105, 'red_alliance': [2191, 6921, 11], 'blue_alliance': [102, 1218, 4342], 'red_score': 50, 'blue_score': 96},
        {'match_number': 106, 'red_alliance': [272, 7414, 6226], 'blue_alliance': [834, 5992, 9094], 'red_score': 106, 'blue_score': 76},
        {'match_number': 107, 'red_alliance': [1676, 5438, 2607], 'blue_alliance': [2495, 222, 8513], 'red_score': 76, 'blue_score': 63},
        {'match_number': 108, 'red_alliance': [9015, 4573, 555], 'blue_alliance': [2720, 1391, 5895], 'red_score': 49, 'blue_score': 114},
        {'match_number': 109, 'red_alliance': [714, 2590, 427], 'blue_alliance': [3314, 3637, 1257], 'red_score': 105, 'blue_score': 83},
        {'match_number': 110, 'red_alliance': [103, 321, 484], 'blue_alliance': [5684, 219, 341], 'red_score': 79, 'blue_score': 105},
        {'match_number': 111, 'red_alliance': [7110, 75, 9027], 'blue_alliance': [56, 3142, 1168], 'red_score': 72, 'blue_score': 87},
        {'match_number': 112, 'red_alliance': [1403, 1089, 2722], 'blue_alliance': [2191, 4285, 1218], 'red_score': 106, 'blue_score': 74},
        {'match_number': 113, 'red_alliance': [834, 293, 316], 'blue_alliance': [365, 11, 4342], 'red_score': 96, 'blue_score': 85},
        {'match_number': 114, 'red_alliance': [1279, 6226, 102], 'blue_alliance': [1640, 1676, 272], 'red_score': 68, 'blue_score': 108},
        {'match_number': 115, 'red_alliance': [6921, 1811, 5895], 'blue_alliance': [9094, 4361, 1807], 'red_score': 83, 'blue_score': 80},
        {'match_number': 116, 'red_alliance': [5401, 2539, 3637], 'blue_alliance': [2607, 7045, 2720], 'red_score': 97, 'blue_score': 84},
        {'match_number': 117, 'red_alliance': [219, 484, 223], 'blue_alliance': [4573, 3314, 2495], 'red_score': 70, 'blue_score': 61},
        {'match_number': 118, 'red_alliance': [222, 714, 9015], 'blue_alliance': [2590, 8513, 5684], 'red_score': 83, 'blue_score': 90},
        {'match_number': 119, 'red_alliance': [321, 5181, 5992], 'blue_alliance': [1257, 1923, 555], 'red_score': 70, 'blue_score': 78},
        {'match_number': 120, 'red_alliance': [5438, 103, 341], 'blue_alliance': [427, 1391, 7414], 'red_score': 109, 'blue_score': 115},
    ]
    
    print("\nProcessing Match History:")
    try:
        for match in match_data:
            margin = abs(match['red_score'] - match['blue_score'])
            
            if match['red_score'] > match['blue_score']:
                rating_system.update_elo(
                    match['red_alliance'],
                    match['blue_alliance'],
                    margin
                )
            elif match['blue_score'] > match['red_score']:
                rating_system.update_elo(
                    match['blue_alliance'],
                    match['red_alliance'],
                    margin
                )
            
            # Print ratings after each match that involves our teams of interest
            teams_of_interest = set([1676, 1640, 2590, 9015, 293, 2191])
            match_teams = set(match['red_alliance'] + match['blue_alliance'])
            if teams_of_interest & match_teams:
                print(f"\nAfter Match {match['match_number']}:")
                for team in teams_of_interest & match_teams:
                    print(f"Team {team}: {rating_system.get_team_rating(team):.1f}")

        # Save the updated ratings
        with open('team_ratings.json', 'w') as f:
            json.dump(rating_system.team_ratings, f)
        print("\nSaved team ratings")

    except Exception as e:
        print(f"Error processing matches: {e}")
        return
    
    # After processing all historical matches, predict the upcoming match
    print("\nPredicting Upcoming Match:")
    upcoming_match = {
        'red_alliance': [1676, 1640, 2590],  # Teams that appeared in previous matches
        'blue_alliance': [75, 7110, 6027]  # Teams that appeared in previous matches
    }
    
    try:
        prediction = rating_system.predict_match(
            upcoming_match['red_alliance'],
            upcoming_match['blue_alliance']
        )
        
        # Format output with more precision
        print(f"\nRed Alliance ({', '.join(map(str, upcoming_match['red_alliance']))})")
        print(f"Win Probability: {prediction['red_win_probability']:.2%}")
        print(f"Alliance Rating: {prediction['red_alliance_rating']:.1f}")
        
        print(f"\nBlue Alliance ({', '.join(map(str, upcoming_match['blue_alliance']))})")
        print(f"Win Probability: {prediction['blue_win_probability']:.2%}")
        print(f"Alliance Rating: {prediction['blue_alliance_rating']:.1f}")
        
        # Add rating difference for context
        rating_diff = abs(prediction['red_alliance_rating'] - prediction['blue_alliance_rating'])
        print(f"\nRating Difference: {rating_diff:.1f}")
        
    except Exception as e:
        print(f"Error making prediction: {e}")

if __name__ == "__main__":
    main()