/*
COMP90024 Team 1
Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au
*/

import React from 'react';
import Head from 'next/head';
import {
    Heading, Container, Center, Text, Spinner,
} from '@chakra-ui/react';
import { Scatter } from 'react-chartjs-2';

import { Navbar } from '../components/index';
import { useChartInfo } from '../utils/fetcher';

export default function Analysis({ apiUrl }) {
    const { chartInfo, isChartInfoLoading, isChartInfoError } = useChartInfo(apiUrl);

    const chartOptions = {
        scales: {
            yAxes: [
                {
                    ticks: {
                        beginAtZero: true,
                    },
                },
            ],
        },
    };

    const xScales = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0];

    const generateData = (info, typeIndex) => (
        {
            labels: xScales,
            datasets: [
                {
                    type: 'scatter',
                    label: 'Business',
                    data: info[typeIndex].value.business.x.map(
                        (xValue, i) => ({ x: xValue, y: info[typeIndex].value.business.y[i] }),
                    ),
                    backgroundColor: '#E53E3E',
                    hidden: false,
                },
                {
                    type: 'line',
                    label: 'Business Regression',
                    data: xScales.map(
                        (xValue, i) => (
                            info[typeIndex].value.business.m * xValue
                                + info[typeIndex].value.business.c),
                    ),
                    pointRadius: 0,
                    borderColor: '#E53E3E',
                    borderWidth: 2,
                    hidden: false,
                },
                {
                    type: 'scatter',
                    label: 'Education',
                    data: info[typeIndex].value.education.x.map(
                        (xValue, i) => ({ x: xValue, y: info[typeIndex].value.education.y[i] }),
                    ),
                    backgroundColor: '#DD6B20',
                    hidden: true,
                },
                {
                    type: 'line',
                    label: 'Education Regression',
                    data: xScales.map(
                        (xValue, i) => (
                            info[typeIndex].value.education.m * xValue
                                + info[typeIndex].value.education.c),
                    ),
                    pointRadius: 0,
                    borderColor: '#DD6B20',
                    borderWidth: 2,
                    hidden: true,
                },
                {
                    type: 'scatter',
                    label: 'Entertainment',
                    data: info[typeIndex].value.entertainment.x.map(
                        (xValue, i) => ({ x: xValue, y: info[typeIndex].value.entertainment.y[i] }),
                    ),
                    backgroundColor: '#38A169',
                    hidden: true,
                },
                {
                    type: 'line',
                    label: 'Entertainment Regression',
                    data: xScales.map(
                        (xValue, i) => (
                            info[typeIndex].value.entertainment.m * xValue
                                + info[typeIndex].value.entertainment.c),
                    ),
                    pointRadius: 0,
                    borderColor: '#38A169',
                    borderWidth: 2,
                    hidden: true,
                },
                {
                    type: 'scatter',
                    label: 'Places',
                    data: info[typeIndex].value.places.x.map(
                        (xValue, i) => ({ x: xValue, y: info[typeIndex].value.places.y[i] }),
                    ),
                    backgroundColor: '#3182CE',
                    hidden: true,
                },
                {
                    type: 'line',
                    label: 'Places Regression',
                    data: xScales.map(
                        (xValue, i) => (
                            info[typeIndex].value.places.m * xValue
                                + info[typeIndex].value.places.c),
                    ),
                    pointRadius: 0,
                    borderColor: '#3182CE',
                    borderWidth: 2,
                    hidden: true,
                },
                {
                    type: 'scatter',
                    label: 'Politics',
                    data: info[typeIndex].value.politics.x.map(
                        (xValue, i) => ({ x: xValue, y: info[typeIndex].value.politics.y[i] }),
                    ),
                    backgroundColor: '#805AD5',
                    hidden: true,
                },
                {
                    type: 'line',
                    label: 'Politics Regression',
                    data: xScales.map(
                        (xValue, i) => (
                            info[typeIndex].value.politics.m * xValue
                                + info[typeIndex].value.politics.c),
                    ),
                    pointRadius: 0,
                    borderColor: '#805AD5',
                    borderWidth: 2,
                    hidden: true,
                },
                {
                    type: 'scatter',
                    label: 'Sport',
                    data: info[typeIndex].value.sport.x.map(
                        (xValue, i) => ({ x: xValue, y: info[typeIndex].value.sport.y[i] }),
                    ),
                    backgroundColor: '#D53F8C',
                    hidden: true,
                },
                {
                    type: 'line',
                    label: 'Sport Regression',
                    data: xScales.map(
                        (xValue, i) => (
                            info[typeIndex].value.sport.m * xValue
                                + info[typeIndex].value.sport.c),
                    ),
                    pointRadius: 0,
                    borderColor: '#D53F8C',
                    borderWidth: 2,
                    hidden: true,
                },
            ],
        }
    );

    const today = new Date();
    const month = today.toLocaleString('default', { month: 'long' });
    const year = today.getFullYear();

    return (
        <div>
            <Head>
                <title>COMP90024 - Analysis</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <main>
                <Navbar />
                <Container maxW="3xl" paddingBottom={8}>
                    <Center margin={8} marginBottom={0}>
                        <Heading>Analysis with AURIN</Heading>
                    </Center>
                    <Center>
                        <Text color="gray.500">{`Last updated: ${month} ${year}`}</Text>
                    </Center>
                    <Center margin={8}>
                        <Text fontSize="xl" fontWeight="semibold">#1: Correlation between Median Income and Topic Scores</Text>
                    </Center>
                    <Center>
                        {isChartInfoError && <Text>Error loading data</Text>}
                        {isChartInfoLoading && <Spinner color="teal.400" />}
                        {chartInfo
                            && <Scatter data={generateData(chartInfo, 0)} options={chartOptions} />}
                    </Center>
                    <Center margin={8}>
                        <Text fontSize="xl" fontWeight="semibold">#2: Correlation between Unemployment Rate and Topic Scores</Text>
                    </Center>
                    <Center>
                        {isChartInfoError && <Text>Error loading data</Text>}
                        {isChartInfoLoading && <Spinner color="teal.400" />}
                        {chartInfo
                            && <Scatter data={generateData(chartInfo, 1)} options={chartOptions} />}
                    </Center>
                    <Center margin={8}>
                        <Text fontSize="xl" fontWeight="semibold">#3: Correlation between Population Percentage Age 25-34 and Topic Scores</Text>
                    </Center>
                    <Center>
                        {isChartInfoError && <Text>Error loading data</Text>}
                        {isChartInfoLoading && <Spinner color="teal.400" />}
                        {chartInfo
                            && <Scatter data={generateData(chartInfo, 2)} options={chartOptions} />}
                    </Center>
                </Container>
            </main>
        </div>
    );
}

export async function getStaticProps() {
    const apiUrl = process.env.API_URL;
    return {
        props: {
            apiUrl,
        },
    };
}
