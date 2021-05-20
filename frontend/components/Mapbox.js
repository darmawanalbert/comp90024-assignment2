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

import WordCloud from './WordCloud';

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

    const ldaResults = [
        { text: 'day', value: 0.01589293 },
        { text: 'photo', value: 0.00922306 },
        { text: 'posted', value: 0.00845825 },
        { text: 'australia', value: 0.00576136 },
        { text: 'one', value: 0.00516197 },
        { text: 'victoria', value: 0.00382048 },
        { text: 'love', value: 0.00351002 },
        { text: 'mother', value: 0.01062788 },
        { text: 'happy', value: 0.00915481 },
        { text: 'would', value: 0.00297083 },
        { text: 'lisapresley', value: 0.00585826 },
        { text: 'year', value: 0.00502370 },
        { text: 'make', value: 0.00365274 },
        { text: 'know', value: 0.00412439 },
        { text: 'holy', value: 0.00328865 },
        { text: 'mainsundayservice', value: 0.00310556 },
        { text: 'see', value: 0.00309822 },
        { text: 'god', value: 0.00299292 },
        { text: 'like', value: 0.00850314 },
        { text: 'melbourne', value: 0.00699135 },
        { text: 'mum', value: 0.00557472 },
        { text: 'today', value: 0.00500120 },
        { text: 'naomirwolf', value: 0.00431268 },
        { text: 'good', value: 0.00871694 },
        { text: 'go', value: 0.00596997 },
        { text: 'time', value: 0.00358518 },
        { text: 'night', value: 0.00434714 },
        { text: 'people', value: 0.00411526 },
        { text: 'u', value: 0.00380271 },
        { text: 'game', value: 0.00363156 },
        { text: 'get', value: 0.00519592 },
        { text: 'need', value: 0.00483581 },
        { text: 'team', value: 0.00407634 },
        { text: 'thank', value: 0.00403449 },
        { text: 'back', value: 0.00351706 },
    ];

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
                <Text fontSize="xl" fontWeight="semibold">Topic Scores</Text>
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
                <Text fontSize="xl" fontWeight="semibold">Topic Keywords</Text>
                <Box marginBottom={4}>
                    <WordCloud data={ldaResults} />
                </Box>
            </Box>
        </Flex>
    );
};

export default Mapbox;
