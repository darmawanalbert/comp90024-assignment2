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
import { Heading, Container, Center } from '@chakra-ui/react';
import { Line } from 'react-chartjs-2';

import { Navbar, TwitterCard } from '../components/index';
import { useMapInfo } from '../utils/fetcher';

export default function Analysis({ apiUrl }) {
    const data = {
        labels: ['1', '2', '3', '4', '5', '6'],
        datasets: [
            {
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                fill: false,
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgba(255, 99, 132, 0.2)',
            },
        ],
    };

    const options = {
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

    const { mapInfo, isMapInfoLoading, isMapInfoError } = useMapInfo(apiUrl);
    alert(JSON.stringify(mapInfo));

    return (
        <div>
            <Head>
                <title>COMP90024 - Analysis</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <main>
                <Navbar />
                <Container maxW="3xl">
                    <Center margin={8}>
                        <Heading>Analysis with AURIN</Heading>
                    </Center>
                    <Line data={data} options={options} />
                    <TwitterCard
                        displayName="Albert Darmawan"
                        username="darmawan2502"
                        tweet="Wow this is awesome!"
                        time="10:50 PM"
                        date="Apr 23, 2021"
                    />
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
