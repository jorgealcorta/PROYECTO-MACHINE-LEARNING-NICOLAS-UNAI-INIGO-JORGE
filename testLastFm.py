import pylast

API_KEY = "6cb74a0510cbdc0e12fc2dc141d4c692"  # this is a sample key
API_SECRET = "0e89a0f79e7bb1164c075d5235a510bd"

username = "MLTest007"
password_hash = pylast.md5("q3tGZUkHt83We@8")

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=password_hash,
)

track = network.get_track("Taylor Swift", "Anti-Hero")



print(track.get_playcount())
print(track.get_listener_count())