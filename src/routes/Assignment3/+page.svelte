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
        year: 2020
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
            chart: "line",
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

        if (chart == "line" || chart == "polar" || chart == "bridge") {
            options.chart = chart;
        }
    }

    function setup_chart(options) {
        d3.select("#chart").selectAll("*").remove();

        if (options.chart == "line") {
            line_chart(data_file, options.state, options.year);
        } else if (options.chart == "polar") {
            polar_chart(data_file, options.state, options.year);
        } else if (options.chart == "bridge") {
            bridge_chart(data_file, options.state);
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

            //title
            svg.append("text")
                .attr("x", width / 2 + margin.left)
                .attr("y", 20)
                .text(`Temperature in ${state} from ${years_array[0]} to ${years_array[years_array.length - 1]}`)
                .style("font-size", "28px")
                .attr("text-anchor", "middle")
                .style("fill", "wheat");
        }
    }

    function polar_chart(data, state, year) {
        console.log("polar chart");
    }

    function bridge_chart(data, state) {
        console.log("bridge chart");
    }

</script>



<div class="assignment3">

    <div class="backhome">
        <a href="/"> &#x2190 Home </a>
    </div>

    <nav class="chart-buttons">
        <ul>
            <li> <button on:click={options_change("line")}> <iconify-icon class="icon" icon="ph:chart-line" width="100%" /> </button> </li>
            <li> <button on:click={polar_chart("polar")}> <iconify-icon class="icon" icon="ph:chart-polar-light" width="100%"/> </button> </li>
            <li> <button on:click={bridge_chart("bridge")}> <iconify-icon class="icon" icon="material-symbols:area-chart-rounded" width="100%"/> </button> </li>
        </ul>
    </nav>

    <svg id="chart" class="chart"></svg>

    <div class="tools">

        <label for="states"> State: </label>
        <select on:change={options_change} id="states"></select>

        <label for="year"> Number of years: {n_year} </label>
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