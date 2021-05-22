/*
COMP90024 Team 1
Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au
*/

// Inspired from: https://raptis.wtf/blog/create-a-navbar-with-chakra-ui-react/

import React from 'react';
import {
    Box, Text, LinkBox, LinkOverlay,
} from '@chakra-ui/react';
import NextLink from 'next/link';

const Logo = (props) => (
    <LinkBox>
        <Box {...props}>
            <Text fontSize="lg" fontWeight="bold">
                <NextLink href="/" passHref>
                    <LinkOverlay>
                        Twitter Topic Analysis
                    </LinkOverlay>
                </NextLink>
            </Text>
        </Box>
    </LinkBox>
);

export default Logo;
