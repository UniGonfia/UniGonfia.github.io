<script>

    import data_file from '$lib/data/assignment2.json';
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    import * as d3_sankey from 'd3-sankey';
    import * as d3_boxplot from 'd3-boxplot';
    /*
    Data:
        {
            city: string,
            state: string,
            scientific_name: string,
            count: number, //count of species
            mean_height: number, //mean height of species
            mean_diameter: number, //mean diameter of species
        }
    */


    function alluvion_filter(data, n_state, n_city, n_species) {
         // Remove null state
        data = data.filter(d => d.state !== null);

        // Get the top n_state states by count
        let top_states = data.reduce((acc, cur) => {
            acc[cur.state] = (acc[cur.state] || 0) + cur.count;
            return acc;
        }, {});
        top_states = Object.keys(top_states)
            .sort((a, b) => top_states[b] - top_states[a])
            .slice(0, n_state);
        data = data.filter(d => top_states.includes(d.state));

        // Get the top n_city cities for each state by count
        let top_cities = top_states.map(state => {
            let city_count = data
                .filter(d => d.state === state)
                .reduce((acc, cur) => {
                    acc[cur.city] = (acc[cur.city] || 0) + cur.count;
                    return acc;
                }, {});
            return { state, cities: Object.keys(city_count)
                .sort((a, b) => city_count[b] - city_count[a])
                .slice(0, n_city) };
        });
        data = data.filter(d => top_cities.find(e => e.state === d.state).cities.includes(d.city));

        // Get the top n_species species for each city by count
        let top_species = top_cities.map(({ state, cities }) => {
            return {
                state,
                city_species: cities.map(city => {
                    let species_count = data
                        .filter(d => d.state === state && d.city === city)
                        .reduce((acc, cur) => {
                            acc[cur.scientific_name] = (acc[cur.scientific_name] || 0) + cur.count;
                            return acc;
                        }, {});
                    return { city, species: Object.keys(species_count)
                        .sort((a, b) => species_count[b] - species_count[a])
                        .slice(0, n_species) };
                })
            };
        });
        data = data.filter(d => top_species.find(e => e.state === d.state).city_species.find(f => f.city === d.city).species.includes(d.scientific_name));

        // If city == New York, change to New York City
        data = data.map(d => {
            if (d.city === 'New York') {
                d.city = 'New York City';
            }
            return d;
        });

        return data;
    }
        
    async function alluvion_chart(n_state, n_city, n_species) {

        //clean the chart
        d3.select('#alluvion-chart').selectAll('*').remove();

        let data = alluvion_filter(data_file, n_state, n_city, n_species);
        
        // sankey graph
        const margin = { top: 30, right: 150, bottom: 10, left: 50 };
        const width = 1400 - margin.left - margin.right;
        const height = 800 - margin.top - margin.bottom;

        const svg = d3.select('#alluvion-chart')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .attr('style', 'color: wheat');

        const sankey = d3_sankey.sankey()
            .nodeId(d => d.name)
            .nodeAlign(d3_sankey.sankeyLeft)
            .nodeWidth(30)
            .nodePadding(15)
            .extent([[100, 100], [width, height]]);


        const cities = [...new Set(data.map(d => d.city))];
        const states = [...new Set(data.map(d => d.state))];

        // https://api.gbif.org/v1/species?name=platanus%20acerifolia for family species
        const data_fetch = async (name) => {
            const request = "https://api.gbif.org/v1/species?name="+name;
            const response = await fetch(request);
            const json = await response.json();

            if (json.results.length === 0) return "N/A";

            if (json.results[0].family === undefined) return "N/A";

            return json.results[0].family;

        }

        await Promise.all(data.map(async (d) => {
            d.family = await data_fetch(d.scientific_name);
        }));

        const family = [...new Set(data.map(d => d.family))];


        const { nodes, links } = sankey({
            nodes: [
                ...states.map(d => ({ name: d, count: data.filter(e => e.state === d).length })),
                ...cities.map(d => ({ name: d, count: data.filter(e => e.city === d).length })),
                ...family.map(d => ({ name: d, count: data.filter(e => e.family === d).length })),
            ],
            links: [
                ...data.map(d => ({ source: d.state, target: d.city, value: d.count })),
                ...data.map(d => ({ source: d.city, target: d.family, value: d.count }))
            ]
        });

        const color = d3.scaleOrdinal()
            .domain(nodes.map(d => d.name))
            .range([    
                '#ff5555', '#5599ff', '#66ff66', '#cc66cc', '#ff9933', '#ffff66',
                '#cc7733', '#ff99ff', '#aaaaaa', '#bbddff', '#3399ff', '#ccff99',
                '#dd99dd', '#ffcc88', '#ffffcc', '#ff9933', '#ffcc88', '#cc7744',
                '#aaddcc', '#ffffcc', '#d0d0da', '#ff9999', '#aaddee', '#ffcc66',
                '#55aa55', '#ccffcc', '#ffbbdd', '#ccff55', '#3344dd', '#ffddbb'
            ]);

        const rect = svg.append('g')
            .attr('stroke', '#000')
            .selectAll('rect')
                .data(nodes)
                .join('rect')
                .attr('x', d => d.x0 + margin.left)
                .attr('y', d => d.y0)
                .attr("height", d => d.y1 - d.y0)
                .attr("width", d => d.x1 - d.x0)
                .attr("fill", d => color(d.name));
        
        rect.append("title")
            .text(d => `${d.name}`)

        const link = svg.append('g')
            .attr("fill", "none")
            .attr("stroke-opacity", 1)
                .selectAll()
                .data(links)
                .join("g")
                .style("mix-blend-mode", "multiply")
                .attr("transform", `translate(${margin.left}, 0)`)

        link.append("path")
            .attr("d", d3_sankey.sankeyLinkHorizontal())
            .attr("stroke", d => color(d.source.name))
            .attr("stroke-opacity", 0.4)
            .attr("stroke-width", d => Math.max(1, d.width))
            .on("mouseover", function (event, d) {
                d3.select(this)
                    .attr("stroke-opacity", 0.9)
            })
            .on("mouseout", function (event, d) {
                d3.select(this)
                    .attr("stroke-opacity", 0.4)
            })
            .append("title")
            .text(d => `${d.source.name} → ${d.target.name}\n${d.value.toLocaleString()}`);

        
        svg.append("g")
            .selectAll()
                .data(nodes)
                .join("text")
                .attr("x", d => d.x0 < width / 2 ? d.x1 - 40 : d.x0 + 40)
                .attr("y", d => (d.y1 + d.y0) / 2)
                .attr("dy", "0.35em")
                .attr("text-anchor", d => d.x0 < width / 2 ? "end" : "start")
                .attr("fill", "wheat")
                .text(d => d.name)
                .attr("transform", `translate(${margin.left}, 0)`)
        
        //add title
        svg.append("text")
            .attr("x", width / 2 + margin.left + 50)
            .attr("y", margin.top)
            .attr("text-anchor", "middle")
            .attr("fill", "wheat")
            .style("font-size", "1.25em")
            .text(`Alluvion Chart of Top ${n_state} States, Top ${n_city} Cities, Top ${n_species} Species`);



        rect.on("mouseover", function (event, d) {

            let links = svg.selectAll("path")
                .filter(e => e.source.name === d.name || e.target.name === d.name)
                .attr("stroke-opacity", 0.9)
            
        })

        rect.on("mouseout", function (event, d) {

            let links = svg.selectAll("path")
                .filter(e => e.source.name === d.name || e.target.name === d.name)
                .attr("stroke-opacity", 0.4)
        })

    }

    function boxplot_filter(data) {

        //take the species with heigh_M != null
        data = data.filter(d => d.mean_height !== null);

        //take the top 10 species by count
        let top_species = data.reduce((acc, cur) => {
            acc[cur.scientific_name] = (acc[cur.scientific_name] || 0) + cur.count;
            return acc;
        }, {});
        top_species = Object.keys(top_species).sort((a, b) => top_species[b] - top_species[a]).slice(0, 10);
        data = data.filter(d => top_species.includes(d.scientific_name));

        const speciesData = {};
        data.forEach((entry) => {
        const species = entry.scientific_name;
        if (!speciesData[species]) {
            speciesData[species] = [];
        }
        speciesData[species].push(entry.mean_height);
        });

        // Convert data to an array for D3.js
        let boxPlotData = Object.keys(speciesData).map((species) => ({
            species,
            heights: speciesData[species].filter((height) => height !== 0),
        }));

        
        return boxPlotData;
    }

    function boxplot_chart() {

        let data = boxplot_filter(data_file);

        //boxplot
        const margin = { top: 100, right: 200, bottom: 100, left: 100 };
        const width = 1400 - margin.left - margin.right;
        const height = 700 - margin.top - margin.bottom;

        const svg = d3.select('#box-plot')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .attr('style', 'color: wheat')

        // Compute quartiles, median, inter quantile range min and max --> these info are then used to draw the box
        var sumstat = d3.group(data, d => d.species)
        // remove species property inside the value
        sumstat.forEach((value, key, map) => {
            map.set(key, value.map(d => d.heights).flat())
        })


        var allBoxes = []
        for (let [key, value] of sumstat) {
            var sortedValues = value.sort(d3.ascending)
            var q1 = d3.quantile(sortedValues, .25)
            var median = d3.quantile(sortedValues, .5)
            var q3 = d3.quantile(sortedValues, .75)
            var interQuantileRange = q3 - q1
            
            var min = sortedValues[0]
            var max = sortedValues[sortedValues.length - 1]
            allBoxes.push({ species: key, q1: q1, median: median, q3: q3, interQuantileRange: interQuantileRange, min: min, max: max })
        }

        // Show the X scale
        var x = d3.scaleBand()
            .range([margin.left, width])
            .domain(data.map(d => d.species))
            .paddingInner(1)
            .paddingOuter(.5)

        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .attr("fill", "wheat")
            .call(d3.axisBottom(x))

        // rotate the labels
        svg.selectAll("text")
            .attr("transform", "translate(-10,0)rotate(-45)")
            .style("text-anchor", "end")

        // Show the Y scale
        var y = d3.scaleLinear()
            .domain([0, 180])
            .range([height, margin.top])

        svg.append("g")
            .attr("fill", "wheat")
            .attr("transform", `translate(${margin.left}, 0)`)
            .call(d3.axisLeft(y))


        // Show the main vertical line
        svg.selectAll("vertLines")
            .data(allBoxes)
            .enter()
            .append("line")
            .attr("x1", d => x(d.species))
            .attr("x2", d => x(d.species))
            .attr("y1", d => y(d.min))
            .attr("y2", d => y(d.max))
            .attr("stroke", "black")
            .style("width", 20)

        // add horizontal at the max and min line
        svg.selectAll("minLines")
            .data(allBoxes)
            .enter()
            .append("line")
            .attr("x1", d => x(d.species) - 20 / 2)
            .attr("x2", d => x(d.species) + 20 / 2)
            .attr("y1", d => y(d.min))
            .attr("y2", d => y(d.min))
            .attr("stroke", "black")
            .style("width", 20)

        svg.selectAll("maxLines")
            .data(allBoxes)
            .enter()
            .append("line")
            .attr("x1", d => x(d.species) - 20 / 2)
            .attr("x2", d => x(d.species) + 20 / 2)
            .attr("y1", d => y(d.max))
            .attr("y2", d => y(d.max))
            .attr("stroke", "black")
            .style("width", 20)

        //color for boxes
        let color = d3.scaleOrdinal(d3.schemeCategory10)

        // rectangle for the main box
        var boxWidth = 50
        svg.selectAll("boxes")
            .data(allBoxes)
            .enter()
            .append("rect")
            .attr("x", d => x(d.species) - boxWidth / 2)
            .attr("y", d => y(d.q3))
            .attr("height", d => y(d.q1) - y(d.q3))
            .attr("width", boxWidth)
            .attr("stroke", "black")
            .style("fill", d => color(d.species))
            .style("opacity", 0.85)

        // Show the median
        svg.selectAll("medianLines")
            .data(allBoxes)
            .enter()
            .append("line")
            .attr("x1", d => x(d.species) - boxWidth / 2)
            .attr("x2", d => x(d.species) + boxWidth / 2)
            .attr("y1", d => y(d.median))
            .attr("y2", d => y(d.median))
            .attr("stroke", "black")
            .style("width", 50)
            .style("stroke-width", 3)
            

        // Add individual points with jitter
        var jitterWidth = 50
        
        let individual_points = []
        data.forEach(d => {
            d.heights.forEach(h => {
                individual_points.push({ species: d.species, height: h })
            })
        })

        svg.selectAll("indPoints")
            .data(individual_points)
            .enter()
            .append("circle")
            .attr("cx", d => x(d.species) - jitterWidth / 2 + Math.random() * jitterWidth)
            .attr("cy", d => y(d.height))
            .attr("r", 4)
            .attr("stroke", "white")
            .attr("stroke-width", 0.75)
            .style("fill", d => color(d.species))

        //Add tittle
        svg.append("text")
            .attr("x", width / 2 + margin.left - 50)
            .attr("y", margin.top - 80)
            .attr("text-anchor", "middle")
            .attr("fill", "wheat")
            .style("font-size", "1.25em")
            .text(`Boxplot of Heights of Top 10 Species by Count`);


        // add hover data on boxes
        const tooltip = d3.select("body")
            .append("div")
            .style("position", "absolute")
            .style("background-color", "wheat")
            .style("color", "#364e51")
            .style("border-radius", "5px")
            .style("padding", "10px")
            .style("opacity", 0);

        svg.selectAll("rect")
            .on("mouseover", function (event, d) {
                tooltip
                    .style("opacity", 1)
                d3.select(this)
                    .style("stroke", "black")
                    .style("opacity", 1)

                tooltip
                    .html(`Species: ${d.species} <br/>
                            Min: ${d.min} <br/>
                            Q1: ${d.q1} <br/>
                            Median: ${d.median} <br/>
                            Q3: ${d.q3} <br/>
                            Max: ${d.max} <br/>`)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 10) + "px")
                
            })
            .on("mouseout", function (event, d) {
                tooltip
                    .style("opacity", 0)
                d3.select(this)
                    .style("stroke", "black")
                    .style("opacity", 0.85)
            })




    }

    function bubblechart_filter(data, n) {

        //filter all the data with height and diameter != null
        data = data.filter(d => d.mean_height !== null && d.mean_diameter !== null);

        // group by species put inside compute the mean of height and diameter and the sum of count
        let species = d3.group(data, d => d.scientific_name)
        species.forEach((value, key, map) => {
            map.set(key, {
                mean_height: d3.mean(value, d => d.mean_height),
                mean_diameter: d3.mean(value, d => d.mean_diameter),
                count: d3.sum(value, d => d.count),
                species: key
            })
        })

        // take the top 100 species by count
        let top_species = data.reduce((acc, cur) => {
            acc[cur.scientific_name] = (acc[cur.scientific_name] || 0) + cur.count;
            return acc;
        }, {});
        top_species = Object.keys(top_species).sort((a, b) => top_species[b] - top_species[a]).slice(0, n);
        species = new Map([...species.entries()].filter(([k, v]) => top_species.includes(k)));


        
        return species;
    }

    function bubblechart_chart() {
        let data = bubblechart_filter(data_file, 100);

        //bubble chart
        const margin = { top: 100, right: 200, bottom: 100, left: 100 };
        const width = 1400 - margin.left - margin.right;
        const height = 700 - margin.top - margin.bottom;

        const svg = d3.select('#bubble-chart')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .attr('style', 'color: wheat')

        // Add X axis
        var x = d3.scaleLinear()
            .domain([0, d3.max(data.values(), d => d.mean_diameter)])
            .range([margin.left, width])

        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .attr("fill", "wheat")
            .call(d3.axisBottom(x))

        // Add Y axis
        var y = d3.scaleLinear()
            .domain([0, d3.max(data.values(), d => d.mean_height)])
            .range([height, margin.top])

        svg.append("g")
            .attr("fill", "wheat")
            .attr("transform", `translate(${margin.left}, 0)`)
            .call(d3.axisLeft(y))
        
         // add x title
        svg.append("text")
            .attr("x", width / 2 + margin.left - 50)
            .attr("y", height + 50)
            .attr("text-anchor", "middle")
            .attr("fill", "wheat")
            .style("font-size", "1em")
            .text(`Mean Diameter`);

        // add y title
        svg.append("text")
            .attr("x", -height / 2 - 50)
            .attr("y", margin.left - 50)
            .attr("text-anchor", "middle")
            .attr("fill", "wheat")
            .style("font-size", "1em")
            .text(`Mean Height`)
            .attr("transform", "rotate(-90)");

        // Add a scale for bubble size

        var z = d3.scaleLinear()
            .domain([0, d3.max(data.values(), d => d.count)])
            .range([1, 40]);


        
        let species = []
        data.forEach((value, key, map) => {
            species.push(value.species)
        })

        var color = d3.scaleOrdinal()
            .domain(species)
            .range([    
                '#ff5555', '#5599ff', '#66ff66', '#cc66cc', '#ff9933', '#ffff66',
                '#cc7733', '#ff99ff', '#aaaaaa', '#bbddff', '#3399ff', '#ccff99',
                '#dd99dd', '#ffcc88', '#ffffcc', '#ff9933', '#ffcc88', '#cc7744',
                '#aaddcc', '#ffffcc', '#d0d0da', '#ff9999', '#aaddee', '#ffcc66',
                '#55aa55', '#ccffcc', '#ffbbdd', '#ccff55', '#3344dd', '#ffddbb',
                '#ff5555', '#5599ff', '#66ff66', '#cc66cc', '#ff9933', '#ffff66',
                '#cc7733', '#ff99ff', '#aaaaaa', '#bbddff', '#3399ff', '#ccff99',
            ]);

        svg.append('g')
            .selectAll("dot")
            .data(data.entries())
            .enter()
            .append("circle")
            .attr("cx", d => x(d[1].mean_diameter))
            .attr("cy", d => y(d[1].mean_height))
            .attr("r", d => z(d[1].count))
            .style("fill", d => color(d[1].species))
            .style("opacity", "0.7")
            .attr("stroke", "white")
            .style("stroke-width", "2px")
            .attr("stroke-opacity", "0.7")

        // add tooltip
        const tooltip = d3.select("body")
            .append("div")
            .style("position", "absolute")
            .style("background-color", "wheat")
            .style("color", "#364e51")
            .style("border-radius", "5px")
            .style("padding", "10px")
            .style("opacity", 0);

        svg.selectAll("circle")
            .on("mouseover", function (event, d) {
                tooltip
                    .style("opacity", 1)
                d3.select(this)
                    .style("stroke", "black")
                    .style("opacity", 1)

                tooltip
                    .html(`Species: ${d[1].species} <br/>
                            Mean Height: ${d[1].mean_height} <br/>
                            Mean Diameter: ${d[1].mean_diameter} <br/>
                            Count: ${d[1].count} <br/>`)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 10) + "px")
                
            })
            .on("mouseout", function (event, d) {
                tooltip
                    .style("opacity", 0)
                d3.select(this)
                    .style("stroke", "white")
                    .style("opacity", 0.7)
            })

        // add title
        svg.append("text")
            .attr("x", width / 2 + margin.left - 50)
            .attr("y", margin.top - 80)
            .attr("text-anchor", "middle")
            .attr("fill", "wheat")
            .style("font-size", "1.25em")
            .text(`Bubble Chart of Top 100 Species`);

    }

    function scatterchart_filter(data) {

        //filter all the data with height and diameter != null
        data = data.filter(d => d.mean_height !== null && d.mean_diameter !== null);

        // group by species and put inside all the heights and diameters and the sum of count
        let species = d3.group(data, d => d.scientific_name)
        species.forEach((value, key, map) => {
            map.set(key, {
                heights: value.map(d => d.mean_height),
                diameters: value.map(d => d.mean_diameter),
                count: d3.sum(value, d => d.count),
                species: key
            })
        })

        // sort by count
        species = new Map([...species.entries()].sort((a, b) => b[1].count - a[1].count));

        return species;
    }

    function scatterchart_chart(n) {

        let data = scatterchart_filter(data_file);

        //scatter chart
        const margin = { top: 100, right: 200, bottom: 100, left: 100 };
        const width = 1400 - margin.left - margin.right;
        const height = 800 - margin.top - margin.bottom;

        const svg = d3.select('#scatter-chart')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .attr('style', 'color: wheat')

        // plot 6 scatter plot for the top 6 species in separate graphs each for a species
        let species = []
        data.forEach((value, key, map) => {
            species.push(value.species)
        })

        species = species.slice(0, n)

        let color = d3.scaleOrdinal(d3.schemeCategory10)


        // divide the svg according to n, max 6 divided in 2 rows and 3 columns
        const n_w = Math.min(n, 3)
        const n_h = Math.ceil(n / 3)


        species.forEach((s, i) => {
            let data_s = data.get(s)
            
            document.getElementById('scatter-chart').innerHTML += `<g id="scatter-chart-${i}"></g>`
            let svg_s = d3.select(`#scatter-chart-${i}`)
                .attr('width', width/n_w)
                .attr('height', height/n_h)
                .attr('style', 'color: wheat')
                .attr("transform", `translate(${width/n_w * (i%n_w)}, ${height/n_h * (i%n_h)})`)
            
            // Add X axis
            var x = d3.scaleLinear()
                .domain([0, d3.max(data_s.diameters)])
                .range([margin.left, width/n_w])

            svg_s.append("g")
                .attr("transform", "translate(0," + height/n_h + ")")
                .attr("fill", "wheat")
                .call(d3.axisBottom(x))

            // Add Y axis
            var y = d3.scaleLinear()
                .domain([0, d3.max(data_s.heights)])
                .range([height/n_h, margin.top])

            svg_s.append("g")
                .attr("fill", "wheat")
                .attr("transform", `translate(${margin.left}, 0)`)
                .call(d3.axisLeft(y))

            // plot the data
            svg_s.append('g')
                .selectAll("dot")
                .data(data_s.heights.map((d, i) => [d, data_s.diameters[i]]))
                .enter()
                .append("circle")
                .attr("cx", d => x(d[1]))
                .attr("cy", d => y(d[0]))
                .attr("r", 8)
                .attr("stroke", "white")
                .attr("stroke-width", 0.75)
                .style("fill", color(s))
                .attr("class", "scatter-chart-dot")

            // Add title of species
            svg_s.append("text")
                .attr("x", width / n_w / 2 + 50)
                .attr("y", margin.top - 40)
                .attr("text-anchor", "middle")
                .attr("fill", "wheat")
                .style("font-size", "1em")
                .text(`${s}`);
            

        })



    }


    let rendered = false;
    onMount(() => {
        rendered = true;
    });

    let n_state = 3;
    let n_city = 5;
    let n_species = 3;
    let n_scatter_plot = 6;
    
    $: if (rendered) {
        //clear chart
        d3.select('#alluvion-chart').selectAll('*').remove();
        alluvion_chart(n_state, n_city, n_species);
        
        d3.select('#box-plot').selectAll('*').remove();
        boxplot_chart();

        d3.select('#bubble-chart').selectAll('*').remove();
        bubblechart_chart();

        d3.select('#scatter-chart').selectAll('*').remove();
        scatterchart_chart(n_scatter_plot);
    }

    

