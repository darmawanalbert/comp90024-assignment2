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
import api from '../axiosConfig'; // Use axios configuration as specified in axiosConfig.js

export default function Home() {
    // Get geojson for the map
    async function getCities() {
        const res = await api.get('/cities');

        console.log(res.data);
    }

    async function getMedianIncome() {
        const res = await api.get('/median_income', { params: { id: '101001' } });

        console.log(res.data);
    }

    async function getMedianIncomes() {
        const res = await api.get('/median_income/all')

        console.log(res.data)
    }

    async function getAge() {
        const res = await api.get('/age_25_34', { params: { id: '101001' } });

        console.log(res.data);
    }

    async function getAges() {
        const res = await api.get('/age_25_34/all')

        console.log(res.data)
    }

    async function getUnemployment() {
        const res = await api.get('/unemployment_rate', { params: { id: '101001' } });

        console.log(res.data);
    }

    async function getUnemployments() {
        const res = await api.get('/unemployment_rate/all')

        console.log(res.data)
    }



    // getCities();
    // getCharts();
    // getChart();
    // getMedianIncome();
    // getMedianIncomes();
    // getAge();
    // getAges();
    getUnemployment();
    getUnemployments();

    // APIs for later use
    // // Get data for all available charts
    // async function getCharts() {
    //     const res = await api.get('/charts/all');

    //     console.log(res.data);
    // }

    // // Get data for a single chart
    // async function getChart() {
    //     const res = await api.get('/charts', { params: { id: 'data2' } });

    //     console.log(res.data);
    // }

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
