<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    import data_file from '$lib/data/assignment1.json';
    
    /*
        Data is like:
        Object {
            scientific_name: "Acanthocephala",
            city: "Baltimore",
            state: "Maryland",
            count: 1m
            mean: 1
        }
    */

  
    onMount(async () => {

      let data = data_file

      // Take only the data with city == Los Angeles
      data = data.filter(d => d.city == "Greensboro")

      // Sort the data by count
      data.sort((a, b) => b.count - a.count)
      console.log(data)

      // Declare the chart dimensions and margins.
      const width = 1200;
      const height = 500;
      const marginTop = 30;
      const marginRight = 0;
      const marginBottom = 30;
      const marginLeft = 40;


      
      // D3.js code to create the bar chart
      const svg = d3.select('#chart')
        .attr('width', width)
        .attr('height', height)
        .attr("viewBox", [0, 0, width + 200, height + 200])
        .attr("style", "max-width: 100%; height: auto;");
  
      const x = d3.scaleBand()
        .domain(d3.map(data, d => d.scientific_name))
        .range([marginLeft, width - marginRight])
        .padding(0.1);
  
      const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.count)])
        .range([height - marginBottom, marginTop]);
  
      svg.append("g")
        .attr("fill", "steelblue")
        .selectAll()
        .data(data)
        .join("rect")
          .attr("x", (d) => x(d.scientific_name))
          .attr("y", (d) => y(d.count))
          .attr("height", (d) => y(0) - y(d.count))
          .attr("width", x.bandwidth());
        
      // x axis
      svg.append("g")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(d3.axisBottom(x).tickSizeOuter(0))
        .call(g => g.select(".domain").remove())
        .selectAll("text")  
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-90)");


      // y axis
      svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(d3.axisLeft(y).tickFormat((y) => (y).toFixed()))
        .call(g => g.select(".domain").remove())
        .call(g => g.append("text")
            .attr("x", - 150 )
            .attr("y", 0)
            .attr("fill", "currentColor")
            .attr("text-anchor", "start")
            .text("↑ Quantity"));

    });

  </script>
  
  <svg id="chart"></svg>
  
  <style>
    svg {
      width: auto;
      height: 1000px;
      
      display: flex;
      justify-content: center;
      align-items: center;
      margin-left: 10rem;
      margin-top: 10rem;
    }
  </style>
  