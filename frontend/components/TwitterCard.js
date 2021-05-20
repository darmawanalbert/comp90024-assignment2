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
    Box, Image, Text, Flex,
} from '@chakra-ui/react';
import { FaTwitter } from 'react-icons/fa';

const TwitterCard = ({
    imageSource, displayName, username, tweet, time, date,
}) => (
    <Box maxW="xs" p={4} borderWidth="1px" borderRadius="lg" overflow="hidden">
        <Flex justifyContent="flex-start" alignItems="center" marginBottom={4}>
            <Image src={imageSource || '/avatar.png'} alt={displayName} borderRadius="full" boxSize="40px" />
            <Box marginLeft={2}>
                <Text fontWeight="semibold" lineHeight="100%">{displayName}</Text>
                <Text fontSize="sm" color="gray.500">{`@${username}`}</Text>
            </Box>
        </Flex>
        <Text>{tweet}</Text>
        <Flex justifyContent="space-between" alignItems="center">
            <Text fontSize="sm">
                {time}
                <span>&nbsp;·&nbsp;</span>
                {date}
            </Text>
            <FaTwitter style={{ color: '#00acee' }} />
        </Flex>
    </Box>
);

export default TwitterCard;
