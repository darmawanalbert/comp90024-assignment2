/*
COMP90024 Team 1
Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au
*/

import React from 'react';
import Head from 'next/head';
import api from '../axiosConfig'; // Use axios configuration as specified in axiosConfig.js

export default function Home() {
    // Get geojson for the map
    async function getCities() {
        const res = await api.get('/cities');

        console.log(res.data);
    }

    // Get data for all available charts
    async function getCharts() {
        const res = await api.get('/charts/all');

        console.log(res.data);
    }

    // Get data for a single chart
    async function getChart() {
        const res = await api.get('/charts', { params: { id: 'data2' } });

        console.log(res.data);
    }

    getCities();
    getCharts();
    getChart();

    return (
        <div>
            <Head>
                <title>COMP90024 - Home</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <main>
                <h1>
                    Test page for API
                </h1>
            </main>
        </div>
    );
}
