import React, { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';

import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

const MapUpdater = ({ center, zoom }) => {
  const map = useMap();

  useEffect(() => {
    const updateMap = () => {
      map.invalidateSize();
      map.flyTo(center, zoom);
    };

    updateMap();

    window.addEventListener('resize', updateMap);
    return () => window.removeEventListener('resize', updateMap);
  }, [map, center, zoom]);

  return null;
};

const UpdateCenter = ({ center, zoom }) => {
  const map = useMap();
  useEffect(() => {
    if (center) {
      map.flyTo(center, zoom);
    }
  }, [center, zoom, map]);

  return null;
};


delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const MapComponent = ({ searchResults, center, zoom }) => {
  return (
    <MapContainer center={center} zoom={zoom} style={{ height: '100%', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {searchResults.map((result, idx) => (
        <Marker key={idx} position={[result.latitude, result.longitude]}>
          <Popup>{result.name}<br /></Popup>
        </Marker>
      ))}
      <UpdateCenter center={center} zoom={zoom}/>
      <MapUpdater center={center} zoom={zoom}/> {}
    </MapContainer>
  );
};
export default MapComponent;
