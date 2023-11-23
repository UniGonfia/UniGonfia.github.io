<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    import 'iconify-icon'
    import data_file from '$lib/data/assignment3.json'


    let months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"];
    let years = [2020, 2010, 2000, 1990, 1980, 1970, 1960, 1950, 1940, 1930]

    const color = d3.scaleOrdinal()
        .domain(years)
        .range(d3.schemeCategory10);
    /*
    Data is like:
    {
        city: Alabama,
        2002: {
            jan: {
                min: value
                avg: value
                max: value
            },
            feb: {
                min: value
                avg: value
                max: value
            }, ...
        },
        2003: ... 
    } ...
    */

    let n_year = 1;

    $: options = {
        chart: "line",
        state: "Alabama",
        year: [2020]
    }

    let rendered = false;
    onMount(() => {

        rendered = true;

        
        //fill the select with the states
        let states = Object.keys(data_file);
        let select = document.getElementById("states");
        states.forEach(state => {
            let option = document.createElement("option");
            option.value = state;
            option.text = state;
            select.appendChild(option);
        });

        //firsth graph
        options = {
            chart: "ridge",
            state: "Alabama",
            year: [2020]
        }

        setup_chart(options);
    })

    function options_change(chart) {
        let select = document.getElementById("states");
        options.state = select.value;

        let slider = document.getElementById("year");
        let years_array = [];
        for (let i = 0; i < slider.value; i++) {
            years_array.push(years[i]);
        }
        options.year = years_array;
        n_year = slider.value;

        if (chart == "line" || chart == "polar" || chart == "ridge") {
            options.chart = chart;
        }

    }

    function setup_chart(options) {
        d3.select("#chart").selectAll("*").remove();

        if (options.chart == "line") {
            document.getElementById("yearlabel").style.display = "block";
            document.getElementById("year").style.display = "block";
            line_chart(data_file, options.state, options.year);
        } else if (options.chart == "polar") {
            document.getElementById("yearlabel").style.display = "block";
            document.getElementById("year").style.display = "block";
            polar_chart(data_file, options.state, options.year);
        } else if (options.chart == "ridge") {
            document.getElementById("yearlabel").style.display = "none";
            document.getElementById("year").style.display = "none";
            ridge_chart(data_file, options.state);
        }
    }

    $: if (rendered && options) {
        setup_chart(options);
    }

    function line_chart(data, state, years_array) {

        let margin = {top: 150, right: 100, bottom: 30, left: 100};
        let width = 1500 - margin.left - margin.right;
        let height = 800 - margin.top - margin.bottom;

        const svg = d3.select("#chart")
            .attr('width', width)
            .attr('height', height)
            .attr("viewBox", [0, 0, width + margin.left + margin.right, height + margin.top + margin.bottom])
            .attr("style", "max-width: 100%;");

            
        const x = d3.scaleBand()
            .rangeRound([0, width])
            .padding(0.1)
            .domain(months);

        const y = d3.scaleLinear()
            .rangeRound([height, 0])
            .domain([d3.min(months, (d) => d3.min(years_array, (y) => data[state][y][d].min - 5)), d3.max(months, (d) => d3.max(years_array, (y) => data[state][y][d].max))]);

        svg.append("g")
            .style("color", "wheat")
            .attr("transform", `translate(${margin.left}, ${margin.top})`)
            .call(d3.axisLeft(y));
        
        svg.append("g")
            .style("color", "wheat")
            .attr("transform", `translate(${margin.left}, ${height + margin.top})`)
            .call(d3.axisBottom(x));

        //plot max and min temperature as lines and avg as scatter for each month
        for (let year of years_array) {
            let data_state = data[state];
            let data_year = data_state[year];

            //draw max line animate
            svg.append("path")
                .datum(months)
                .attr("fill", "none")
                .attr("stroke", years_array.length > 1 ? color(year) : "red")
                .attr("stroke-width", 2)
                .attr("d", d3.line()
                    .x((d) => x(d) + margin.left + x.bandwidth() / 2)
                    .y((d) => y(data_year[d].max) + margin.top)
                )
                .attr("stroke-dasharray", function() { return this.getTotalLength() })
                .attr("stroke-dashoffset", function() { return this.getTotalLength() })
                .transition()
                    .duration(1000)
                    .attr("stroke-dashoffset", 0);

            //draw min line animate
            svg.append("path")
                .datum(months)
                .attr("fill", "none")
                .attr("stroke", years_array.length > 1 ? color(year) : "blue")
                .attr("stroke-width", 2)
                .attr("d", d3.line()
                    .x((d) => x(d) + margin.left + x.bandwidth() / 2)
                    .y((d) => y(data_year[d].min) + margin.top)
                )
                .attr("stroke-dasharray", function() { return this.getTotalLength() })
                .attr("stroke-dashoffset", function() { return this.getTotalLength() })
                .transition()
                    .duration(1000)
                    .attr("stroke-dashoffset", 0);

            //draw avg scatter animate
            svg.append("g")
                .selectAll("dot")
                .data(months)
                .enter()
                .append("circle")
                    .attr("cx", (d) => x(d) + margin.left + x.bandwidth() / 2)
                    .attr("cy", (d) => y(data_year[d].avg) + margin.top)
                    .attr("r", 5)
                    .attr("fill", years_array.length > 1 ? color(year) : "white")
                    .attr("opacity", 0)
                    .transition()
                        .delay(250)
                        .duration(1000)
                        .attr("opacity", 1);

                if (years_array.length > 1) {
                    //legend
                    svg.append("circle")
                                    .attr("cx", width + margin.left - 50)
                                    .attr("cy", 60 + years_array.indexOf(year) * 30)
                                    .attr("r", 6)
                                    .style("fill", color(year));
                    
                    svg.append("text")
                        .attr("x", width + margin.left - 40)
                        .attr("y", 65 + years_array.indexOf(year) * 30)
                        .text(year)
                        .style("font-size", "15px")
                        .attr("alignment-baseline","middle")
                        .style("fill", "wheat");
                }
        }


        //title
        svg.append("text")
            .attr("x", width / 2 + margin.left)
            .attr("y", 20)
            .text(`Temperature in ${state} from ${years_array[0]} to ${years_array[years_array.length - 1]}`)
            .style("font-size", "28px")
            .attr("text-anchor", "middle")
            .style("fill", "wheat");
    }

    function polar_chart(data, state, years_array) {

        let margin = {top: 200, right: 100, bottom: 200, left: 100};
        let width = 375 - margin.left - margin.right;
        let height = 200 - margin.top - margin.bottom;

        const svg = d3.select("#chart")
            .attr('width', width)
            .attr('height', height)
            .attr("viewBox", [0, 0, width + margin.left + margin.right, height + margin.top + margin.bottom])
            .attr("style", "max-width: 100%;");


        //draw the polar chart
        let polar = svg.append("g")
            .attr("transform", `translate(${width / 2 + margin.left}, ${height / 2 + margin.top})`);

        //draw the circles and axis and labels of month and temperature
        let r = d3.scaleLinear()
            .domain([d3.min(months, (d) => d3.min(years_array, (y) => data[state][y][d].min - 10)), d3.max(months, (d) => d3.max(years_array, (y) => data[state][y][d].max + 20))])
            .range([0, width / 2]);
        
        let t = d3.scaleLinear()
            .domain([0, 12])
            .range([0, 2 * Math.PI]);


        //draw the circles
        polar.selectAll("circle")
            .data(r.ticks(5).slice(1))
            .enter()
            .append("circle")
                .attr("fill", "none")
                .attr("stroke", "wheat")
                .attr("stroke-width", 0.5)
                .attr("r", (d) => r(d));

        //draw the axis
        polar.append("g")
            .selectAll("circle")
            .data(months)
            .enter()
            .append("line")
                .attr("x1", 0)
                .attr("y1", 0)
                .attr("x2", (d, i) => r(d3.max(months, (d) => d3.max(years_array, (y) => data[state][y][d].max + 20))) * Math.cos(t(i) - Math.PI / 2))
                .attr("y2", (d, i) => r(d3.max(months, (d) => d3.max(years_array, (y) => data[state][y][d].max + 20))) * Math.sin(t(i) - Math.PI / 2))
                .attr("stroke", "wheat")
                .attr("stroke-width", 0.5);

        //draw the labels of the months
        polar.append("g")
            .selectAll("circle")
            .data(months)
            .enter()
            .append("text")
                .attr("x", (d, i) => r(d3.max(months, (d) => d3.max(years_array, (y) => data[state][y][d].max + 20))) * Math.cos(t(i) - Math.PI / 2))
                .attr("y", (d, i) => r(d3.max(months, (d) => d3.max(years_array, (y) => data[state][y][d].max + 20))) * Math.sin(t(i) - Math.PI / 2))
                .text((d) => d.toUpperCase())
                .style("font-size", "8px")
                .attr("alignment-baseline","middle")
                .attr("text-anchor", "middle")
                .attr("transform", (d, i) => "translate(" + 10 * Math.cos(t(i) - Math.PI / 2) + ", " + 10 * Math.sin(t(i) - Math.PI / 2) + ")")
                .style("fill", "wheat");

        
        //draw the labels of the temperature
        polar.append("g")
            .selectAll("circle")
            .data(r.ticks(5).slice(1))
            .enter()
            .append("text")
                .attr("x", 0)
                .attr("y", (d) => -r(d))
                .text((d) => d + "°F")
                .style("font-size", "5px")
                .attr("alignment-baseline","middle")
                .attr("text-anchor", "middle")
                .style("fill", "wheat");
        
        //draw the circles with the temperature, if the year == 1 draw max and min and avg, else draw only avg for each year
        for (let year of years_array) {
            let data_state = data[state];
            let data_year = data_state[year];


            let line = d3.lineRadial()
                .angle((d, i) => t(i))
                .radius((d) => r(d));


            if (years_array.length > 1) {
                //draw the line
                polar.append("path")
                    .datum(months.map((d) => data_year[d].avg).concat(data_year[months[0]].avg))
                    .attr("fill", "none")
                    .attr("stroke", color(year))
                    .attr("stroke-width", 0.75)
                    .attr("d", line)
                    .attr("stroke-dasharray", function() { return this.getTotalLength() })
                    .attr("stroke-dashoffset", function() { return this.getTotalLength() })
                    .transition()
                        .duration(1000)
                        .attr("stroke-dashoffset", 0);

            } else {
                //draw the line animate
                polar.append("path")
                    .datum(months.map((d) => data_year[d].max).concat(data_year[months[0]].max))
                    .attr("fill", "none")
                    .attr("stroke", "red")
                    .attr("stroke-width", 0.75)
                    .attr("d", line)
                    .attr("stroke-dasharray", function() { return this.getTotalLength() })
                    .attr("stroke-dashoffset", function() { return this.getTotalLength() })
                    .transition()
                        .duration(1000)
                        .attr("stroke-dashoffset", 0);

                polar.append("path")
                    .datum(months.map((d) => data_year[d].min).concat(data_year[months[0]].min))
                    .attr("fill", "none")
                    .attr("stroke", "blue")
                    .attr("stroke-width", 0.75)
                    .attr("d", line)
                    .attr("stroke-dasharray", function() { return this.getTotalLength() })
                    .attr("stroke-dashoffset", function() { return this.getTotalLength() })
                    .transition()
                        .duration(1000)
                        .attr("stroke-dashoffset", 0);

                polar.append("path")
                    .datum(months.map((d) => data_year[d].avg).concat(data_year[months[0]].avg))
                    .attr("fill", "none")
                    .attr("stroke", "white")
                    .attr("stroke-width", 0.75)
                    .attr("d", line)
                    .attr("stroke-dasharray", function() { return this.getTotalLength() })
                    .attr("stroke-dashoffset", function() { return this.getTotalLength() })
                    .transition()
                        .duration(1000)
                        .attr("stroke-dashoffset", 0);
            }

        }

        //legend
        if (years_array.length > 1) {
            for (let year of years_array) {
                polar.append("circle")
                    .attr("cx", width - 40)
                    .attr("cy", years_array.indexOf(year) * 10)
                    .attr("r", 3)
                    .style("fill", color(year));
                
                polar.append("text")
                    .attr("x", width - 35)
                    .attr("y", 2 + years_array.indexOf(year) * 10)
                    .text(year)
                    .style("font-size", "5px")
                    .attr("alignment-baseline","middle")
                    .style("fill", "wheat");

                
            }
        }


    }

    function ridge_chart(data, state) {
        
        let margin = {top: 150, right: 50, bottom: 50, left: 50};
        let width = 1800 - margin.left - margin.right;
        let height = 1300 - margin.top - margin.bottom;

        const svg = d3.select("#chart")
            .attr('width', width)
            .attr('height', height)
            .attr("viewBox", [0, 0, width + margin.left + margin.right, height + margin.top + margin.bottom])
            .attr("style", "max-width: 100%;");

        //max temperatures for each year
        let max_temps = [];
        let min_temps = [];
        for (let year of years) {
            let data_state = data[state];
            let data_year = data_state[year];
            
            let year_max = []
            let year_min = []
            for (let month of months) {
                year_max.push(data_year[month].max);
                year_min.push(data_year[month].min);
            }

            max_temps.push({
                year: year,
                max: year_max,
            });

            min_temps.push({
                year: year,
                min: year_min,
            });
        }
        
        const x = d3.scaleLinear()
            .domain([d3.min(min_temps, (d) => d3.min(d.min)), d3.max(max_temps, (d) => d3.max(d.max))])
            .range([margin.left, width]);

        const y = d3.scaleLinear()
            .domain([0, 0.4])
            .range([height, 0]);
        
        const yName = d3.scaleBand()
            .domain(years)
            .range([margin.top, height])
            .padding(0.1);

        
        svg.append("g")
            .style("color", "wheat")
            .attr("transform", `translate(${margin.left}, ${margin.top})`)
            .call(d3.axisLeft(yName));

        svg.append("g")
            .style("color", "wheat")
            .attr("transform", `translate(0, ${height + margin.top})`)
            .call(d3.axisBottom(x));

        //increase font size
        svg.selectAll("text")
            .style("font-size", "25px");

        const kde = kernelDensityEstimator(kernelEpanechnikov(3), x.ticks(40));
        const maxDensity = [];
        for (let i = 0; i < years.length; i++) {
            let data_year = max_temps[i].max;
            let density = kde(data_year);
            maxDensity.push({
                year: years[i],
                density: density
            });
        }

        const minDensity = [];
        for (let i = 0; i < years.length; i++) {
            let data_year = min_temps[i].min;
            let density = kde(data_year);
            minDensity.push({
                year: years[i],
                density: density
            });
        }

        let area_max = d3.area()
            .curve(d3.curveBasis)
            .x((d) => x(d[0]))
            .y0(height)
            .y1((d) => y(d[1]));

        let area_min = d3.area()
            .curve(d3.curveBasis)
            .x((d) => x(d[0]))
            .y0(height)
            .y1((d) => y(d[1]));

        //draw the max and fill the area under the curve
        svg.selectAll("areas")
            .data(maxDensity)
            .enter()
            .append("path")
                .attr("transform", (d) => `translate(0, ${yName(d.year) - height + margin.top + 45})`)    
                .datum((d) => d.density)
                .attr("fill", "red")
                .attr("opacity", 0.6)
                .attr("stroke", "white")
                .attr("stroke-width", 1)
                .attr("d", d3.line()
                    .curve(d3.curveBasis)
                )
                .attr("d", area_max);

        
        //draw the min and fill the area under the curve
        svg.selectAll("areas")
            .data(minDensity)
            .enter()
            .append("path")
                .attr("transform", (d) => `translate(0, ${yName(d.year) - height + margin.top  + 45})`)    
                .datum((d) => d.density)
                .attr("fill", "blue")
                .attr("opacity", 0.6)
                .attr("stroke", "white")
                .attr("stroke-width", 1)
                .attr("d", d3.line()
                    .curve(d3.curveBasis)
                )
                .attr("d", area_min);
        
        
    }

    // This is what I need to compute kernel density estimation
    function kernelDensityEstimator(kernel, X) {
    return function(V) {
        return X.map(function(x) {
        return [x, d3.mean(V, function(v) { return kernel(x - v); })];
        });
    };
    }
    function kernelEpanechnikov(k) {
    return function(v) {
        return Math.abs(v /= k) <= 1 ? 0.75 * (1 - v * v) / k : 0;
    };
    }

