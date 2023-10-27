<script>
    import FaRegChartBar from 'svelte-icons/fa/FaRegChartBar.svelte'
    import FaBuromobelexperte from 'svelte-icons/fa/FaBuromobelexperte.svelte'

    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    import data_file from '$lib/data/assignment1.json';

    import o_bar from '$lib/images/assignment1/o_bar.png';
    import v_bar from '$lib/images/assignment1/v_bar.png';
    import heatmap from '$lib/images/assignment1/heatmap.png';
    
    /*
        Data is like:
        Object {
            scientific_name: "Acanthocephala",
            city: "Baltimore",
            state: "Maryland",
            count: 1,
            mean_height: 1 
        }
    */
    
    $: active_chart = {
      v_bar: true,
      o_bar: false,
      heatmap: false
    }

    function select_change() {
      const dropdown = document.getElementById('dropdown');
      const value = dropdown.value;

      //clean chart
      const chart = document.getElementById('chart');
      chart.innerHTML = '';

      if (active_chart.v_bar) {
        v_barchart(value);
      } else if (active_chart.o_bar) {
        o_barchart(value);
      } else if (active_chart.heatmap) {
        heatmap(value);
      }
    }
      
    function button_v_barchart() {
      active_chart = {
        v_bar: true,
        o_bar: false,
        heatmap: false
      }
      const data = data_file;
      //Populate the dropdown with city
      const dropdown = document.getElementById('dropdown');
      const cities = data.reduce((acc, curr) => {
        acc[curr.city] = true;
        return acc;
      }, {});

      //clean the dropdown
      dropdown.innerHTML = '';

      //clean chart
      const chart = document.getElementById('chart');
      chart.innerHTML = '';

      Object.keys(cities).forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.innerText = city;
        dropdown.appendChild(option);
      });

      v_barchart("Los Angeles");

      let text = `
        This graph displays the top 10 tree species within a chosen city, 
        which can be selected via a dropdown menu. The y-axis represents the tree count,
        while the x-axis denotes the specific tree species. The graph is organized in descending order, 
        showcasing the most prevalent tree species first and progressing to the less common ones.
        The graph is interactive, allowing the user to hover over the bars to see the exact count of each tree species
        and the average height if it is available.
      `

      const explanation = document.getElementById('explanation');
      explanation.innerText = text;
    }

    function v_barchart (city) {

      let data = data_file;
      //Take only data with city == city
      data = data.filter(d => d.city == city)
      //Take only top 10 count
      data.sort((a, b) => b.count - a.count)
      data = data.slice(0, 10)

      // Declare the chart dimensions and margins.
      const width = 1200;
      const height = 700;
      const marginTop = 120;
      const marginRight = 0;
      const marginBottom = 100;
      const marginLeft = 40;

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
        .attr("fill", "#9ac9db")
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
        .attr("dx", "-.9em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-45)")
        .style("font-size", "1.2em")


      // y axis
      svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(d3.axisLeft(y).tickFormat((y) => (y).toFixed()))
        .call(g => g.select(".domain").remove())
      
      // Title
      svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", marginTop - 50)
        .attr("text-anchor", "middle")  
        .style("font-size", "32px") 
        .style("text-decoration", "underline")
        .style("fill", "wheat")  
        .text(`Top 10 trees species in ${city}`);

      //Add on hover data
      const tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("background-color", "wheat")
        .style("color", "#364e51")
        .style("border-radius", "5px")
        .style("padding", "10px")
        .style("opacity", 0);
      
      svg.selectAll("rect")
        .on("mouseover", function(event, d) {
          tooltip.transition()
            .duration(200)
            .style("opacity", .9);
          tooltip
            .html(`
              Species: ${d.scientific_name} <br>
              Count: ${d.count} <br>
              Average height: ${d.mean_height ? d.mean_height.toFixed(2) : "N/A"}
            `)
            .style("left", (event.pageX + 30) + "px")
            .style("top", (event.pageY - 30) + "px");
        })
        .on("mouseout", function(d) {
          tooltip.transition()
            .duration(500)
            .style("opacity", 0);
        });

    }

    function button_o_barchart() {
      active_chart = {
        v_bar: false,
        o_bar: true,
        heatmap: false
      }
      const data = data_file;
      //Populate the dropdown with state
      const dropdown = document.getElementById('dropdown');
      const states = data.reduce((acc, curr) => {
        acc[curr.state] = true;
        return acc;
      }, {});

      //clean the dropdown
      dropdown.innerHTML = '';

      //clean chart
      const chart = document.getElementById('chart');
      chart.innerHTML = '';

      Object.keys(states).forEach(state => {
        const option = document.createElement('option');
        option.value = state;
        option.innerText = state;
        dropdown.appendChild(option);
      });

      o_barchart("California");

      let text = `
        This graph displays the top 5 tree species within a chosen state, 
        which can be selected via a dropdown menu. The y-axis represents the tree count,
        while the x-axis denotes the specific tree species. The graph is organized in descending order, 
        showcasing the most prevalent tree species first and progressing to the less common ones.
        The graph is interactive, allowing the user to hover over the bars to see the exact count of each tree species
        and the average height if it is available.
      `

      const explanation = document.getElementById('explanation');
      explanation.innerText = text;

    }

    function o_barchart(state) {
      let data = data_file;
      //Take only data with state == state
      data = data.filter(d => d.state == state)
      //Take only the top 5 city with the sum of count, and the separate sum for each tree
      data = data.reduce((acc, curr) => {
        const city = curr.city;
        const count = curr.count;
        const scientific_name = curr.scientific_name;
        const mean_height = curr.mean_height;

        if (acc[city]) {
          acc[city].count += count;
          if (acc[city].trees[scientific_name]) {
            acc[city].trees[scientific_name].count += count;
            acc[city].trees[scientific_name].mean_height += mean_height;
          } else {
            acc[city].trees[scientific_name] = {
              count: count,
              mean_height: mean_height
            }
          }
        } else {
          acc[city] = {
            count: count,
            trees: {
              [scientific_name]: {
                count: count,
                mean_height: mean_height
              }
            }
          }
        }
        return acc;
      }, {});

      data = Object.keys(data).map(city => {
        const count = data[city].count;
        const trees = data[city].trees;
        // take the top 5 trees
        let tree_array = Object.keys(trees).map(scientific_name => {
          const count = trees[scientific_name].count;
          const mean_height = trees[scientific_name].mean_height;
          return {
            scientific_name: scientific_name,
            count: count,
            mean_height: mean_height
          }
        });
        tree_array.sort((a, b) => b.count - a.count)
        tree_array = tree_array.slice(0, 5)
        return {
          city: city,
          count: count,
          trees: tree_array
        }
      });

      //Take only top 5 count
      data.sort((a, b) => b.count - a.count)
      data = data.slice(0, 5)

      //graph with 5 bar for each city repersenting the top 5 tree the barchart is horizontal
      // Declare the chart dimensions and margins.
      const width = 1200;
      const height = 700;
      const marginTop = 120;
      const marginRight = 100;
      const marginBottom = 100;
      const marginLeft = 100;

      const svg = d3.select('#chart')
        .attr('width', width)
        .attr('height', height)
        .attr("viewBox", [0, 0, width + 200, height + 200])
        .attr("style", "max-width: 100%; height: auto;");

      const x = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.count)])
        .range([marginLeft, width - marginRight]);
      
      const y = d3.scaleBand()
        .domain(d3.map(data, d => d.city))
        .range([height - marginBottom, marginTop])
        .padding(0.1);
      
      // x axis
      svg.append("g")
        .attr("fill", "#9ac9db")
        .selectAll()
        .data(data)
        .join("rect")
          .attr("x", marginLeft)
          .attr("y", (d) => y(d.city))
          .attr("width", (d) => x(d.count) - x(0))
          .attr("height", y.bandwidth());
      
      // y axis
      svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(d3.axisLeft(y).tickSizeOuter(0))

      // Title
      svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", marginTop - 50)
        .attr("text-anchor", "middle")  
        .style("font-size", "32px") 
        .style("text-decoration", "underline")
        .style("fill", "wheat")  
        .text(`Top 5 trees species in ${state}`);
      
      //Add on hover data
      const tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("background-color", "wheat")
        .style("color", "#364e51")
        .style("border-radius", "5px")
        .style("padding", "10px")
        .style("opacity", 0);

      svg.selectAll("rect")
        .on("mouseover", function(event, d) {
          tooltip.transition()
            .duration(200)
            .style("opacity", .9);
          tooltip
            .html(`
              Species: ${d.scientific_name} <br>
              Count: ${d.count} <br>
              Average height: ${d.mean_height ? d.mean_height.toFixed(2) : "N/A"}
            `)
            .style("left", (event.pageX + 30) + "px")
            .style("top", (event.pageY - 30) + "px");
        })
        .on("mouseout", function(d) {
          tooltip.transition()
            .duration(500)
            .style("opacity", 0);
        });




    }

    onMount(async () => {
        button_v_barchart();
    });

    /*
      Grafico 1: Una citta con top 10 tipi di alberi, menu dropdown per selezionale la citta
      Grafico 2: Piu citta insieme, dello stesso stato per esempio, con top 5 alberi
      Grafico 3: Heatmap su alcune cittaf
    */

