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
    Flex, Box, Heading, Spacer, IconButton, useColorMode,
} from '@chakra-ui/react';
import { MoonIcon, SunIcon } from '@chakra-ui/icons';

const Header = () => {
    const { colorMode, toggleColorMode } = useColorMode();
    return (
        <Flex boxShadow="base" align="center">
            <Box p={4}>
                <Heading>COMP90024 - Team 1</Heading>
            </Box>
            <Spacer />
            <Box p={4}>
                {colorMode === 'light'
                    ? (<IconButton aria-label="Dark mode" icon={<MoonIcon />} onClick={toggleColorMode} />)
                    : (<IconButton aria-label="Light mode" icon={<SunIcon />} onClick={toggleColorMode} />
                    )}
            </Box>
        </Flex>
    );
};

export default Header;
