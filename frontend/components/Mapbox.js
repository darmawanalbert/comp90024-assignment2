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
import './Mapbox.module.css';

mapboxgl.accessToken = MAPBOX_PUBLIC_KEY;

const Mapbox = () => {
    const mapContainer = useRef();
    const [lng, setLng] = useState(-70.9);
    const [lat, setLat] = useState(42.35);
    const [zoom, setZoom] = useState(9);

    useEffect(() => {
        const map = new mapboxgl.Map({
            container: mapContainer.current,
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [lng, lat],
            zoom,
        });
        return () => map.remove();
    }, []);

    return (
        <div>
            <div className="map-container" ref={mapContainer} style={{ height: 500, width: 500 }} />
        </div>
    );
};

export default Mapbox;
