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
    Spinner,
} from '@chakra-ui/react';
import mapboxgl from 'mapbox-gl/dist/mapbox-gl';
import { MAPBOX_PUBLIC_KEY } from '../utils/config';
import { useMapInfo, useLdaScores } from '../utils/fetcher';

import WordCloud from './WordCloud';

import './Mapbox.module.css';

mapboxgl.accessToken = MAPBOX_PUBLIC_KEY;

const mapContainerStyle = {
    height: 'calc(100vh - 70px)',
    width: '100vw',
};

const Mapbox = ({ apiUrl }) => {
    const [isComponentMounted, setIsComponentMounted] = useState(false);
    const mapContainer = useRef();
    const [lng, setLng] = useState(144.9637);
    const [lat, setLat] = useState(-37.8130);
    const [zoom, setZoom] = useState(7.60);
    const [Map, setMap] = useState();
    const [cityName, setCityName] = useState('Melbourne');

    const { mapInfo, isMapInfoLoading, isMapInfoError } = useMapInfo(apiUrl);
    const { ldaScores, isLdaScoresLoading, isLdaScoresError } = useLdaScores(apiUrl);

    useEffect(() => {
        setIsComponentMounted(true);
        const map = new mapboxgl.Map({
            container: mapContainer.current,
            style: 'mapbox://styles/mapbox/outdoors-v11',
            center: [lng, lat],
            zoom,
            pitch: 45,
            maxBounds: [
                [96.8168, -43.7405], // Southwest coordinates
                [159.1092, -9.1422], // Northeast coordinates
            ],
        });

        map.on('click', 'cities', (e) => {
            setCityName(e.features[0].properties.UCL_NAME_2016);
        });

        map.on('mouseenter', 'cities', () => {
            map.getCanvas().style.cursor = 'pointer';
        });

        map.on('mouseleave', 'cities', () => {
            map.getCanvas().style.cursor = '';
        });

        map.on('move', () => {
            setLng(map.getCenter().lng.toFixed(4));
            setLat(map.getCenter().lat.toFixed(4));
            setZoom(map.getZoom().toFixed(2));
        });
        setMap(map);
    }, []);

    useEffect(() => {
        if (isComponentMounted && mapInfo) {
            Map.on('load', () => {
                Map.addSource('cities', {
                    type: 'geojson',
                    data: mapInfo,
                });

                Map.addLayer({
                    id: 'cities',
                    type: 'fill',
                    source: 'cities',
                    layout: {},
                    paint: {
                        'fill-color': '#0080ff',
                        'fill-opacity': 0.5,
                    },
                });

                Map.addLayer({
                    id: 'city-outlines',
                    type: 'line',
                    source: 'cities',
                    layout: {},
                    paint: {
                        'line-color': '#000000',
                        'line-width': 3,
                    },
                });
            });
        }
    }, [isComponentMounted, setMap, mapInfo, Map]);

    const generateLdaKeywords = (ldaParam, index) => {
        const ldaObject = ldaParam[index].value.lda_keywords;
        return Object.keys(ldaObject).map(
            (keyword, i) => ({ text: keyword, value: ldaObject[keyword] }),
        );
    };

    const getTopicScore = (ldaParam, topicLabel) => (
        ldaParam[cityIndex].value.topic_score[topicLabel]
    );

    const today = new Date();
    const day = today.getDate();
    const month = today.toLocaleString('default', { month: 'long' });
    const year = today.getFullYear();

    const [cityIndex, setCityIndex] = useState(0);

    return (
        <Flex>
            <div className="map-container" ref={mapContainer} style={mapContainerStyle} />
            <Box w={1 / 3} p={4} borderRight="1px" borderRightColor="gray.200" overflowY="scroll" height="93vh">
                <Text fontSize="xl" fontWeight="semibold">{`Selected City: ${cityName}`}</Text>
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
                {isLdaScoresError && <Text>Error loading data</Text>}
                {isLdaScoresLoading && <Spinner color="teal.400" />}
                {/* {ldaScores
                    && (
                        <Table variant="simple">
                            <TableCaption>{`Last updated: ${day} ${month} ${year}`}</TableCaption>
                            <Thead>
                                <Tr>
                                    <Th>No</Th>
                                    <Th>Topic Name</Th>
                                    <Th isNumeric>Scores</Th>
                                </Tr>
                            </Thead>
                            <Tbody>
                                <Tr>
                                    <Td>1</Td>
                                    <Td>Business</Td>
                                    <Td isNumeric>
                                        {getTopicScore(ldaScore, 'business')}
                                    </Td>
                                </Tr>
                                <Tr>
                                    <Td>2</Td>
                                    <Td>Education</Td>
                                    <Td isNumeric>
                                        {getTopicScore(ldaScore, 'education')}
                                    </Td>
                                </Tr>
                                <Tr>
                                    <Td>3</Td>
                                    <Td>Entertainment</Td>
                                    <Td isNumeric>
                                        {getTopicScore(ldaScore, 'entertainment')}
                                    </Td>
                                </Tr>
                                <Tr>
                                    <Td>4</Td>
                                    <Td>Places</Td>
                                    <Td isNumeric>
                                        {getTopicScore(ldaScore, 'places')}
                                    </Td>
                                </Tr>
                                <Tr>
                                    <Td>5</Td>
                                    <Td>Politics</Td>
                                    <Td isNumeric>
                                        {getTopicScore(ldaScore, 'politics')}
                                    </Td>
                                </Tr>
                                <Tr>
                                    <Td>6</Td>
                                    <Td>Sport</Td>
                                    <Td isNumeric>
                                        {getTopicScore(ldaScore, 'sport')}
                                    </Td>
                                </Tr>
                            </Tbody>
                            <Tfoot>
                                <Tr>
                                    <Th colSpan={2}>Total</Th>
                                    <Th isNumeric>172</Th>
                                </Tr>
                            </Tfoot>
                        </Table>
                    )} */}
                <Text fontSize="xl" fontWeight="semibold">Topic Keywords</Text>
                <Box marginBottom={4}>
                    {isLdaScoresError && <Text>Error loading data</Text>}
                    {isLdaScoresLoading && <Spinner color="teal.400" />}
                    {/* {ldaScores
                        && <WordCloud data={generateLdaKeywords(ldaScores, cityIndex)} />} */}
                </Box>
            </Box>
        </Flex>
    );
};

export default Mapbox;
