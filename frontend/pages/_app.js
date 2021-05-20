/*
COMP90024 Team 1
Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au
*/

import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import { SWRConfig } from 'swr';
import axios from 'axios';
import { API_REFRESH_INTERVAL } from '../utils/config';
import theme from '../utils/theme';

function MyApp({ Component, pageProps }) {
    return (
        <ChakraProvider theme={theme}>
            <SWRConfig value={{
                refreshInterval: API_REFRESH_INTERVAL,
                fetcher: (resource, init) => axios.get(resource, init).then((res) => res.data),
            }}
            >
                <Component {...pageProps} />
            </SWRConfig>
        </ChakraProvider>
    );
}

export default MyApp;
