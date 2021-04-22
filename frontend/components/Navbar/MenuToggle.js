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
import { Box, IconButton } from '@chakra-ui/react';
import { CloseIcon, HamburgerIcon } from '@chakra-ui/icons';

const MenuToggle = ({ toggle, isOpen }) => (
    <Box display={{ base: 'block', md: 'none' }} onClick={toggle}>
        {isOpen
            ? <IconButton colorScheme="teal" aria-label="Close menu" icon={<CloseIcon />} />
            : <IconButton colorScheme="teal" aria-label="Open menu" icon={<HamburgerIcon />} />}
    </Box>
);

export default MenuToggle;
