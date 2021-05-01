/*
COMP90024 Team 1
Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au
*/

// Inspired from: https://raptis.wtf/blog/create-a-navbar-with-chakra-ui-react/

import React from 'react';
import {
    Text, Stack, Box, LinkBox, LinkOverlay, useColorMode, IconButton, Spacer,
} from '@chakra-ui/react';
import NextLink from 'next/link';
import { SunIcon, MoonIcon } from '@chakra-ui/icons';

import GithubButton from './GithubButton';

const MenuItem = ({
    children, isLast, to = '/', ...restProps
}) => (
    <LinkBox>
        <Text display="block" {...restProps}>
            <NextLink href={to} passHref>
                <LinkOverlay>{children}</LinkOverlay>
            </NextLink>
        </Text>
    </LinkBox>
);

const MenuList = ({ isOpen }) => {
    const { colorMode, toggleColorMode } = useColorMode();
    return (
        <Box
            display={{ base: isOpen ? 'block' : 'none', md: 'block' }}
            flexBasis={{ base: '100%', md: 'auto' }}
        >
            <Stack
                spacing={8}
                align="center"
                justify={['center', 'center', 'flex-end', 'flex-end']}
                direction={['column', 'row', 'row', 'row']}
                pt={[4, 4, 0, 0]}
            >
                <MenuItem to="/">Data</MenuItem>
                <MenuItem to="/analysis">Analysis</MenuItem>
                <MenuItem to="/about">About</MenuItem>
                {colorMode === 'light'
                    ? (<IconButton aria-label="Dark mode" icon={<MoonIcon />} onClick={toggleColorMode} variant="ghost" colorScheme="teal.400" />)
                    : (<IconButton aria-label="Light mode" icon={<SunIcon />} onClick={toggleColorMode} variant="ghost" colorScheme="teal.400" />
                    )}
                <Spacer />
                <GithubButton />
            </Stack>
        </Box>
    );
};

export default MenuList;
