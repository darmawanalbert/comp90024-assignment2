/*
COMP90024 Team 1
Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au
*/

import React, { useRef, useState, useEffect } from 'react';
import { useColorMode } from '@chakra-ui/react';
import mapboxgl from 'mapbox-gl/dist/mapbox-gl';
import { MAPBOX_PUBLIC_KEY } from '../utils/config';
import './Mapbox.module.css';

mapboxgl.accessToken = MAPBOX_PUBLIC_KEY;

const mapContainerStyle = {
    height: 'calc(100vh - 80px)',
    width: '100vw',
};

const Mapbox = () => {
    const { colorMode, toggleColorMode } = useColorMode();
    const mapContainer = useRef();
    const [lng, setLng] = useState(144.96378101783327);
    const [lat, setLat] = useState(-37.81307396157611);
    const [zoom, setZoom] = useState(9);

    useEffect(() => {
        const map = new mapboxgl.Map({
            container: mapContainer.current,
            style: colorMode === 'light' ? 'mapbox://styles/mapbox/light-v10' : 'mapbox://styles/mapbox/dark-v10',
            center: [lng, lat],
            zoom,
        });
        return () => map.remove();
    }, []);

    return (
        <div>
            <div className="map-container" ref={mapContainer} style={mapContainerStyle} />
        </div>
    );
};

export default Mapbox;