</script>



<div class="assignment3">

    <div class="backhome">
        <a href="/"> &#x2190 Home </a>
    </div>

    <nav class="chart-buttons">
        <ul>
            <li> <button on:click|preventDefault={() => options_change("line")}> <iconify-icon class="icon" icon="ph:chart-line" width="100%" /> </button> </li>
            <li> <button on:click|preventDefault={() => options_change("polar")}> <iconify-icon class="icon" icon="ph:chart-polar-light" width="100%"/> </button> </li>
            <li> <button on:click|preventDefault={() => options_change("ridge")}> <iconify-icon class="icon" icon="material-symbols:area-chart-rounded" width="100%"/> </button> </li>
        </ul>
    </nav>

    <svg id="chart" class="chart"></svg>

    <div class="tools">

        <label for="states"> State: </label>
        <select on:change={options_change} id="states"></select>

        <label for="year" id="yearlabel"> Number of years: {n_year} </label>
        <input on:change={options_change} type="range" id="year" min="1" max="10" step="1" value="1">
        
        <p class="description">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Quam blanditiis quas expedita, dolores modi ipsam similique ab temporibus 
            impedit illo fuga neque itaque, nostrum eveniet ullam accusamus voluptatibus pariatur delectus? Laboriosam enim repellendus quasi 
            quisquam at recusandae voluptas, officiis doloribus?
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Minus, veniam.
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Ullam impedit sunt quo eveniet quae aliquid blanditiis excepturi suscipit delectus voluptatum!
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Rem, deleniti?
        </p>

    </div>

