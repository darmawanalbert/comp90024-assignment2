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
    height: 'calc(100vh - 100px)',
    width: '100vw',
};

const Mapbox = () => {
    const { colorMode, toggleColorMode } = useColorMode();
    const [isComponentMounted, setIsComponentMounted] = useState(false);
    const mapContainer = useRef();
    // const [lng, setLng] = useState(144.96378101783327);
    // const [lat, setLat] = useState(-37.81307396157611);
    const [lng, setLng] = useState(-77.02);
    const [lat, setLat] = useState(-38.887);
    const [zoom, setZoom] = useState(12.5);

    useEffect(() => {
        setIsComponentMounted(true);
        const map = new mapboxgl.Map({
            container: mapContainer.current,
            style: colorMode === 'light' ? 'mapbox://styles/mapbox/light-v10' : 'mapbox://styles/mapbox/dark-v10',
            center: [lng, lat],
            zoom,
            pitch: 45,
            // maxBounds: [
            //     [-77.875588, 38.50705], // Southwest coordinates
            //     [-76.15381, 39.548764], // Northeast coordinates
            // ],
        });

        map.on('load', () => {
            map.addSource('earthquakes', {
                type: 'geojson',
                data: 'https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson',
                cluster: true,
                clusterMaxZoom: 14,
                clusterRadius: 50,
            });

            map.addLayer({
                id: 'clusters',
                type: 'circle',
                source: 'earthquakes',
                filter: ['has', 'point_count'],
                paint: {
                    'circle-color': [
                        'step',
                        ['get', 'point_count'],
                        '#51bbd6',
                        100,
                        '#f1f075',
                        750,
                        '#f28cb1',
                    ],
                    'circle-radius': [
                        'step',
                        ['get', 'point_count'],
                        20,
                        100,
                        30,
                        750,
                        40,
                    ],
                },
            });

            map.addLayer({
                id: 'cluster-count',
                type: 'symbol',
                source: 'earthquakes',
                filter: ['has', 'point_count'],
                layout: {
                    'text-field': '{point_count_abbreviated}',
                    'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
                    'text-size': 12,
                },
            });

            map.addLayer({
                id: 'unclustered-point',
                type: 'circle',
                source: 'earthquakes',
                filter: ['!', ['has', 'point_count']],
                paint: {
                    'circle-color': '#11b4da',
                    'circle-radius': 4,
                    'circle-stroke-width': 1,
                    'circle-stroke-color': '#fff',
                },
            });

            map.on('click', 'clusters', (e) => {
                const features = map.queryRenderedFeatures(e.point, {
                    layers: ['clusters'],
                });
                const clusterId = features[0].properties.cluster_id;
                map.getSource('earthquakes').getClusterExpansionZoom(
                    clusterId,
                    (err, zoomVal) => {
                        if (err) return;
                        map.easeTo({
                            center: features[0].geometry.coordinates,
                            zoom: zoomVal,
                        });
                    },
                );
            });

            map.on('click', 'unclustered-point', (e) => {
                const coordinates = e.features[0].geometry.coordinates.slice();
                const { mag } = e.features[0].properties;
                let tsunami = 'no';
                if (e.features[0].properties.tsunami === 1) {
                    tsunami = 'yes';
                }

                while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                    coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
                }

                new mapboxgl.Popup()
                    .setLngLat(coordinates)
                    .setHTML(`magnitude: ${mag} <br>Was there a tsunami?: ${tsunami}`)
                    .addTo(map);
            });

            map.on('mouseenter', 'clusters', () => {
                map.getCanvas().style.cursor = 'pointer';
            });

            map.on('mouseleave', 'clusters', () => {
                map.getCanvas().style.cursor = '';
            });
        });

        map.on('move', () => {
            setLng(map.getCenter().lng.toFixed(4));
            setLat(map.getCenter().lat.toFixed(4));
            setZoom(map.getZoom().toFixed(2));
        });

        return () => map.remove();
    }, []);

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
