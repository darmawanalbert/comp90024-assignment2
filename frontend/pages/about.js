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
import {
    Heading, Container, Text, Link, Center, Wrap, WrapItem,
} from '@chakra-ui/react';

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
                <Container maxW="3xl">
                    <Center margin={8}>
                        <Heading>Team Members</Heading>
                    </Center>
                    <Wrap>
                        <WrapItem>
                            <StudentProfile
                                name="Albert Darmawan"
                                studentId="1168452"
                                githubName="darmawanalbert"
                                twitterName="darmawan2502"
                                email="darmawana@student.unimelb.edu.au"
                                jobDescription="Web Application"
                                imageSource="/albert-darmawan.jpeg"
                            />
                        </WrapItem>
                        <WrapItem>
                            <StudentProfile
                                name="Clarisca Lawrencia"
                                studentId="1152594"
                                githubName="clawrencia"
                                email="clawrencia@student.unimelb.edu.au"
                                jobDescription="Data Harvesting, Machine Learning model"
                            />
                        </WrapItem>
                        <WrapItem>
                            <StudentProfile
                                name="I Gede Wibawa Cakramurti"
                                studentId="1047538"
                                githubName="cakraocha"
                                email="icakramurti@student.unimelb.edu.au"
                                jobDescription="Data Storage, CouchDB Clusters"
                            />
                        </WrapItem>
                        <WrapItem>
                            <StudentProfile
                                name="Nuvi Anggaresti"
                                studentId="830683"
                                githubName="nuvianggaresti"
                                email="nanggaresti@student.unimelb.edu.au"
                                jobDescription="Web Services, Analytics"
                            />
                        </WrapItem>
                        <WrapItem>
                            <StudentProfile
                                name="Wildan Anugrah Putra"
                                studentId="1191132"
                                githubName="wildananugra"
                                email="wildananugra@student.unimelb.edu.au"
                                jobDescription="Orchestration, Ansible"
                            />
                        </WrapItem>
                    </Wrap>
                    <Center margin={8}>
                        <Heading>Acknowledgements</Heading>
                    </Center>
                    <Text spacing={4}>
                        This project is for academic purpose only. We respect your data privacy and
                        will only display aggregated or anonymous information.
                    </Text>
                    <br />
                    <Text>
                        All the Twitter data stored in the system is publicly accessible from
                        {' '}
                        <Link color="teal.500" href="https://developer.twitter.com/en/docs/twitter-api/v1" isExternal>
                            Standard Twitter API
                        </Link>
                        .
                    </Text>
                    <br />
                    <Text>
                        This project was supported by use of the
                        {' '}
                        <Link color="teal.500" href="https://docs.cloud.unimelb.edu.au/" isExternal>
                            Melbourne Research Cloud
                        </Link>
                        , a free on-demand computing resources to researchers at the
                        University of Melbourne, managed by
                        {' '}
                        <Link color="teal.500" href="https://research.unimelb.edu.au/infrastructure/research-computing-services" isExternal>
                            Research Computing Services
                        </Link>
                        .
                    </Text>
                    <br />
                    <br />
                </Container>
            </main>
        </div>
    );
}
