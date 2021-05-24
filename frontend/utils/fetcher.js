/*
COMP90024 Team 1
Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au
*/

import useSWR from 'swr';

const useMapInfo = (apiUrl) => {
    const { data, error } = useSWR(`${apiUrl}/cities`);
    return {
        mapInfo: data,
        isMapInfoLoading: !error && !data,
        isMapInfoError: error,
    };
};

const useLdaScores = (apiUrl) => {
    const { data, error } = useSWR(`${apiUrl}/lda-scores`);
    return {
        ldaScores: data,
        isLdaScoresLoading: !error && !data,
        isLdaScoresError: error,
    };
};

const useChartInfo = (apiUrl) => {
    const { data, error } = useSWR(`${apiUrl}/charts`);
    return {
        chartInfo: data,
        isChartInfoLoading: !error && !data,
        isChartInfoError: error,
    };
};

export { useMapInfo, useLdaScores, useChartInfo };
