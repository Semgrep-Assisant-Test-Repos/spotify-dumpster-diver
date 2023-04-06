from spotify.spotify_wrapper import SpotifyWrapper
from django.shortcuts import render
import os

# Create your views here.
def index(request):
    
    ## Call your data processing functions here
    ## This is what gets called when a user hits the website index/root directory "/"
    wrapper = SpotifyWrapper()
    tracks_df = wrapper.get_user_recent_tracks(limit=50)
    print('f RECENT SONGS {tracks_df}')

    # Extract seed artists, genres, and tracks
    seed_artists = tracks_df['artist_id'].tolist()
    seed_tracks = tracks_df['track_id'].tolist()

    flat_genres = list(set([genre for genres in tracks_df['genres'] for genre in genres]))
    seed_genres = flat_genres[:5]

    # TODO handle the case if the paarams are too restrictive and return a blank dataframe

    sample_params = {
        "limit": 10,
        "seed_artists": None,
        "seed_genres": seed_genres,
        "seed_tracks": None,
        "market": None,
        "target_acousticness": 0.8,
        "target_duration_ms": 200000,
        "target_instrumentalness": 0.5,
        "target_key": 5,
        "target_liveness": 0.3,
        "target_loudness": -15,
        "target_mode": 1,
        "target_popularity": 0,
        "target_speechiness": 0.1,
        "target_tempo": 120,
        "target_time_signature": 4,
        "target_valence": 0.5,
        "max_popularity": 50
    }

    msd_plot = wrapper.plot_msd()

    # Pass the seed artists, genres, tracks, and targets into the recommendations function
    recommendations_df = wrapper.get_spotify_recommendations(**sample_params)
    print(f'recommendations_df = {recommendations_df.head()}')
    print(f'seed_genres = {seed_genres}')

    # Plot track data
    features, parallel_cords, features_merged, parallel_cords_merged  = wrapper.plot_song_data(tracks_df, recommendations_df)
    # recommended_songs = wrapper.plot_recommended_songs(recommendations_df)

    ## Then pass your processed data to the frontend via "context" below
    context = {
        ## Put data here that you want to pass to the frontend in key-value pair/dictionary form:
        ## 'key':variable,

        'tracks': tracks_df.to_html(),
        'filtered_recommendations': recommendations_df.to_html(),
        'msd_plot': msd_plot,
        'features': features,
        'parallel_cords': parallel_cords,
        'features_merged': features_merged,
        'parallel_cords_merged': parallel_cords_merged
    }
    
    return render(request, 'dumpster_diver/index.html', context)
