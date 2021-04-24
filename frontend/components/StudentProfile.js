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
    Box, Flex, Image, Text, LinkBox, LinkOverlay,
} from '@chakra-ui/react';
import { FaGithub, FaTwitter, FaEnvelope } from 'react-icons/fa';

const StudentProfile = ({
    name, studentId, githubName, twitterName, email, jobDescription, imageSource,
}) => (
    <Box maxW="xs" p={4} borderWidth="1px" borderRadius="lg" overflow="hidden">
        <Flex justifyContent="center" alignItems="flex-start">
            <Image src={imageSource || '/avatar.png'} alt={name} borderRadius="full" boxSize="100px" />
            <Box marginLeft={4}>
                <Text>{`${name} (${studentId})`}</Text>
                <Flex alignItems="center">
                    {githubName
                        ? (
                            <LinkBox>
                                <Box
                                    mr={2}
                                    _hover={{ bg: '#ebedf0' }}
                                    _active={{
                                        bg: '#dddfe2',
                                        transform: 'scale(0.98)',
                                        borderColor: '#bec3c9',
                                    }}
                                    _focus={{
                                        boxShadow: '0 0 1px 2px rgba(88, 144, 255, .75), 0 1px 1px rgba(0, 0, 0, .15)',
                                    }}
                                >
                                    <LinkOverlay href={`https://github.com/${githubName}`} isExternal>
                                        <FaGithub />
                                    </LinkOverlay>
                                </Box>
                            </LinkBox>
                        ) : null}
                    {twitterName
                        ? (
                            <LinkBox>
                                <Box
                                    mr={2}
                                    _hover={{ bg: '#ebedf0' }}
                                    _active={{
                                        bg: '#dddfe2',
                                        transform: 'scale(0.98)',
                                        borderColor: '#bec3c9',
                                    }}
                                    _focus={{
                                        boxShadow: '0 0 1px 2px rgba(88, 144, 255, .75), 0 1px 1px rgba(0, 0, 0, .15)',
                                    }}
                                >
                                    <LinkOverlay href={`https://twitter.com/${twitterName}`} isExternal>
                                        <FaTwitter />
                                    </LinkOverlay>
                                </Box>
                            </LinkBox>
                        ) : null}
                    <LinkBox>
                        <Box
                            _hover={{ bg: '#ebedf0' }}
                            _active={{
                                bg: '#dddfe2',
                                transform: 'scale(0.98)',
                                borderColor: '#bec3c9',
                            }}
                            _focus={{
                                boxShadow: '0 0 1px 2px rgba(88, 144, 255, .75), 0 1px 1px rgba(0, 0, 0, .15)',
                            }}
                        >
                            <LinkOverlay href={`mailto:${email}`} isExternal>
                                <FaEnvelope />
                            </LinkOverlay>
                        </Box>
                    </LinkBox>
                </Flex>
                <Text fontSize="sm">{jobDescription}</Text>
            </Box>
        </Flex>
    </Box>
);

export default StudentProfile;