</script>

<div class="assignment1">
  <div class="container">
    <nav class="chart_nav"> 
      <ul>
        <li> <button on:click={button_v_barchart}> <div class="icon"> <FaRegChartBar /> </div> </button> </li>
        <li> <div class="icon"> <FaBuromobelexperte/> </div> </li>
        <li> <button on:click={button_o_barchart}> <div class="icon rotate"> <FaRegChartBar/> </div> </button> </li>
      </ul>
    </nav>
    
    <svg id="chart"></svg>

    <div>
      <select id="dropdown" class="dropdown" on:change={select_change}>
      </select>
      
      <p id="explanation" class="explanation">
        Hi there!
      </p>
    </div>

  </div>
</div>

<style>
    .assignment1 {
      position: absolute;
      top: 0;
      height: 100vh;
      width: 100vw;

      display: flex;
      flex-direction: row;

      background-color: #364e51;
    }

    .container {
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      margin-inline: auto;
    }

    svg {
      position: relative;
      width: 80rem;
      height: 10rem;
      color: wheat;
    }

    .chart_nav {
      position: relative;
    }

    .chart_nav ul {
      display: flex;
      flex-direction: column;
    }

    .chart_nav li {
      display: flex;
      list-style-type: none;
      width: 80px;
      height: 80px;
      margin: 10px;
      align-items: center;
      justify-content: center;
      background-color: wheat;
      border: 4px solid black;
      border-radius: 10%;
    }

    .chart_nav li:hover {
      background-color: rgb(241, 204, 134);
      border: 5px solid black;

    }

    .chart_nav .icon {
      position: relative;

      width: 50px;
      height: 50px;

      display: block;
      margin: auto;

      color: #364e51;
    }

    .rotate {
      transform: scaleX(-1) rotate(-90deg);
    }

    .chart_nav button {
      width: 80px;
      height: 80px;
      background-color: transparent;
      border: none;
    }

    .explanation {
      position: relative;
      width: 20rem;
      color: wheat;
      margin-left: -8rem;
    }

    .dropdown {
      position: relative;
      width: 20rem;
      height: 2rem;
      margin-left: -8rem;
      margin-bottom: 2rem;

      background-color: wheat;
      border: 0;
      border-radius: 8px;
      text-align: center;
    }

    @media screen and (max-width: 1300px) {
      .container {
        flex-direction: column;
      }

      svg {
        width: 90rem;
      }

      .explanation {
        width: 90vw;
        margin-left: 0;
        margin-top: 4rem;
      }

      .chart_nav ul {
        flex-direction: row;
        margin-bottom: 5rem;
      }

      .chart_nav li {
        width: 64px;
        height: 64px;
      }

      .chart_nav .icon {
        width: 32px;
        height: 32px;
      }
    }

  </style>
  
