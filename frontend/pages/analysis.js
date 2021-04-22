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
import { Heading, Container } from '@chakra-ui/react';

import { Navbar } from '../components/index';

export default function Analysis() {
    return (
        <div>
            <Head>
                <title>COMP90024 - Analysis</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <main>
                <Navbar />
                <Container>
                    <Heading>Analysis with AURIN</Heading>
                </Container>
            </main>
        </div>
    );
}
