/*
COMP90024 Team 1
Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au
*/

import React from 'react';
import {
    Box, Flex, Image, Text, Spacer,
} from '@chakra-ui/react';
import { FaGithub, FaTwitter } from 'react-icons/fa';
import { EmailIcon } from '@chakra-ui/icons';

const StudentProfile = ({
    name, studentId, githubName, twitterName, email, jobDescription, imageSource,
}) => (
    <Box maxW="sm" p={4} borderWidth="1px" borderRadius="lg" overflow="hidden">
        <Flex justifyContent="center" alignItems="flex-start">
            <Image src={imageSource} alt={name} borderRadius="full" boxSize="100px" />
            <Box marginLeft={4}>
                <Text>{`${name} (${studentId})`}</Text>
                <Flex>
                    <FaGithub />
                    <FaTwitter />
                    <EmailIcon />
                </Flex>
                <Text fontSize="sm">{jobDescription}</Text>
            </Box>
        </Flex>
    </Box>
);

export default StudentProfile;
