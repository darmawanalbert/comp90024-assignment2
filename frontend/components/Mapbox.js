/*
COMP90024 Team 1
Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au
*/

import React, { useRef, useState, useEffect } from 'react';
import mapboxgl from 'mapbox-gl/dist/mapbox-gl';
import { MAPBOX_PUBLIC_KEY } from '../utils/config';
import { addDataLayer, initialiseMap } from '../utils/mapboxUtil';
import './Mapbox.module.css';

mapboxgl.accessToken = MAPBOX_PUBLIC_KEY;

const mapContainerStyle = {
    height: 'calc(100vh - 100px)',
    width: '100vw',
};

const Mapbox = () => {
    const [isComponentMounted, setIsComponentMounted] = useState(false);
    const mapContainer = useRef();
    const [lng, setLng] = useState(144.96378101783327);
    const [lat, setLat] = useState(-37.81307396157611);
    // const [lng, setLng] = useState(-77.02);
    // const [lat, setLat] = useState(-38.887);
    const [zoom, setZoom] = useState(12.5);
    const [Map, setMap] = useState();
    const data = 'https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson';

    useEffect(() => {
        setIsComponentMounted(true);
        const map = new mapboxgl.Map({
            container: mapContainer.current,
            style: 'mapbox://styles/mapbox/outdoors-v11',
            center: [lng, lat],
            zoom,
            pitch: 45,
            // maxBounds: [
            //     [-77.875588, 38.50705], // Southwest coordinates
            //     [-76.15381, 39.548764], // Northeast coordinates
            // ],
        });

        initialiseMap(mapboxgl, map);
        map.on('move', () => {
            setLng(map.getCenter().lng.toFixed(4));
            setLat(map.getCenter().lat.toFixed(4));
            setZoom(map.getZoom().toFixed(2));
        });
        setMap(map);
    }, []);

    useEffect(() => {
        if (isComponentMounted && data) {
            Map.on('load', () => {
                addDataLayer(Map, data);
            });
        }
    }, [isComponentMounted, setMap, data, Map]);

    return (
        <div>
            <div className="sidebar">
                {`Longitude: ${lng} | Latitude: ${lat} | Zoom: ${zoom}`}
            </div>
            <div className="map-container" ref={mapContainer} style={mapContainerStyle} />
        </div>
    );
};

export default Mapbox;
