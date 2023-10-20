<!-- BarChart.svelte -->
<script >
    import { onMount } from 'svelte';
    import * as d3 from 'd3';

    let data = [10, 20, 30, 40, 50]; // Example data

    const margin = { top: 20, right: 30, bottom: 30, left: 40 };
    const width = 400 - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;

    // Function to create the bar chart
    function createBarChart() {
        // Select the SVG container
        const svg = d3.select('#chart-container')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`);

        // Create scales
        const xScale = d3.scaleBand()
        .domain(data.map((d, i) => i))
        .range([0, width])
        .padding(0.1);

        const yScale = d3.scaleLinear()
        .domain([0, d3.max(data)])
        .range([height, 0]);

        // Create bars
        svg.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'bar')
        .attr('x', (d, i) => xScale(i))
        .attr('y', d => yScale(d))
        .attr('width', xScale.bandwidth())
        .attr('height', d => height - yScale(d));

        // Create X and Y axes
        const xAxis = d3.axisBottom(xScale);
        const yAxis = d3.axisLeft(yScale);

        svg.append('g')
        .attr('class', 'x-axis')
        .attr('transform', `translate(0, ${height})`)
        .call(xAxis);

        svg.append('g')
        .attr('class', 'y-axis')
        .call(yAxis);
    }

    onMount(() => {
        createBarChart();
    });
</script>

<div id="chart-container" class="bar"></div>

<style>
    .bar {
        fill: steelblue;
    }
</style>