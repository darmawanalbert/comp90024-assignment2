/*
COMP90024 Team 1
Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au
*/

import useSWR from 'swr';
import { API_URL } from './config';

const useMapInfo = () => {
    const { data, error } = useSWR(`${API_URL}/examples`);
    return {
        mapInfo: data,
        isLoading: !error && !data,
        isError: error,
    };
};

export { useMapInfo };
