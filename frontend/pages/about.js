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

import { Navbar, StudentProfile } from '../components/index';

export default function About() {
    return (
        <div>
            <Head>
                <title>COMP90024 - About</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <main>
                <Navbar />
                <Container>
                    <Heading>Team Members</Heading>
                    <StudentProfile
                        name="Albert Darmawan"
                        studentId="1168452"
                        githubName="darmawanalbert"
                        twitterName="darmawan2502"
                        email="darmawana@student.unimelb.edu.au"
                        jobDescription="Web Application"
                        imageSource="/albert-darmawan.jpeg"
                    />
                    <Heading>Acknowledgements</Heading>
                </Container>
            </main>
        </div>
    );
}
