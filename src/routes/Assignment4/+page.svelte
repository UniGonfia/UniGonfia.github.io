<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    import data from '$lib/data/tree_density.json'
    import 'iconify-icon'
    import mapdata from '$lib/data/choropleth.json'

    function left_btn() {
        
        //create animation to move map to the left and appear on the right
        let svg = d3.select("svg");
        //clean
        svg.selectAll("circle").remove();
        svg.selectAll("path").remove();
        svg.selectAll("g").remove();
        svg.selectAll("text").remove();
        svg.selectAll("rect").remove();
        svg.selectAll("line").remove();
        svg.selectAll("polygon").remove();
        
        createMap()

        const svgdiv = document.querySelector("svg");
        svgdiv.classList.add("moveLeft");

        svgdiv.addEventListener("animationend", () => {
            svgdiv.classList.remove("moveLeft");
        });

    }

    function right_btn() {
        //create animation to move map to the right and appear on the left
        let svg = d3.select("svg");
        //clean
        svg.selectAll("circle").remove();
        svg.selectAll("path").remove();
        svg.selectAll("g").remove();
        svg.selectAll("text").remove();
        svg.selectAll("rect").remove();
        svg.selectAll("line").remove();
        svg.selectAll("polygon").remove();
        
        createMap()

        const svgdiv = document.querySelector("svg");
        svgdiv.classList.add("moveRight");

        svgdiv.addEventListener("animationend", () => {
            svgdiv.classList.remove("moveRight");
        });
    }

    function createMap() {
        // The svg
        const svg = d3.select("svg");
        const width = document.querySelector("svg").getBoundingClientRect().width;
        const height = document.querySelector("svg").getBoundingClientRect().height;

        // Map and projection
        const projection = d3.geoAlbersUsa()
            .translate([width/2, height/2])
            .scale([1000])
        
        let path = d3.geoPath().projection(projection);
        
        let world = svg.append("g");
        const data_features = topojson.feature(mapdata, mapdata.objects.states).features;
        world.selectAll(".states")
            .data(data_features)
            .enter().append("path")
            .attr("data-name", function(d) { return d.properties.name }) 
            .attr("d", path)
            .style("stroke", "black")
            .attr("class", "Country")
            .attr("id", function(d) { return d.id })
            .style("opacity", 1)
            .style("fill", "white")

        return projection
    }

    onMount(async () => {
       // The svg
        const svg = d3.select("svg");     

        const projection = createMap()

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

<div class="Panel"> <button class="buttonleft" on:click={left_btn}> <iconify-icon class="icon" icon="typcn:arrow-up-outline" width="100%" /> </button> </div>
<svg id="map_graph" width="900" height="900"></svg>
<div class="Panel"><button class="buttonright" on:click={right_btn}> <iconify-icon class="icon" icon="typcn:arrow-up-outline" width="100%" /> </button> </div>

<div class="moveLeft moveRight" style="display: none;"></div>

</div>
<style>

.assignment4 {
    background-color: #364e51;
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: row;
    flex-wrap: nowrap;
    overflow: hidden;
}

button {
    position: relative;
    width: 5rem;
    height: 5rem;
    background-color: transparent;
    border: 0;
}

.buttonleft {
    left: 0;
    transform: rotate(-90deg);
}

.buttonright {
    right: 0;
    transform: rotate(90deg);
}

.Panel {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;

    width: 10%;
    height: 100%;
    background-color: #364e51;
    z-index: 50;
}

svg {

    display: block;
    margin-inline: auto;
    width: 80%;
    height: 100%;
}

.icon {
    background-color: wheat;
    border: 3px solid black;
    border-radius: 50%;
}

.moveLeft {
    animation: moveLeft 2s ease-out;
}

.moveRight {
    animation: moveRight 2s ease-out;
}

@keyframes moveLeft {
    0% {
        transform: translateX(0);
    }
    50% {
        transform: translateX(-100%);
        opacity: 0;
    }
    51% {
        transform: translateX(200%);
    }
    100% {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes moveRight {
    0% {
        transform: translateX(0);
    }
    50% {
        transform: translateX(100%);
        opacity: 0;
    }
    51% {
        transform: translateX(-200%);
    }
    100% {
        transform: translateX(0);
        opacity: 1;
    }
}

</style>