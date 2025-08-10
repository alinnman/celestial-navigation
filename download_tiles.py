''' Dowload used map tiles.
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)

'''
import os
import time
import requests

# Alternative tile sources
# pylint: disable=C0301
tile_sources = {
    'stamen_terrain': 'https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png',
    'cartodb_positron': 'https://cartodb-basemaps.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png',
    'opentopomap': 'https://tile.opentopomap.org/{z}/{x}/{y}.png',
    'esri_world': 
    'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
    'usgs':'https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}'
}
# pylint: enable=C0301

CHOSEN_TILES = 'usgs'
# NOTE: The USGS data is *public domain* and can be freely used.
# You are strongly advised to check legal requirements before using *any*
# other map data source for the Celeste app.

def download_world_tiles(max_zoom=2,
                         base_url=tile_sources[CHOSEN_TILES],
                         output_dir="tiles"):
    """Download world tiles up to specified zoom level"""

    total_size = 0
    tile_count = 0

    for zoom in range(0, max_zoom + 1):
        max_tiles = 2 ** zoom  # Number of tiles per dimension

        for x in range(max_tiles):
            for y in range(max_tiles):
                tile_url = base_url.format(z=zoom, x=x, y=y)
                tile_path = f"{output_dir}/{zoom}/{x}/{y}.png"

                os.makedirs(os.path.dirname(tile_path), exist_ok=True)

                try:
                    response = requests.get(tile_url, timeout=1)
                    if response.status_code == 200:
                        with open(tile_path, 'wb') as f:
                            f.write(response.content)

                        file_size = len(response.content)
                        total_size += file_size
                        tile_count += 1

                        print(f"Downloaded {zoom}/{x}/{y}.png ({file_size} bytes)")

                        if total_size > 1024 * 1024:  # 1MB limit
                            print(f"Reached 1MB limit with {tile_count} tiles")
                            return

                    time.sleep(0.5)  # Be respectful
# pylint: disable=W0718
                except Exception as e:
                    print(f"Error downloading {zoom}/{x}/{y}: {e}")
# pylint: enable=W0718

    print(f"Downloaded {tile_count} tiles, total size: {total_size/1024:.1f}KB")

# Usage
download_world_tiles(max_zoom=2)
