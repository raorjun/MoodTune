// src/services/api.js

const API_BASE_URL = 'http://localhost:5000';

export const generatePlaylist = async (moodParams, platform) => {

  const normalizedParams = {
    target_valence: moodParams.valence / 100,
    target_energy: moodParams.energy / 100,
    activity: moodParams.activity,
    environment: moodParams.environment,
    amount: moodParams.songCount,
    seed_platform: platform,
    // You'll need to implement getting these from your auth flow
    seed_playlist_id: 'placeholder_id', 
    playlist_name: `${moodParams.activity || 'Mood'} Playlist`
  };

  try {
    const response = await fetch(`${API_BASE_URL}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams(normalizedParams),
    });

    if (!response.ok) {
      throw new Error('Failed to generate playlist');
    }

    const data = await response.json();
    return data.url;
  } catch (error) {
    console.error('Error generating playlist:', error);
    throw error;
  }
};

export const convertPlaylist = async (sourceUrl, targetPlatform) => {
  try {
    const response = await fetch(`${API_BASE_URL}/convert`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        source_url: sourceUrl,
        target_platform: targetPlatform,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to convert playlist');
    }

    const data = await response.json();
    return data.url;
  } catch (error) {
    console.error('Error converting playlist:', error);
    throw error;
  }
};