</script>

<div class="assignment2">

    <div class="backhome">
        <a href="/"> &#x2190 Home </a>
    </div>

    <section class="section1">

        <div class="chart">
            <svg id="alluvion-chart" />
        </div>

        <div class="alluvion-inputs">

            <p> 
                Here we can see an alluvion chart that represents has as nodes: states, cities and species, 
                which can be controlled from the buttons below, it is advisable not to increase the categories 
                too much together otherwise the chart will not be able to support them, however a maximum of 10
                has been inserted which should ensure a clear view of the chart most of the time. 
                <br/> <br/>
                By hovering the mouse over the links in the graph, you can see the number of trees belonging to each path.
                In addition the links will be highlighted when hovering over the mouse.
                <br/> <br/>
                By hovering the mouse over the boxes you can see the name of the category and also the links that pass through it will
                be highlighted.
                <br/> <br/>
                The colours have been chosen to highlight the path from source to target so that it can be easily followed.
                The species have been grouped by family, so that the chart is not too cluttered.
            </p>

            <label for="n_state">Number of states: {n_state} </label>
            <input type="range" bind:value={n_state} min="1" max="10" step="1" />
            <br />
            <label for="n_city">Number of cities {n_city} </label>
            <input type="range" bind:value={n_city} min="1" max="10" step="1" />
            <br />
            <label for="n_species">Number of species {n_species} </label>
            <input type="range" bind:value={n_species} min="1" max="10" step="1" />
        </div>

    </section>

    <section class="section2">

        <div class="chart">
            <svg id="box-plot" />
        </div>

        <div class="box-plot-description">
            <p> Here you can see a boxplot representing the heights of the top 10 species per count within our dataset, 
                first the species that did not have the average height were filtered out and then I removed the heights == 0 
                from each individual species, this is because in the case of newly-born trees I did not want them to be considered.
                
                <br> <br>
                Hovering over the mouse you can see the various statistics such as Q1/3, min and max, species and median.
            </p>
        </div>

    </section>

    <section class="section3">

        <div class="chart">
            <svg id="bubble-chart"></svg>
        </div>

        <div class="bubble-chart-description">
            <p> Here you can see a bubble chart representing the mean height and diameter of the top 100 species by count, 
                the size of the bubble represents the number of trees belonging to that species, 
                the colour instead represents the species itself.
                <br> <br>
                Hovering over the mouse you can see the various statistics such as mean height and diameter, count and species.
            </p>

    </section>

    <section class="section4">

        <div class="chart">
            <svg id="scatter-chart" />
        </div>



        <div class="scatter-chart-description">
            <p> Here you can see a scatter chart representing the mean height and diameter of the top {n_scatter_plot} species by count, 
                the size of the bubble represents the number of trees belonging to that species, 
                the colour instead represents the species itself.
                <br> <br>
                Hovering over the mouse you can see the various statistics such as mean height and diameter, count and species.
            </p>

            <label for="n_scatter_plot">Number of species: {n_scatter_plot} </label>
            <input type="range" bind:value={n_scatter_plot} min="1" max="6" step="1" />

        </div>

    </section>
