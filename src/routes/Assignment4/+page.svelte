<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    import * as d3_geo from 'd3-geo-projection';
    import data from '$lib/data/tree_density.json'

    /*
    The data:
        {
            "state": "Texas",
            "num_points": 10,
            "middle_point": {
                "longitude": -91.18689123500002,
                "latitude": 37.63236978
            }
        
    ...

    */

    onMount(async () => {
       // The svg
        const svg = d3.select("svg"),
            width = +svg.attr("width"),
            height = +svg.attr("height");

        // Map and projection
        const projection = d3.geoMercator()
            .center([-103.77156, 44.967243])                // GPS of location to zoom on
            .scale(300)                       // This is like the zoom
            .translate([ width/2, height/2 ])

        // Load external data and boot
        await d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson").then( function(data){

            // Filter data
            data.features = data.features.filter(d => {console.log(d.properties.name); return d.properties.name=="USA"})

            // Draw the map
            svg.append("g")
                .selectAll("path")
                .data(data.features)
                .join("path")
                .attr("fill", "grey")
                .attr("d", d3.geoPath()
                    .projection(projection)
                )
                .style("stroke", "none")
        })


        const radius = d3.scaleSqrt()
            .domain([0, 100000])
            .range([0, 10])
        
        // Add circles:
        svg.selectAll("Circle")
        .data(data)
        .enter()
        .append("circle")
            .attr("cx", function(d){ return projection([d.middle_point.longitude, d.middle_point.latitude])[0] })
            .attr("cy", function(d){ return projection([d.middle_point.longitude, d.middle_point.latitude])[1] })
            .style("fill", "red")
            .attr("stroke", "white")
            .attr("stroke-width", 0.2)
            .attr("fill-opacity", .3)
            .attr("r", function(d){ return radius(d.num_points)})
            
            


        
    });
    
</script>
<div class="assignment4">
<!-- Create an element where the map will take place -->
<svg id="my_dataviz" width="1000" height="800"></svg>
</div>
<style>

.assignment4 {
    background-color: black;
    width: 100%;
    height: 100vh;
    display: block;
}

svg {
    width: 1000px;
    height: 800px;
    display: block;
    margin-inline: auto;
    margin-block: auto;
    z-index: 0;
}

</style>