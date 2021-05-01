/* eslint-disable no-param-reassign */
/*
COMP90024 Team 1
Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au
*/

// Inspired from: https://dev.to/naomigrace/how-to-integrate-mapbox-gl-js-in-your-next-js-project-without-react-map-gl-or-a-react-wrapper-library-50f#2-adding-a-map

const addDataLayer = (map, data) => {
    // map.addSource('earthquakes', {
    //     type: 'geojson',
    //     data,
    //     cluster: true,
    //     clusterMaxZoom: 14,
    //     clusterRadius: 50,
    // });

    // map.addLayer({
    //     id: 'clusters',
    //     type: 'circle',
    //     source: 'earthquakes',
    //     filter: ['has', 'point_count'],
    //     paint: {
    //         'circle-color': [
    //             'step',
    //             ['get', 'point_count'],
    //             '#51bbd6',
    //             100,
    //             '#f1f075',
    //             750,
    //             '#f28cb1',
    //         ],
    //         'circle-radius': [
    //             'step',
    //             ['get', 'point_count'],
    //             20,
    //             100,
    //             30,
    //             750,
    //             40,
    //         ],
    //     },
    // });

    // map.addLayer({
    //     id: 'cluster-count',
    //     type: 'symbol',
    //     source: 'earthquakes',
    //     filter: ['has', 'point_count'],
    //     layout: {
    //         'text-field': '{point_count_abbreviated}',
    //         'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
    //         'text-size': 12,
    //     },
    // });

    // map.addLayer({
    //     id: 'unclustered-point',
    //     type: 'circle',
    //     source: 'earthquakes',
    //     filter: ['!', ['has', 'point_count']],
    //     paint: {
    //         'circle-color': '#11b4da',
    //         'circle-radius': 4,
    //         'circle-stroke-width': 1,
    //         'circle-stroke-color': '#fff',
    //     },
    // });

    map.addSource('cities', {
        type: 'geojson',
        data,
        cluster: false,
    });

    map.addLayer({
        id: 'city',
        type: 'fill',
        source: 'cities', // reference the data source
        layout: {},
        paint: {
            'fill-color': '#0080ff', // blue color fill
            'fill-opacity': 0.5
        }
    });
};

const initialiseMap = (mapboxgl, map) => {
    map.on('click', 'clusters', (e) => {
        const features = map.queryRenderedFeatures(e.point, {
            layers: ['clusters'],
            // layers: ['cities_top50_simplified'],
        });
        const clusterId = features[0].properties.cluster_id;
        map.getSource('earthquakes').getClusterExpansionZoom(
            clusterId,
            (err, zoomVal) => {
                if (err) return;
                map.easeTo({
                    center: features[0].geometry.coordinates,
                    zoom: zoomVal,
                });
            },
        );
    });

    map.on('click', 'unclustered-point', (e) => {
        const coordinates = e.features[0].geometry.coordinates.slice();
        const { mag } = e.features[0].properties;
        let tsunami = 'no';
        if (e.features[0].properties.tsunami === 1) {
            tsunami = 'yes';
        }

        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        new mapboxgl.Popup()
            .setLngLat(coordinates)
            .setHTML(`magnitude: ${mag} <br>Was there a tsunami?: ${tsunami}`)
            .addTo(map);
    });

    map.on('mouseenter', 'clusters', () => {
        map.getCanvas().style.cursor = 'pointer';
    });

    map.on('mouseleave', 'clusters', () => {
        map.getCanvas().style.cursor = '';
    });
};

export { addDataLayer, initialiseMap };
