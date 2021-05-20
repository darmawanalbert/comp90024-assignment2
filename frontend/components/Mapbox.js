/*
COMP90024 Team 1
Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au
*/

// Inspired from: https://dev.to/naomigrace/how-to-integrate-mapbox-gl-js-in-your-next-js-project-without-react-map-gl-or-a-react-wrapper-library-50f#2-adding-a-map

import React, { useRef, useState, useEffect } from 'react';
import {
    Box, Flex, Text, Stat, StatLabel, StatNumber, StatGroup,
    Table, TableCaption, Thead, Tbody, Th, Td, Tr, Tfoot,
} from '@chakra-ui/react';
import mapboxgl from 'mapbox-gl/dist/mapbox-gl';
import { MAPBOX_PUBLIC_KEY } from '../utils/config';
import { addDataLayer, initialiseMap } from '../utils/mapboxUtil';

import './Mapbox.module.css';

mapboxgl.accessToken = MAPBOX_PUBLIC_KEY;

const mapContainerStyle = {
    height: 'calc(100vh - 70px)',
    width: '100vw',
};

const Mapbox = () => {
    const [isComponentMounted, setIsComponentMounted] = useState(false);
    const mapContainer = useRef();
    const [lng, setLng] = useState(144.9637);
    const [lat, setLat] = useState(-37.8130);
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
        <Flex>
            <div className="map-container" ref={mapContainer} style={mapContainerStyle} />
            <Box w={1 / 3} p={4} borderRight="1px" borderRightColor="gray.200" overflowY="scroll" height="93vh">
                <Text fontSize="xl" fontWeight="semibold">Info</Text>
                <StatGroup p={4} borderWidth="1px" borderRadius="lg" overflow="hidden" justifyContent="center">
                    <Stat>
                        <StatLabel>Longitude</StatLabel>
                        <StatNumber>{lng}</StatNumber>
                    </Stat>
                    <Stat>
                        <StatLabel>Latitude</StatLabel>
                        <StatNumber>{lat}</StatNumber>
                    </Stat>
                    <Stat>
                        <StatLabel>Zoom</StatLabel>
                        <StatNumber>{zoom}</StatNumber>
                    </Stat>
                </StatGroup>
                <br />
                <Text fontSize="xl" fontWeight="semibold">Topics</Text>
                <Table variant="simple">
                    <TableCaption>Last updated: April 2021</TableCaption>
                    <Thead>
                        <Tr>
                            <Th>No</Th>
                            <Th>Topic Name</Th>
                            <Th isNumeric>#Tweets</Th>
                        </Tr>
                    </Thead>
                    <Tbody>
                        <Tr>
                            <Td>1</Td>
                            <Td>Business</Td>
                            <Td isNumeric>104</Td>
                        </Tr>
                        <Tr>
                            <Td>2</Td>
                            <Td>Politics</Td>
                            <Td isNumeric>58</Td>
                        </Tr>
                        <Tr>
                            <Td>3</Td>
                            <Td>Entertainment</Td>
                            <Td isNumeric>10</Td>
                        </Tr>
                    </Tbody>
                    <Tfoot>
                        <Tr>
                            <Th colSpan={2}>Total</Th>
                            <Th isNumeric>172</Th>
                        </Tr>
                    </Tfoot>
                </Table>
            </Box>
        </Flex>
    );
};

export default Mapbox;
