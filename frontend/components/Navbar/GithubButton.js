/*
COMP90024 Team 1
Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au
*/

import React from 'react';
import {
    Box, Text, LinkBox, LinkOverlay, Flex,
} from '@chakra-ui/react';
import NextLink from 'next/link';
import { FaGithub } from 'react-icons/fa';

import { GITHUB_REPO_URL } from '../../utils/config';

const GithubButton = () => (
    <LinkBox>
        <Box
            lineHeight="1.2"
            transition="all 0.2s cubic-bezier(.08,.52,.52,1)"
            border="1px"
            px="8px"
            py="4px"
            borderRadius="4px"
            fontSize="14px"
            fontWeight="semibold"
            bg="#f5f6f7"
            borderColor="#ccd0d5"
            color="#4b4f56"
            m="4px"
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
            <Flex>
                <FaGithub />
                <Text px="4px">
                    <NextLink href={GITHUB_REPO_URL} passHref>
                        <LinkOverlay isExternal>
                            GitHub
                        </LinkOverlay>
                    </NextLink>
                </Text>
            </Flex>
        </Box>
    </LinkBox>
);

export default GithubButton;