</div>

<style>

    .assignment2 {
        width: 100vw;
        height: max-content;
        background-color: #364e51;
        color: wheat;
        display: flex;
        flex-direction: column;
        align-items: center;

        overflow: hidden;
    }

    .backhome {
        position: fixed;
        top: 2rem;
        left: 2rem;
    }

    .backhome a {
        font-size: 1.5em;
    }

    .chart {
        display: block;
        position: relative;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .alluvion-inputs {
        position: absolute;
        top: 5rem;
        right: 8rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .alluvion-inputs p {
        width: 20rem;
        margin-bottom: 5rem;
    }

    .alluvion-inputs input {
        width: 20rem;
        margin-bottom: 2rem;
        accent-color: wheat;
    }

    .section1 {
        top: 10rem;
    }

    #alluvion-chart {
        margin-right: 30rem;
    }

    section {
        position: relative;
    }

    @media screen and (max-width: 1700px) {

        .alluvion-inputs {
            position: relative;
            top: 0;
            right: 0;
            margin-top: 2rem;
            margin-right: 0;
        }

        .alluvion-inputs p {
            width: 60%;
        }

        .section1 {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        

        #alluvion-chart {
            margin-right: 0;
            width: auto;
        }
    }


    .section2 {
        display: block;
        position: relative;
        width: 100%;
        height: 100%;
        margin-top: 20rem;
    }

    #box-plot {
        margin-right: 30rem;
    }

    .box-plot-description {
        position: absolute;
        top: 10rem;
        right: 15rem;
        width: 20rem;
    }

    .box-plot-description p {
        width: 20rem;
        margin-bottom: 5rem;
    }

    @media screen and (max-width: 1700px) {

        .box-plot-description {
            position: relative;
            top: 0;
            right: 0;
            margin-top: 2rem;
            margin-right: 0;
            width: 80%;
        }

        .box-plot-description p {
            width: 100%;
        }

        .section2 {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        

        #box-plot {
            margin: 0;
            width: 75%;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
    }


    .section3 {
        display: block;
        position: relative;
        width: 100%;
        height: 100%;
        margin-top: 10rem;
    }

    #bubble-chart {
        margin-right: 30rem;
    }

    .bubble-chart-description {
        position: absolute;
        top: 10rem;
        right: 15rem;
        width: 20rem;
    }


    .bubble-chart-description p {
        width: 20rem;
        margin-bottom: 5rem;
    }

    @media screen and (max-width: 1700px) {

        .bubble-chart-description {
            position: relative;
            top: 0;
            right: 0;
            margin-top: 2rem;
            margin-right: 0;
            width: 80%;
        }

        .bubble-chart-description p {
            width: 100%;
        }

        .section3 {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        

        #bubble-chart {
            margin: 0;
            margin-inline: 5%;
            width: 75%;
        }
    }

    .section4 {
        display: block;
        position: relative;
        width: 100%;
        height: 100%;
        margin-top: 10rem;
    }

    #scatter-chart {
        margin-right: 30rem;
    }

    .scatter-chart-description {
        position: absolute;
        top: 10rem;
        right: 15rem;
        width: 20rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .scatter-chart-description p {
        margin-bottom: 5rem;
    }

    .scatter-chart-description input {
        width: 20rem;
        margin-bottom: 2rem;
        accent-color: wheat;
    }


    @media screen and (max-width: 1700px) {

        .scatter-chart-description {
            position: relative;
            top: 0;
            right: 0;
            margin-top: 2rem;
            margin-right: 0;
            width: 80%;
        }

        .scatter-chart-description p {
            width: 100%;
        }

        .section4 {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        

        #scatter-chart {
            margin: 0;
            margin-inline: 5%;
            width: 75%;
        }
    }

</style>