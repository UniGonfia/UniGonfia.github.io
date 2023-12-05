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

    let line_description = `
        This chart shows the temperature in a state for a number of years.
        Is possible to change the state and the number of decades to consider for the comparison with the 2020, up to 10 decade <br> <br>
        It is interesting to see how temperatures change over the years. For this reason, a 10-year jump was chosen in order to note more clearly the difference between the years. <br>
        If is chosen only one decade, the chart will show the maximum, minimum and average temperature for each month and the legend will show the color for each variable. <br> <br>
        If are chosen more than one decade, the chart will show the average temperature for each month and the legend will show the color for each decade. <br>
        There is an interaction with the mouse, if the mouse is over a point, the chart will show the temperature for each variable and the decade. <br>
        This interaction was added to show how much of an overhang there is between the maximum and minimum for each year.
    `

    let polar_description = `
        This chart shows the temperature in a state for a number of decades like the previous chart, but in a radar chart. <br>
        Is possible to change the state and the number of decades to consider for the comparison with the 2020, up to 10 decade <br> <br>
        If is chosen only one decade, the chart will show the maximum, minimum and average temperature for each month and the legend will show the color for each variable. <br>
        If are chosen more than one decade, the chart will show the average temperature for each month and the legend will show the color for each decade. <br> <br>
        It is interesting to use a radar chart as one can better see the 'shape' of the temperatures, in fact it is very noticeable that for the older years there tends to be less of a fluctuation while for the newer ones there is more of a tendency to fluctuation.
    `

    let ridge_description = `
        This chart shows the density of the temperature in a state for 10 decade. <br>
        Is possible to change the state by using the tools on the right. <br> <br>
        The chart shows the density of the maximum and minimum temperature for each decade and the legend will show the color for each variable. <br>
        For the density is used the kernel density estimation with the Epanechnikov kernel. <br> <br>
        This is the graph I find most interesting for analysing temperature changes, because for recent years we have greater dispersion and temperatures that tend to be higher, while for older years we have temperatures with less dispersion and tend to be colder.
    `

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

        document.getElementById("description").innerHTML = line_description;

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

        if (chart == "line") {
            document.getElementById("description").innerHTML = line_description;
        }

        if (chart == "polar") {
            document.getElementById("description").innerHTML = polar_description;
        }

        if (chart == "ridge") {
            document.getElementById("description").innerHTML = ridge_description;
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

        const all_year = []
        const data_state = data[state];
        Object.keys(data_state).forEach(year => {
            all_year.push(year);
        });

        const y = d3.scaleLinear()
            .rangeRound([height, 0])
            .domain([d3.min(all_year, (d) => d3.min(months, (m) => data_state[d][m].min)), d3.max(all_year, (d) => d3.max(months, (m) => data_state[d][m].max))]);

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
                } else {
                    //legend
                    svg.append("circle")
                                    .attr("cx", width + margin.left - 50)
                                    .attr("cy", 60)
                                    .attr("r", 6)
                                    .style("fill", "red");
                    
                    svg.append("text")
                        .attr("x", width + margin.left - 40)
                        .attr("y", 65)
                        .text("Max")
                        .style("font-size", "15px")
                        .attr("alignment-baseline","middle")
                        .style("fill", "wheat");

                    svg.append("circle")
                                    .attr("cx", width + margin.left - 50)
                                    .attr("cy", 90)
                                    .attr("r", 6)
                                    .style("fill", "blue");
                    
                    svg.append("text")
                        .attr("x", width + margin.left - 40)
                        .attr("y", 95)
                        .text("Min")
                        .style("font-size", "15px")
                        .attr("alignment-baseline","middle")
                        .style("fill", "wheat");

                    svg.append("circle")
                                    .attr("cx", width + margin.left - 50)
                                    .attr("cy", 120)
                                    .attr("r", 6)
                                    .style("fill", "white");
                    
                    svg.append("text")
                        .attr("x", width + margin.left - 40)
                        .attr("y", 125)
                        .text("Avg")
                        .style("font-size", "15px")
                        .attr("alignment-baseline","middle")
                        .style("fill", "wheat");
                }

            
        }


        //mouse over
        for (let year of years_array) {
            let data_state = data[state];
            let data_year = data_state[year];

            svg.append("g")
                .selectAll("dot")
                .data(months)
                .enter()
                .append("circle")
                    .attr("cx", (d) => x(d) + margin.left + x.bandwidth() / 2)
                    .attr("cy", (d) => y(data_year[d].avg) + margin.top)
                    .attr("r", 5)
                    .attr("fill", "transparent")
                    .on("mouseover", function(event, d) {
                        d3.select(this)
                            .attr("fill", "white")
                            .attr("r", 10);

                        //temperatures with endline for each variable
                        svg.append("line")
                            .attr("x1", x(d) + margin.left + x.bandwidth() / 2)
                            .attr("y1", y(data_year[d].max) + margin.top)
                            .attr("x2", x(d) + margin.left + x.bandwidth() / 2)
                            .attr("y2", y(data_year[d].min) + margin.top)
                            .attr("stroke", "wheat")
                            .attr("stroke-width", 1)
                            .attr("stroke-dasharray", function() { return this.getTotalLength() })
                            .attr("stroke-dashoffset", function() { return this.getTotalLength() })
                            .transition()
                                .duration(500)
                                .attr("stroke-dashoffset", 0);

                        svg.append("line")
                            .attr("x1", x(d) + margin.left + x.bandwidth() / 2 - 10)
                            .attr("y1", y(data_year[d].max) + margin.top)
                            .attr("x2", x(d) + margin.left + x.bandwidth() / 2 + 10)
                            .attr("y2", y(data_year[d].max) + margin.top)
                            .attr("stroke", "wheat")
                            .attr("stroke-width", 1)
                            .attr("stroke-dasharray", function() { return this.getTotalLength() })
                            .attr("stroke-dashoffset", function() { return this.getTotalLength() })
                            .transition()
                                .duration(500)
                                .attr("stroke-dashoffset", 0);

                        svg.append("line")
                            .attr("x1", x(d) + margin.left + x.bandwidth() / 2 - 10)
                            .attr("y1", y(data_year[d].min) + margin.top)
                            .attr("x2", x(d) + margin.left + x.bandwidth() / 2 + 10)
                            .attr("y2", y(data_year[d].min) + margin.top)
                            .attr("stroke", "wheat")
                            .attr("stroke-width", 1)
                            .attr("stroke-dasharray", function() { return this.getTotalLength() })
                            .attr("stroke-dashoffset", function() { return this.getTotalLength() })
                            .transition()
                                .duration(500)
                                .attr("stroke-dashoffset", 0);


                        svg.append("line")
                            .attr("x1", x(d) + margin.left + x.bandwidth() / 2 - 10)
                            .attr("y1", y(data_year[d].avg) + margin.top)
                            .attr("x2", x(d) + margin.left + x.bandwidth() / 2 + 10)
                            .attr("y2", y(data_year[d].avg) + margin.top)
                            .attr("stroke", "wheat")
                            .attr("stroke-width", 1)
                            .attr("stroke-dasharray", function() { return this.getTotalLength() })
                            .attr("stroke-dashoffset", function() { return this.getTotalLength() })
                            .transition()
                                .duration(500)
                                .attr("stroke-dashoffset", 0);

                        
                        //text with temperatures
                        svg.append("text")
                            .attr("class", "textover")
                            .attr("x", x(d) + margin.left + x.bandwidth() / 2 + 15)
                            .attr("y", y(data_year[d].max) + margin.top + 5)
                            .text(parseFloat(data_year[d].max).toFixed(2) + "°F")
                            .style("font-size", "15px")
                            .attr("alignment-baseline","middle")
                            .style("fill", "wheat");

                        svg.append("text")
                            .attr("class", "textover")
                            .attr("x", x(d) + margin.left + x.bandwidth() / 2 + 15)
                            .attr("y", y(data_year[d].min) + margin.top + 5)
                            .text(parseFloat(data_year[d].min).toFixed(2) + "°F")
                            .style("font-size", "15px")
                            .attr("alignment-baseline","middle")
                            .style("fill", "wheat");

                        svg.append("text")
                            .attr("class", "textover")
                            .attr("x", x(d) + margin.left + x.bandwidth() / 2 + 15)
                            .attr("y", y(data_year[d].avg) + margin.top + 5)
                            .text(parseFloat(data_year[d].avg).toFixed(2) + "°F")
                            .style("font-size", "15px")
                            .attr("alignment-baseline","middle")
                            .style("fill", "wheat");

                        //Add the year
                        svg.append("text")
                            .attr("class", "textover")
                            .attr("x", x(d) + margin.left + x.bandwidth() / 2 + 15)
                            .attr("y", y(data_year[d].avg) + margin.top - 20)
                            .text(year)
                            .style("font-size", "15px")
                            .attr("alignment-baseline","middle")
                            .style("fill", "wheat");

                    })
                    .on("mouseout", function(event, d) {
                        d3.select(this)
                            .attr("fill", "transparent")
                            .attr("r", 5);

                        svg.selectAll("line").remove();

                        svg.selectAll(".textover").remove();
                    });
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

        let margin = {top: 225, right: 100, bottom: 200, left: 100};
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
        let all_year = []
        const data_state = data[state];
        Object.keys(data_state).forEach(year => {
            all_year.push(year);
        });
        let r = d3.scaleLinear()
            .domain([d3.min(months, (d) => d3.min(all_year, (y) => data[state][y][d].min)), d3.max(months, (d) => d3.max(all_year, (y) => data[state][y][d].max + 10))])
            .range([0, width / 2.5]);
        
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
                .attr("x2", (d, i) => r(d3.max(months, (d) => d3.max(all_year, (y) => data[state][y][d].max + 10))) * Math.cos(t(i) - Math.PI / 2))
                .attr("y2", (d, i) => r(d3.max(months, (d) => d3.max(all_year, (y) => data[state][y][d].max + 10))) * Math.sin(t(i) - Math.PI / 2))
                .attr("stroke", "wheat")
                .attr("stroke-width", 0.5);

        //draw the labels of the months
        polar.append("g")
            .selectAll("circle")
            .data(months)
            .enter()
            .append("text")
                .attr("x", (d, i) => r(d3.max(months, (d) => d3.max(all_year, (y) => data[state][y][d].max + 10))) * Math.cos(t(i) - Math.PI / 2))
                .attr("y", (d, i) => r(d3.max(months, (d) => d3.max(all_year, (y) => data[state][y][d].max + 10))) * Math.sin(t(i) - Math.PI / 2))
                .text((d) => d.toUpperCase())
                .style("font-size", "6px")
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
                    .attr("cy", -100 + years_array.indexOf(year) * 10)
                    .attr("r", 3)
                    .style("fill", color(year));
                
                polar.append("text")
                    .attr("x", width - 35)
                    .attr("y", -100 + 2 + years_array.indexOf(year) * 10)
                    .text(year)
                    .style("font-size", "5px")
                    .attr("alignment-baseline","middle")
                    .style("fill", "wheat");

                
            }
        } else {
            polar.append("circle")
                .attr("cx", width - 40)
                .attr("cy", -100)
                .attr("r", 3)
                .style("fill", "red");
            
            polar.append("text")
                .attr("x", width - 35)
                .attr("y", -98)
                .text("Max")
                .style("font-size", "5px")
                .attr("alignment-baseline","middle")
                .style("fill", "wheat");

            polar.append("circle")
                .attr("cx", width - 40)
                .attr("cy", -90)
                .attr("r", 3)
                .style("fill", "blue");
            
            polar.append("text")
                .attr("x", width - 35)
                .attr("y", -88)
                .text("Min")
                .style("font-size", "5px")
                .attr("alignment-baseline","middle")
                .style("fill", "wheat");

            polar.append("circle")
                .attr("cx", width - 40)
                .attr("cy", -80)
                .attr("r", 3)
                .style("fill", "white");
            
            polar.append("text")
                .attr("x", width - 35)
                .attr("y", -78)
                .text("Avg")
                .style("font-size", "5px")
                .attr("alignment-baseline","middle")
                .style("fill", "wheat");
        }


        //add title
        polar.append("text")
            .attr("x", 0 )
            .attr("y", -100)
            .text(`Temperature in ${state} from ${years_array[0]} to ${years_array[years_array.length - 1]}`)
            .style("font-size", "6px")
            .attr("text-anchor", "middle")
            .style("fill", "wheat");

            
    }

    function ridge_chart(data, state) {
        
        let margin = {top: 200, right: 50, bottom: 100, left: 50};
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
            .domain([0, 0.5])
            .range([height, 0]);
        
        const yName = d3.scaleBand()
            .domain(years)
            .range([margin.top, height])
            .padding(0.1);

        
        svg.append("g")
            .style("color", "wheat")
            .attr("transform", `translate(${margin.left}, ${margin.top})`)
            .attr("transform", `translate(${margin.left}, ${margin.top})`)
            .call(d3.axisLeft(yName));

        svg.append("g")
            .style("color", "wheat")
            .attr("transform", `translate(0, ${height + margin.top})`)
            .attr("transform", `translate(0, ${height + margin.top})`)
            .call(d3.axisBottom(x))
            .selectAll("text")
                .text((d) => d + "°F");

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
                .attr("transform", (d) => `translate(0, ${yName(d.year) - height + margin.top + 38})`)    
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
                .attr("transform", (d) => `translate(0, ${yName(d.year) - height + margin.top + 38})`)    
                .datum((d) => d.density)
                .attr("fill", "blue")
                .attr("opacity", 0.6)
                .attr("stroke", "white")
                .attr("stroke-width", 1)
                .attr("d", d3.line()
                    .curve(d3.curveBasis)
                )
                .attr("d", area_min);
        

        //add title
        svg.append("text")
            .attr("x", width / 2 + margin.left)
            .attr("y", margin.top - 30)
            .text(`Temperature density in ${state} from ${years[0]} to ${years[years.length - 1]}`)
            .style("font-size", "38px")
            .attr("text-anchor", "middle")
            .style("fill", "wheat");

        
        //add legend
        svg.append("circle")
            .attr("cx", width - 50)
            .attr("cy", margin.top - 50)
            .attr("r", 10)
            .style("fill", "red");

        svg.append("text")
            .attr("x", width - 30)
            .attr("y", margin.top - 45)
            .text("Max")
            .style("font-size", "25px")
            .attr("alignment-baseline","middle")
            .style("fill", "wheat");

        svg.append("circle")
            .attr("cx", width - 50)
            .attr("cy", margin.top - 20)
            .attr("r", 10)
            .style("fill", "blue");

        svg.append("text")
            .attr("x", width - 30)
            .attr("y", margin.top - 10)
            .text("Min")
            .style("font-size", "25px")
            .attr("alignment-baseline","middle")
            .style("fill", "wheat");    
        
        
   
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

        <label for="year" id="yearlabel"> Number of decades: {n_year} </label>
        <input on:change={options_change} type="range" id="year" min="1" max="10" step="1" value="1">
        
        <p id="description" class="description">

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
        width: 67%;
        height: 80%;
    }

    .tools {
        width: 23%;
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