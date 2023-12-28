<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    import 'iconify-icon'

    import mapdata from '$lib/data/choropleth.json'
    import data_tree_density from '$lib/data/tree_density.json'
    import data_tree_10_density from '$lib/data/tree_density_species.json'
    import data_state_density from '$lib/data/tree_density_state.json'

    let position = 0;

    function position_switch() {
        if (position == 0) {
            tree_density()
            document.querySelector(".description").innerHTML = description_tree_density
        }

        if (position == 1) {
            top_tree_density()
            document.querySelector(".description").innerHTML = description_tree_density_10
        }

        if (position == -1) {
            state_density()
            document.querySelector(".description").innerHTML = description_state_density
        }
    }

    let description_tree_density = `
        Here we can see a map depicting the distribution of trees in the United States. 
        Larger dots have been chosen to represent the greater presence of trees in that area, obviously we can see 
        that in desert areas there are fewer trees while in more favourable areas there are more trees.
    `

    let description_tree_density_10 = `
        In this graph we can see the distribution of trees in the United States with one more piece of information, 
        namely the distribution of the top 10 tree species. The position is the same as in the previous graph but we 
        can also see the distribution of the species, in warmer areas we have Gleditsia triacanthos and Lagerstroemia 
        indica while in colder areas we have Platanus acerifolia.
    `

    let description_state_density = `
        In this graph, however, we no longer focus on the exact position of the trees but on the density for each state. 
        In particular, California and New York state jump out at you; by hovering the mouse over the state, you can see 
        the exact amount of trees.
    `

    async function left_btn() {

        const svgdiv = document.querySelector("svg");
        svgdiv.classList.add("moveLeft");

        svgdiv.addEventListener("animationstart", async () => {
            //wait 1s
            await new Promise(r => setTimeout(r, 1000));
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
            svg.selectAll("Circle").remove();
            svg.selectAll("*").remove();
            svg.selectAll("g").remove();
            svg.html("")
            svg.selectAll(".circlemap").remove();
            svgdiv.innerHTML = "";

            createMap()
        }, { once: true})

        svgdiv.addEventListener("animationend", () => {
            svgdiv.classList.remove("moveLeft");
            position_switch()
        }, { once: true});



        if (position < 1) {
            position += 1;
        } else {
            position = -1;
        }

        let description = document.querySelector(".description");
        description.classList.add("opacityDescription");
        
        description.addEventListener("animationend", () => {
            description.classList.remove("opacityDescription");
        }, { once: true});

        description.addEventListener("animationstart", async () => {
            
            if (position == 0) {
                description.innerHTML = description_tree_density
            }

            if (position == 1) {
                description.innerHTML = description_tree_density_10
            }

            if (position == -1) {
                description.innerHTML = description_state_density
            }
        }, { once: true})

    }

    async function right_btn() {
        const svgdiv = document.querySelector("svg");
        svgdiv.classList.add("moveRight");

        svgdiv.addEventListener("animationstart", async () => {
            //wait 1s
            await new Promise(r => setTimeout(r, 1000));
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
            svg.selectAll("Circle").remove();
            svg.selectAll("*").remove();
            svg.selectAll("g").remove();
            svg.html("")
            svg.selectAll(".circlemap").remove();
            svgdiv.innerHTML = "";

            createMap()
        }, { once: true})

        svgdiv.addEventListener("animationend", () => {
            svgdiv.classList.remove("moveRight");
            position_switch()
        }, { once: true});

        if (position > -1) {
            position -= 1;
        } else {
            position = 1;
        }

        let description = document.querySelector(".description");
        description.classList.add("opacityDescription");
        
        description.addEventListener("animationend", () => {
            description.classList.remove("opacityDescription");
        }, { once: true});

        description.addEventListener("animationstart", async () => {
            //wait 1s

            if (position == 0) {
                description.innerHTML = description_tree_density
            }

            if (position == 1) {
                description.innerHTML = description_tree_density_10
            }

            if (position == -1) {
                description.innerHTML = description_state_density
            }
        }, { once: true})
    }

    function createMap() {
        // The svg
        const svg = d3.select("svg");
        const width = document.querySelector("svg").getBoundingClientRect().width;
        const height = document.querySelector("svg").getBoundingClientRect().height - 100;

        // Map and projection
        const projection = d3.geoAlbersUsa()
            .translate([width/2, height/2])
            .scale([1200])
        
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

    function tree_density() {
        const svg = d3.select("svg");     
        const width = document.querySelector("svg").getBoundingClientRect().width;
        const height = document.querySelector("svg").getBoundingClientRect().height - 100;

        const projection = d3.geoAlbersUsa()
            .translate([width/2, height/2])
            .scale([1200])

        const radius = d3.scaleSqrt()
            .domain([0, 100000])
            .range([0, 20])

        // Add circles:
        svg.selectAll("Circle")
        .data(data_tree_density)
        .enter()
        .append("circle")
            .attr("cx", function(d){ return projection([d.middle_point.longitude, d.middle_point.latitude])[0] })
            .attr("cy", function(d){ return projection([d.middle_point.longitude, d.middle_point.latitude])[1] })
            .style("fill", "red")
            .attr("stroke", "white")
            .attr("stroke-width", 0.2)
            .attr("fill-opacity", .3)
            .attr("r", function(d){ return radius(d.num_points)})
            .attr("class", "circlemap")

        // Add title and explanation
        svg.append("text")
            .attr("text-anchor", "middle")
            .style("fill", "wheat")
            .attr("x", width / 2)
            .attr("y", 30)
            .attr("width", 90)
            .html("Tree density in the USA")
            .style("font-size", "30px")

        //add on hover on circle with a tooltip
        const tooltip = d3.select("body")
            .append("div")
            .style("position", "absolute")
            .style("background-color", "wheat")
            .style("border-radius", "5px")
            .style("padding", "10px")
            .style("opacity", 0)

        const mouseover = function(event, d) {
            tooltip
                .style("opacity", 1)
        }

        const mousemove = function(event, d) {
            tooltip
                .html(`State: ${d.state}  <br/> Number of trees: ${d.num_points}`)
                .style("left", (event.x + 30) + "px")
                .style("top", (event.y + 30) + "px")

            d3.select(this)
                .style("stroke", "black")
                .style("stroke-width", 2)
                .style("opacity", 1)
                .attr("r", function(d){ return radius(d.num_points) + 10})

        }

        const mouseleave = function(event, d) {
            tooltip
                .transition()
                .duration(200)
                .style("opacity", 0)

            d3.select(this)
                .style("stroke", "black")
                .style("stroke-width", 0.2)
                .style("opacity", 1)
                .attr("r", function(d){ return radius(d.num_points)})
        }

        svg.selectAll("circle")
            .on("mouseover", mouseover)
            .on("mousemove", mousemove)
            .on("mouseleave", mouseleave)
    }


    function top_tree_density() {
        const svg = d3.select("svg");
        const width = document.querySelector("svg").getBoundingClientRect().width;
        const height = document.querySelector("svg").getBoundingClientRect().height - 100;

        const projection = d3.geoAlbersUsa()
            .translate([width/2, height/2])
            .scale([1200])

        const radius = d3.scaleSqrt()
            .domain([0, 100000])
            .range([0, 20])

        let species = []
        data_tree_10_density.forEach(function(d) {
            d.species.forEach(function(s) {
                species.push(s.scientific_name)
            })
        })

        let unique_species = [...new Set(species)]
        unique_species.push("other")

        //create array with the species, the coordinate, the number of trees and the state, and create also a point for the other species
        let data = []
        data_tree_10_density.forEach(function(d) {
            d.species.forEach(function(s) {
                data.push({
                    "species": s.scientific_name,
                    "coordinate": [d.middle_point.longitude, d.middle_point.latitude],
                    "num_points": s.num_points_species,
                    "state": d.state
                })
            })
            data.push({
                "species": "other",
                "coordinate": [d.middle_point.longitude, d.middle_point.latitude],
                "num_points": d.num_points - d.species.reduce((a, b) => a + b.num_points_species, 0),
                "state": d.state
            })
        })

        //create a color scale for the species
        const color = d3.scaleOrdinal()
            .domain(unique_species)
            .range(d3.schemeSet3);

        // Add circles:
        svg.selectAll("Circle")
        .data(data)
        .enter()
        .append("circle")
            .attr("cx", function(d){ return projection(d.coordinate)[0] })
            .attr("cy", function(d){ return projection(d.coordinate)[1] })
            .style("fill", function(d) { return color(d.species) })
            .attr("stroke", "white")
            .attr("stroke-width", 0.2)
            .attr("fill-opacity", function(d) { if (d.species == "other") { return 0.3 } else { return 0.8 } })
            .attr("r", function(d){ return radius(d.num_points)})
            .attr("class", "circlemap")

        // Add title and explanation
        svg.append("text")
            .attr("text-anchor", "middle")
            .style("fill", "wheat")
            .attr("x", width / 2)
            .attr("y", 30)
            .attr("width", 90)
            .html("Tree density in the USA of Top 10 Species")
            .style("font-size", "30px")

        //create a legend with color and species name
        const legend = svg.selectAll(".legend")
            .data(unique_species)
            .enter().append("g")
            .attr("class", "legend")
            .attr("transform", function(d, i) { return `translate(${-200 },${i * 20 + 400})`; });

        legend.append("rect")
            .attr("x", width - 18)
            .attr("width", 18)
            .attr("height", 18)
            .style("fill", function(d) { return color(d) });

        //add label on the rect
        legend.append("text")
            .attr("x", width + 5)
            .attr("y", 9)
            .attr("dy", ".35em")
            .style("fill", "wheat")
            .style("text-anchor", "start")
            .text(function(d) { return d; });
    }

    function state_density() {
        const svg = d3.select("svg");
        const width = document.querySelector("svg").getBoundingClientRect().width;
        const height = document.querySelector("svg").getBoundingClientRect().height - 100;

        //color each state with a different color based on the number of trees
        let data = []
        data_state_density.forEach(function(d) {
            data.push({
                "state": d.state,
                "num_trees": d.num_trees
            })
        })

        //create a color scale for the species
        const color = d3.scaleSequential()
            .domain([0, d3.max(data, function(d) { return d.num_trees })])
            .interpolator(d3.interpolateYlOrRd);

        // Map and projection
        const projection = d3.geoAlbersUsa()
            .translate([width/2, height/2])
            .scale([1200])

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
            .style("fill", function(d) { 
                let state = data.find(function(s) { return s.state == d.properties.name })
                if (state) {
                    return color(state.num_trees)
                } else {
                    return "white"
                }
            })

        // Add title and explanation
        svg.append("text")
            .attr("text-anchor", "middle")
            .style("fill", "wheat")
            .attr("x", width / 2)
            .attr("y", 30)
            .attr("width", 90)
            .html("Tree density in the USA by State")
            .style("font-size", "30px")

        //add tooltip on hover to a state with the number of trees
        const tooltip = d3.select("body")
            .append("div")
            .style("position", "absolute")
            .style("background-color", "wheat")
            .style("border-radius", "5px")
            .style("padding", "10px")
            .style("opacity", 0)

        const mouseover = function(event, d) {
            tooltip
                .style("opacity", 1)
        }

        const mousemove = function(event, d) {
            let state = data.find(function(s) { return s.state == d.properties.name })
            if (!state) {
                state = {
                    "num_trees": 0
                }
            }
            tooltip
                .html(`State: ${d.properties.name}  <br/> Number of trees: ${state.num_trees}`)
                .style("left", (event.x + 30) + "px")
                .style("top", (event.y + 30) + "px")

            d3.select(this)
                .style("stroke", "black")
                .style("stroke-width", 2)
                .style("opacity", 1)

        }

        const mouseleave = function(event, d) {
            tooltip
                .transition()
                .duration(200)
                .style("opacity", 0)

            d3.select(this)
                .style("stroke", "black")
                .style("stroke-width", 0.2)
                .style("opacity", 1)
        }

        svg.selectAll("path")
            .on("mouseover", mouseover)
            .on("mousemove", mousemove)
            .on("mouseleave", mouseleave)
    }


    onMount(() => {    
        createMap()    
        tree_density()
    });
    
</script>
<div class="backhome">
    <a href="/"> &#x2190 Home </a>
</div>

<p class="description opacityDescription"> {description_tree_density} </p>

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

.backhome {
    position: absolute;
    top: 2rem;
    left: 2rem;
    z-index: 100;
}

.backhome a {
    font-size: 1.5em;
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
    height: 80%;
}

.description {
    position: absolute;
    bottom: 1rem;
    left: 50%;
    transform: translateX(-50%);
    z-index: 100;
    font-size: 1.2em;
    color: wheat;
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

.opacityDescription {
    animation: opacityDescription 3s ease-out;
}

@keyframes opacityDescription {
    0% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
}

</style>