</div>


<style>

    .assignment3 {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        height: 100vh;
        background-color: #364e51;
        gap: 1rem;
        overflow: hidden;
        flex-wrap:wrap;

    }

    .backhome {
        position: absolute;
        top: 2rem;
        left: 2rem;
    }

    .backhome a {
        font-size: 1.5em;
    }

    .chart-buttons {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 5%;
    }

    .chart-buttons ul {
        list-style: none;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    .chart-buttons li {
        margin: 0.5rem;
    }

    .chart-buttons button {
        width: 80px;
        height: 80px;
        border: none;
        background-color: transparent;
    }

    .icon {
        background-color: wheat;
        border: 3px solid black;
        border-radius: 1rem;
    }

    .icon:hover {
        border: 5px solid black;
    }

    .chart {
        display: flex;
        width: 70%;
        height: 80%;
    }

    .tools {
        width: 20%;
        height: 60%;
        display: flex;
        flex-direction: column;
        color: wheat;
        justify-content: center;
        align-items: center;
        gap: 1rem;
    }

    .tools select {
        width: 80%;
        height: 2rem;
        border: none;
        border-radius: 0.5rem;
        background-color: wheat;
        color: black;
        text-align: center;
    }

    .tools input {
        width: 80%;
        height: 2rem;
        border: none;
        border-radius: 0.5rem;
        background-color: wheat;
        color: black;
        accent-color: wheat;
    }

    .tools p {
        width: 80%;
        text-align: justify;
    }


</style>