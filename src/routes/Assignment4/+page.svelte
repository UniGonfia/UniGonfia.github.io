<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    import * as d3_geo from 'd3-geo-projection';
    import data_file from '$lib/data/tree_coordinates.json'


    onMount(() => {
        const width = 7500;
        const height = 4000;

        const svg = d3.select('.graph')
            .append('svg')
            .attr('width', width)
            .attr('height', height);

        const projection = d3.geoMercator()
            .scale(500)
            .translate([width / 4, height / 4]);

        const path = d3.geoPath()
            .projection(projection);

        const g = svg.append('g');

        d3.json('https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson')
            .then(function(data) {

                data.features = data.features.filter(function(d) {
                    return d.properties.name == 'USA'
                })

                g.selectAll('path')
                    .data(data.features)
                    .enter()
                    .append('path')
                    .attr('fill', '#b8b8b8')
                    .attr('d', path)
                    .style('stroke', 'black')
                    .style('opacity', .3)
            });

        var data = data_file;
        // cancel random point mantain the 10%
        

        g.selectAll('circle')
            .data(data)
            .enter()
            .append('circle')
            .attr('cx', function(d) {
                return projection([d.ln, d.la])[0];
            })
            .attr('cy', function(d) {
                return projection([d.ln, d.la])[1];
            })
            .attr('r', 2)
            .style('fill', 'red')
            

        
    });
    
</script>

<div class="graph">

</div>

<style>

</style>