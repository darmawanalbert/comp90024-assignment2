/*
COMP90024 Team 1
Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au
*/

// Inspired from: https://raptis.wtf/blog/create-a-navbar-with-chakra-ui-react/

import React, { useState } from 'react';
import { Flex } from '@chakra-ui/react';
import Logo from './Logo';
import MenuToggle from './MenuToggle';
import MenuList from './MenuList';

const NavbarContainer = ({ children, ...restProps }) => (
    <Flex
        as="nav"
        align="center"
        justify="space-between"
        wrap="wrap"
        w="100%"
        p={4}
        bg="teal.400"
        {...restProps}
    >
        {children}
    </Flex>
);

const Navbar = (props) => {
    const [isOpen, setIsOpen] = useState(false);
    const toggle = () => setIsOpen(!isOpen);
    return (
        <NavbarContainer {...props}>
            <Logo />
            <MenuToggle toggle={toggle} isOpen={isOpen} />
            <MenuList isOpen={isOpen} />
        </NavbarContainer>
    );
};

export default Navbar;
