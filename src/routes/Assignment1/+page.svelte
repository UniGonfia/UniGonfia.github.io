<script>
    import FaRegChartBar from 'svelte-icons/fa/FaRegChartBar.svelte'
    import FaBuromobelexperte from 'svelte-icons/fa/FaBuromobelexperte.svelte'

    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    import data_file from '$lib/data/assignment1.json';
    
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
        
        const dropdown_o = document.getElementById('dropdown_o');
        const value_o = dropdown_o.value;

          if (value_o == "Percentage") {
            o_barchart_percent(value);
          } else if (value_o == "Count") {
            o_barchart_count(value);
          } else if (value_o == "Multiple") {
            o_barchart_multiple(value);
          }

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
      dropdown.style.display = "block";
      dropdown.innerHTML = '';

      //clean chart
      const chart = document.getElementById('chart');
      chart.innerHTML = '';

      const dropdown_o = document.getElementById('dropdown_o');
      dropdown_o.style.display = "none";

      Object.keys(cities).forEach(city => {
        if (city == "null") return;
        const option = document.createElement('option');
        option.value = city;
        option.innerText = city;
        dropdown.appendChild(option);
      });

      v_barchart("New York");

      let text = `
        This graph displays the top 10 tree species within a chosen city, which can be selected via a dropdown menu. 
        The y-axis represents the tree count, while the x-axis denotes the specific tree species. 
        
        The graph is organized in descending order, showcasing the most prevalent tree species first and progressing to the less common ones.
        
        The graph is interactive, allowing the user to hover over the bars to see the exact count of each tree species and the average height if it is available.
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
  
      //animate the creation of bars
      svg.selectAll("rect")
        .data(data)
        .enter()
        .append("rect")
        .attr("x", d => x(d.scientific_name))
        .attr("y", d => y(0))
        .attr("width", x.bandwidth())
        .attr("height", d => height - marginBottom - y(0))
        .attr("fill", "#9ac9db")
        .transition()
        .duration(800)
        .attr("y", d => y(d.count))
        .attr("height", d => height - marginBottom - y(d.count))
        .delay((d, i) => (i * 100))
        
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
        .attr("opacity", 0)
        .transition()
        .duration(800)
        .attr("opacity", 1)
        .delay((d, i) => (i * 100))


      // y axis
      svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(d3.axisLeft(y).tickFormat((y) => (y).toFixed()))
        .call(g => g.select(".domain").remove())
        .selectAll("text")
        .style("font-size", "1.2em")
        .attr("opacity", 0)
        .transition()
        .duration(800)
        .attr("opacity", 1)
        .delay((d, i) => (i * 100))
      
      // Title
      svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", marginTop - 50)
        .attr("text-anchor", "middle")  
        .style("font-size", "32px") 
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

          d3.select(this)
            .style("fill", "#f1cc86")
            

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

          d3.select(this)
            .style("fill", "#9ac9db")

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

      // Calculate how many city there are in a state and remove the one with just one city
      Object.keys(states).forEach(state => {
        if (state == "null") return;
        const cities = data.filter(d => d.state == state).reduce((acc, curr) => {
          acc[curr.city] = true;
          return acc;
        }, {});
        if (Object.keys(cities).length == 1) {
          delete states[state];
        }
      });

      //clean the dropdown
      dropdown.style.display = "block";
      dropdown.innerHTML = '';

      //clean chart
      const chart = document.getElementById('chart');
      chart.innerHTML = '';

      Object.keys(states).forEach(state => {
        if (state == "null") return;
        const option = document.createElement('option');
        option.value = state;
        option.innerText = state;
        dropdown.appendChild(option);
      });

      //unhide the other dropdown
      const dropdown_o = document.getElementById('dropdown_o');
      dropdown_o.style.display = "block";

      o_barchart_percent("New York");

    }

    function o_barchart_percent(state) {

      let text = `
              This graph represents for the chosen state the cities and their percentage presence of the top 5 species for each city.

              It is useful to see first of all which species are present in a state but especially how much is the percentage of each species for each city, to check its diversity.

              The state with just one city is not shown.

              Hovering the mouse over a rectangle will display its percentage and species.
            `

      const explanation = document.getElementById('explanation');
      explanation.innerText = text;
      // Load the data from data_file
      let data = data_file;

      // Filter data for the selected state
      data = data.filter(d => d.state == state);

      // Group data by city and calculate percentages
      const cityData = data.reduce((acc, curr) => {
        if (!acc[curr.city]) {
          acc[curr.city] = [];
        }
        acc[curr.city].push(curr);
        return acc;
      }, {});

      //Take the only top5 species but calculate the percentage to the total, add a new field to the object for the other
      for (const city in cityData) {
        const total = cityData[city].reduce((acc, curr) => acc + curr.count, 0);

        cityData[city].sort((a, b) => b.count - a.count);
        cityData[city] = cityData[city].slice(0, 5);

        cityData[city].forEach(d => {
          d.percent = (d.count / total) * 100;
        });
      }

      for (const city in cityData) {
        const total = cityData[city].reduce((acc, curr) => acc + curr.percent, 0);
        cityData[city].push({
          city: city,
          scientific_name: "Other",
          percent: 100 - total,
        });
      }

      //order the data
      for (const city in cityData) {
        cityData[city].sort((a, b) => a.percent - b.percent);
      }


      // Flatten the data for chart rendering
      data = Object.values(cityData).flatMap(city => city);



      // Set chart dimensions and margins
      const margin = { top: 120, right: 100, bottom: 150, left: 100 };
      const width = 1300 - margin.left - margin.right;
      const height = 800 - margin.top - margin.bottom;

      // Extract unique city and species names
      const cities = [...new Set(data.map(d => d.city))];
      const species = [...new Set(data.map(d => d.scientific_name))];

      // Create an SVG element for the chart
      const svg = d3.select("#chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      // Create Y axis
      const y = d3.scaleBand()
        .domain(cities)
        .range([0, height])
        .padding([0.2])
      
      svg.append("g")
        .call(d3.axisLeft(y).tickSizeOuter(0))
        .selectAll("text")
        .attr("class", "yax")
        .style("font-size", "1em");


      // Create X axis
      const x = d3.scaleLinear()
        .domain([0, 100])
        .range([0, width]);

      svg.append("g")
        .call(d3.axisBottom(x));

      // Define color scale
      const color = d3.scaleOrdinal()
        .domain(species)
        .range([  
          "#FFA07A", // Light Salmon
          "#E0BBE4", // Pale Lavender
          "#FFD700", // Gold
          "#97E3D5", // Pale Turquoise
          "#FFDDC1", // Pale Apricot
          "#FFB6C1", // Light Pink
          "#B5E7A0", // Pastel Green
          "#FFC0CB", // Pink
          "#A9D3A4", // Mint Green
          "#C3D1FB",  //Soft Violet 
          "#FF91A4", // Pastel Red
          "#94D0CC", // Pale Teal
          "#D4A5A5", // Soft Rose
          "#C5E384", // Light Lime
          "#B2A8E2"  // Lavender Blue
        ]);

      const citySpeciesData = [];
      data.forEach((d) => {
        let citySpeciesGroup = citySpeciesData.find((group) => group.city === d.city);

        if (!citySpeciesGroup) {
          citySpeciesGroup = {
            city: d.city,
            percentages: [],
          };
          citySpeciesData.push(citySpeciesGroup);
        }

        citySpeciesGroup.percentages.push({
          name: d.scientific_name,
          value: d.percent,
        });
      });

      // Create a stacked bar chart
      let series = d3.stack()
        .keys(species)
        .value((d, key) => {
          const percent = d.percentages.find(p => p.name === key);
          return percent ? percent.value : 0;
        })
        .order(d3.stackOrderAscending)(citySpeciesData);

      
      

      
      const bars = svg.selectAll(".bar")
        .data(series)
        .enter()
        .append("g")
        .attr("class", "bar")
        .attr("fill", d => d.key != "Other" ? color(d.key) : "lightgrey");

      bars.selectAll("rect")
      .data(d => d)
      .enter()
      .append("rect")
      .attr("y", d => y(d.data.city))
      .attr("x", d => x(0))
      .attr("width", d => x(0))
      .attr("height", y.bandwidth())
      .attr("class", "barrect")
      .transition()
      .duration(800)
      .attr("x", d => x(d[0]))
      .attr("width", d => x(d[1]) - x(d[0]))
      .delay((d, i) => (i * 50))


      //put the x axis to the tob of the x axis
      svg.selectAll(".tick text")
        .attr("transform", "translate(0,-30)");

      svg.selectAll(".yax")
        .attr("transform", "translate(0,0)");

      const speciesColors = {};
      data.forEach((d) => {
        if (d.scientific_name == "Other") {
          speciesColors[d.scientific_name] = "lightgrey";
        } else {
          speciesColors[d.scientific_name] = color(d.scientific_name);
        }
      });

      // Create an SVG group for the legend
      const legend = svg.append("g")
        .attr("class", "legend")
        .attr("transform", `translate(${0}, ${height + 10})`)

      // Create legend items
      const legendItems = legend.selectAll(".legend-item")
        .data(Object.entries(speciesColors))
        .enter()
        .append("g")
        .attr("class", "legend-item")
        .attr("transform", (d, i) => `translate(${i % 3 * 350}, ${Math.floor(i / 3) * 20})`);

      // Create colored squares in the legend
      legendItems.append("rect")
        .attr("width", 16) 
        .attr("height", 16)
        .style("fill", d => d[1]);

      // Add text labels to the legend
      legendItems.append("text")
        .attr("x", 24) 
        .attr("y", 15) 
        .text(d => d[0])
        .attr("class", "legend-text")
        .attr("fill", "wheat")

      // Add chart title
      svg.append("text")
        .attr("class", "chart-title")
        .attr("x", width / 2)
        .attr("y", -margin.top / 2)
        .style("text-anchor", "middle")
        .style("fill", "wheat")
        .style("font-size", "32px")
        .text("Horizontal Stacked Bar Chart for Cities and Species by percent");

      //Add on hover data
      const tooltip = d3.select("body")
      .append("div")
      .style("position", "absolute")
      .style("background-color", "wheat")
      .style("color", "#364e51")
      .style("border-radius", "5px")
      .style("padding", "10px")
      .style("opacity", 0);
      
      svg.selectAll(".barrect")
      .on("mouseover", function(event, d) {

          d3.select(this)
            .attr("y", d => y(d.data.city) - 5)
            .attr("stroke-width", 4)
            .attr("stroke", "black")

          const species = d3.select(this.parentNode).datum().key;

          tooltip.transition()
            .duration(100)
            .style("opacity", 0.9);
          
          tooltip
            .html(`
              Species: ${species} <br>
              Value: ${(d[1] - d[0]).toFixed(2)}%
            `)
            .style("left", (event.pageX + 30) + "px")
            .style("top", (event.pageY - 30) + "px");
      })
      .on("mouseout", function(d) {

        d3.select(this)
          .attr("y", d => y(d.data.city))
          .attr("stroke-width", 0)

        tooltip.transition()
          .duration(500)
          .style("opacity", 0);
      });

    }

    function o_barchart_onselect(e) {

      const val = e.target.value;

      //clean chart
      const chart = document.getElementById('chart');
      chart.innerHTML = '';

      const state = document.getElementById('dropdown').value;

      if (val == "Percentage") {
        o_barchart_percent(state);
      } else if (val == "Count") {
        o_barchart_count(state);
      } else if (val == "Multiple") {
        o_barchart_multiple(state);
      }
    }

    function o_barchart_count(state) {

      let text = `
              In this graph we can see the actual number of species for each city in the selected state. 
              This unlike the percentage graph gives us a clearer idea of the amount of species for each city.

              The state with just one city is not shown.

              Hovering the mouse over a rectangle will display its count and species.
            `

      const explanation = document.getElementById('explanation');
      explanation.innerText = text;

      // Load the data from data_file
      let data = data_file;

      // Filter data for the selected state
      data = data.filter(d => d.state == state);

      // Group data by city and calculate percentages
      const cityData = data.reduce((acc, curr) => {
        if (!acc[curr.city]) {
          acc[curr.city] = [];
        }
        acc[curr.city].push(curr);
        return acc;
      }, {});

      // Sort and limit each city's data to the top 5
      for (const city in cityData) {
        cityData[city].sort((a, b) => b.count - a.count);
        cityData[city] = cityData[city].slice(0, 5);
      }

      // Add the other species to each city's data
      for (const city in cityData) {
        const total = cityData[city].reduce((acc, curr) => acc + curr.count, 0);
        cityData[city].push({
          city: city,
          scientific_name: "Other",
          count: total,
        });
      }

      // Flatten the data for chart rendering
      data = Object.values(cityData).flatMap(city => city);


      // Set chart dimensions and margins
      const margin = { top: 120, right: 100, bottom: 150, left: 100 };
      const width = 1300 - margin.left - margin.right;
      const height = 800 - margin.top - margin.bottom;

      // Extract unique city and species names
      const cities = [...new Set(data.map(d => d.city))];
      const species = [...new Set(data.map(d => d.scientific_name))];

      // Create an SVG element for the chart
      const svg = d3.select("#chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)

      // Create Y axis
      const y = d3.scaleBand()
        .domain(cities)
        .range([0, height])
        .padding([0.2])

      svg.append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`)
        .call(d3.axisLeft(y).tickSizeOuter(0))
        .selectAll("text")
        .attr("class", "yax")
        .style("font-size", "1em");


      // Define color scale
      const color = d3.scaleOrdinal()
        .domain(species)
        .range([  
          "#FFA07A", // Light Salmon
          "#E0BBE4", // Pale Lavender
          "#FFD700", // Gold
          "#97E3D5", // Pale Turquoise
          "#FFDDC1", // Pale Apricot
          "#FFB6C1", // Light Pink
          "#B5E7A0", // Pastel Green
          "#FFC0CB", // Pink
          "#A9D3A4", // Mint Green
          "#C9C1BB", // Pale Gray
          "#FF91A4", // Pastel Red
          "#94D0CC", // Pale Teal
          "#D4A5A5", // Soft Rose
          "#C5E384", // Light Lime
          "#B2A8E2"  // Lavender Blue
        ]);

      const citySpeciesData = [];

      data.forEach((d) => {
        let citySpeciesGroup = citySpeciesData.find((group) => group.city === d.city);

        if (!citySpeciesGroup) {
          citySpeciesGroup = {
            city: d.city,
            counts: [],
          };
          citySpeciesData.push(citySpeciesGroup);
        }

        citySpeciesGroup.counts.push({
          name: d.scientific_name,
          value: d.count,
        });
      });

      //title
      svg.append("text")
        .attr("class", "chart-title")
        .attr("x", (width+margin.left+margin.right) / 2)
        .attr("y", margin.top / 2)
        .style("text-anchor", "middle")
        .style("fill", "wheat")
        .style("font-size", "32px")
        .text("Horizontal Stacked Bar Chart for Cities and Species by count");

      // Create a stacked bar chart
      const series = d3.stack()
        .keys(species)
        .value((d, key) => {
          const count = d.counts.find(p => p.name === key);
          return count ? count.value : 0;
        }).order(d3.stackOrderAscending)(citySpeciesData);

      const x = d3.scaleLinear()
        .domain([0, d3.max(series, d => d3.max(d, d => d[1]))])
        .range([0, width]);

        svg.append("g")
        .attr("transform", `translate(${margin.left}, ${height + margin.top })`)
        .call(d3.axisBottom(x))
        

      const bars = svg.selectAll(".bar")
        .data(series)
        .enter()
        .append("g")
        .attr("class", "bar")
        .attr("transform", `translate(${margin.left}, ${margin.top})`)
        .attr("fill", d => d.key != "Other" ? color(d.key) : "lightgrey");

      bars.selectAll("rect")
        .data(d => d)
        .enter()
        .append("rect")
        .attr("y", d => y(d.data.city))
        .attr("x", d => x(0))
        .attr("width", d => x(0))
        .attr("height", y.bandwidth())
        .attr("class", "barrect")
        .transition()
        .duration(800)
        .attr("x", d => x(d[0]))
        .attr("width", d => x(d[1]) - x(d[0]))
        .delay((d, i) => (i * 50))

      //put the x axis to the tob of the x axis
      svg.selectAll(".tick text")
        .attr("transform", "translate(0,10)");

      svg.selectAll(".yax")
        .attr("transform", "translate(0,0)");

      const speciesColors = {};
      data.forEach((d) => {
        if (d.scientific_name == "Other") {
          speciesColors[d.scientific_name] = "lightgrey";
        } else {
          speciesColors[d.scientific_name] = color(d.scientific_name);
        }
      });

      // Create an SVG group for the legend
      const legend = svg.append("g")
        .attr("class", "legend")
        .attr("transform", `translate(${margin.left}, ${height + 170})`)

      // Create legend items
      const legendItems = legend.selectAll(".legend-item")
        .data(Object.entries(speciesColors))
        .enter()
        .append("g")
        .attr("class", "legend-item")
        .attr("transform", (d, i) => `translate(${i % 3 * 350}, ${Math.floor(i / 3) * 20})`);

      // Create colored squares in the legend
      legendItems.append("rect")
        .attr("width", 16) 
        .attr("height", 16)
        .style("fill", d => d[1]);

      // Add text labels to the legend
      legendItems.append("text")
        .attr("x", 24) 
        .attr("y", 15) 
        .text(d => d[0])
        .attr("class", "legend-text")
        .attr("fill", "wheat")

      // Add chart title
      svg.append("text")
        .attr("class", "chart-title")
        .attr("x", width / 2)
        .attr("y", -margin.top / 2)
        .style("text-anchor", "middle")
        .style("fill", "wheat")
        .style("font-size", "32px")
        .text("Horizontal Stacked Bar Chart for Cities and Species");

      //Add on hover data
      const tooltip = d3.select("body")
      .append("div")
      .style("position", "absolute")
      .style("background-color", "wheat")
      .style("color", "#364e51")
      .style("border-radius", "5px")
      .style("padding", "10px")
      .style("opacity", 0);

      svg.selectAll(".barrect")
        .on("mouseover", function(event, d) {

          d3.select(this)
            .attr("y", d => y(d.data.city) - 5)
            .attr("stroke-width", 4)
            .attr("stroke", "black")

          const species = d3.select(this.parentNode).datum().key;

          tooltip.transition()
            .duration(100)
            .style("opacity", 0.9);
          
          tooltip
            .html(`
              Species: ${species} <br>
              Count: ${(d[1] - d[0]).toFixed(2)}
            `)
            .style("left", (event.pageX + 30) + "px")
            .style("top", (event.pageY - 30) + "px");
        })
        .on("mouseout", function(d) {

          d3.select(this)
            .attr("y", d => y(d.data.city))
            .attr("stroke-width", 0)

          tooltip.transition()
            .duration(500)
            .style("opacity", 0);
        });


    }

    function o_barchart_multiple(state) {
      let text = `
      Instead, in this graph we compare more closely the top 3 species in the chosen state, and the actual quantity in each city.
      In addition, the green bar indicates the total amount of trees in that city, so from here we can also see how many there actually are compared to the total.

      The graph has been filtered to make the visualisation clearer, in particular those cities that did not have at least one of the top 3 species calculated for the state have been removed, and the top 10 cities by total have been taken, because for Iowa, for example, too many cities appeared that did not allow a clear comparison.

      Hovering the mouse over a rectangle will display its count and species.
      
      `

      const explanation = document.getElementById('explanation');
      explanation.innerText = text;

      // Load the data from data_file
      let data = data_file;

      // Filter data for the selected state
      data = data.filter(d => d.state == state);

      // Group data by city and calculate percentages
      const cityData = data.reduce((acc, curr) => {
        if (!acc[curr.city]) {
          acc[curr.city] = [];
        }
        acc[curr.city].push(curr);
        return acc;
      }, {});

      // Sort and limit each city's data to the top 5
      for (const city in cityData) {
        cityData[city].sort((a, b) => b.count - a.count);
        cityData[city] = cityData[city].slice(0, 5);
        const total = cityData[city].reduce((acc, curr) => acc + curr.count, 0);
        cityData[city].forEach(d => {
          d.percent = (d.count / total) * 100;
        });
      }

      // Flatten the data for chart rendering
      data = Object.values(cityData).flatMap(city => city);

      // Set chart dimensions and margins
      const margin = { top: 200, right: 100, bottom: 100, left: 100 };
      const width = 1300 - margin.left - margin.right;
      const height = 900 - margin.top - margin.bottom;

      // Find the top three species by count from all the cities
      const top_three_species = data.reduce((acc, curr) => {
        if (!acc[curr.scientific_name]) {
          acc[curr.scientific_name] = 0;
        }
        acc[curr.scientific_name] += curr.count;
        return acc;
      }, {});

      // Calculate the total count for each city and store in a separate array
      const total_count = data.reduce((acc, curr) => {
        if (!acc[curr.city]) {
          acc[curr.city] = 0;
        }
        acc[curr.city] += curr.count;
        return acc;
      }, {});

      let top_three = Object.keys(top_three_species)
        .sort((a, b) => top_three_species[b] - top_three_species[a])
        .slice(0, 3);
      
      data = data.filter(d => top_three.includes(d.scientific_name));

      // Take the top 10 cities by total count
      const top_cities = Object.keys(total_count)
        .sort((a, b) => total_count[b] - total_count[a])
        .slice(0, 10);

      data = data.filter(d => top_cities.includes(d.city));
      const cities = [...new Set(data.map(d => d.city))];


      const x = d3.scaleLinear()
        .domain([0, d3.max(data, function(d) { return total_count[d.city]})])
        .range([0, width]);

      const y = d3.scaleBand()
        .domain(cities)
        .range([0, height])
        .padding([0.2]);

      // Create an SVG element for the chart
      const svg = d3.select("#chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

      // Color palette = one color per subgroup
      const color = d3.scaleOrdinal()
        .domain(top_three)
        .range([
          "#97E3D5", // Pale Turquoise
          "#FFDDC1", // Pale Apricot
          "#FFB6C1", // Light Pink
          "#B5E7A0", // Pastel Green
        ]);

      // x-axis
      svg.append("g")
        .attr("transform", `translate(${margin.left}, ${height + margin.top})`)
        .call(d3.axisBottom(x).ticks(5))
        .selectAll("text")
        .attr("class", "xax");

      // y-axis
      svg.append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`)
        .call(d3.axisLeft(y).tickSizeOuter(0))
        .selectAll("text")
        .attr("class", "yax")
        .style("font-size", "1.2em");

      top_three.push("Total");
      cities.forEach(city => {
        data.push({
          city: city,
          scientific_name: "Total",
          count: total_count[city],
        });
      });

      const ySubGroups = d3.scaleBand()
        .domain(top_three)
        .range([0, y.bandwidth()])
        .padding([0.05]);

      // Show the bars
      svg.append("g")
        .selectAll("g")
        // Enter in data = loop group per group
        .data(data)
        .join("g")
        .attr("transform", d => `translate(${margin.left}, ${y(d.city) + margin.top})`)
        .selectAll("rect")
        .data(function (d) {
          return [{ key: d.scientific_name, value: d.count }];
        })
        .join("rect")
        .attr("x", 0)
        .attr("y", d => ySubGroups(d.key))
        .attr("width", d => x(0))
        .attr("height", ySubGroups.bandwidth())
        .attr("fill", d => color(d.key))
        .attr("class", "barrect")
        .transition()
        .duration(800)
        .attr("width", d => x(d.value))
        .delay((d, i) => (i * 100))


        //Add title
        svg.append("text")
        .attr("class", "chart-title")
        .attr("x", (width+margin.left+margin.right) / 2 + 50)
        .attr("y", margin.top / 2)
        .style("text-anchor", "middle")
        .style("fill", "wheat")
        .style("font-size", "32px")
        .text("Horizontal Stacked Bar Chart for subgroups with total");

        // Add legend
        const legend = svg.append("g")
          .attr("class", "legend")
          .attr("transform", `translate(${(width - margin.left - margin.right)/2}, ${margin.top - 50})`)

        // Create legend items
        const legendItems = legend.selectAll(".legend-item")
          .data(Object.entries(color.domain()))
          .enter()
          .append("g")
          .attr("class", "legend-item")
          .attr("transform", (d, i) => `translate(${i % 2 * 350}, ${Math.floor(i / 2) * 20})`);

        // Create colored squares in the legend
        legendItems.append("rect")
          .attr("width", 16) 
          .attr("height", 16)
          .style("fill", d => color(d[1]));

        // Add text labels to the legend
        legendItems.append("text")
          .attr("x", 24) 
          .attr("y", 15) 
          .text(d => d[1])
          .attr("class", "legend-text")
          .attr("fill", "wheat")
          .style("font-size", "1em")

        //Add on hover data
        const tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("background-color", "wheat")
        .style("color", "#364e51")
        .style("border-radius", "5px")
        .style("padding", "10px")
        .style("opacity", 0);

        svg.selectAll(".barrect")
          .on("mouseover", function(event, d) {

            d3.select(this)
              .attr("y", d => ySubGroups(d.key) - 5)
              .attr("stroke-width", 4)
              .attr("stroke", "black")

            tooltip.transition()
              .duration(100)
              .style("opacity", 0.9);
            
            tooltip
              .html(`
                Species: ${d.key} <br>
                Count: ${d.value}
              `)
              .style("left", (event.pageX + 30) + "px")
              .style("top", (event.pageY - 30) + "px");
          })
          .on("mouseout", function(d) {

            d3.select(this)
              .attr("y", d => ySubGroups(d.key))
              .attr("stroke-width", 0)

            tooltip.transition()
              .duration(500)
              .style("opacity", 0);
          });


    }

    function button_heatmap() {
      active_chart = {
        v_bar: false,
        o_bar: false,
        heatmap: true
      }

      const dropdown = document.getElementById('dropdown');
      dropdown.innerHTML = '';
      dropdown.style.display = "none";

      const dropdown_o = document.getElementById('dropdown_o');
      dropdown_o.style.display = "none";
      
      //clean chart
      const chart = document.getElementById('chart');
      chart.innerHTML = '';

      heatmap("Acer negundo");

      let text = `
        This graph represents a heatmap, on the x-axis we have the top 10 species by count, 
        obtained by ranking over all the data, and on the y-axis the top 10 cities also by count 
        over all the data. 

        It is useful to understand which are the most important species in the
        most important cities. 
        
        Hovering the mouse over the square will show which species it is, the city, and the total count.
      `

      const explanation = document.getElementById('explanation');
      explanation.innerText = text;


    }

    function heatmap() {
      const data = data_file;

      //take top 10 cities by total count
      const cities = data.reduce((acc, curr) => {
        if (!acc[curr.city]) {
          acc[curr.city] = 0;
        }
        acc[curr.city] += curr.count;
        return acc;
      }, {});

      const top_cities = Object.keys(cities).sort((a, b) => cities[b] - cities[a]).slice(0, 10);

      //take top 10 species by total count
      const species = data.reduce((acc, curr) => {
        if (!acc[curr.scientific_name]) {
          acc[curr.scientific_name] = 0;
        }
        acc[curr.scientific_name] += curr.count;
        return acc;
      }, {});

      const top_species = Object.keys(species).sort((a, b) => species[b] - species[a]).slice(0, 10);

      //create a heatmap matrix
      let matrix = []
      for (let i = 0; i < top_cities.length; i++) {
        for (let j = 0; j < top_species.length; j++) {
          matrix.push({
            city: top_cities[i],
            specie: top_species[j],
            count: data.filter(d => d.city == top_cities[i] && d.scientific_name == top_species[j]).reduce((acc, curr) => acc + curr.count, 0) 
          })
        }
      }

      // Set chart dimensions and margins
      const margin = { top: 100, right: 300, bottom: 200, left: 200 };
      const width = 1200 + margin.left;
      const height = 800 + margin.top;

      // Create an SVG element for the chart
      const svg = d3.select("#chart")
        .append("svg")
        .attr("width", width)
        .attr("height", height)

      const x = d3.scaleBand()
        .range([margin.left, width - margin.right])
        .domain(top_species)
        .padding(0.01);
      svg.append("g")
        .style("font-size", 15)
        .call(d3.axisBottom(x).tickSize(0))
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .selectAll(".tick text")
        .attr("class", "xax")
        .select(".domain").remove()

      svg.selectAll(".xax")
        .attr("transform", "rotate(-45) translate(-10, -10)")
        .attr("text-anchor", "end")

      const y = d3.scaleBand()
        .range([margin.top, height - margin.bottom])
        .domain(top_cities)
        .padding(0.01)

      svg.append("g")
        .style("font-size", 15)
        .call(d3.axisLeft(y).tickSize(0))
        .attr("transform", `translate(${margin.left},0)`)
        .selectAll(".tick text")
        .attr("class", "yax")
        .select(".domain").remove()

      svg.append("text")
        .attr("class", "chart-title")
        .attr("x", width / 2 - 70)
        .attr("y", 30)
        .style("text-anchor", "middle")
        .style("fill", "wheat")
        .style("font-size", "32px")
        .text("Heatmap for Top 10 Cities with Top 10 Species");

      const colorScale = d3.scaleSequential()
        .domain([0, d3.max(matrix, d => d.count)])
        .interpolator(d3.interpolateBlues)

      svg.selectAll()
        .data(matrix, function(d) {return d.city+':'+d.specie;})
        .enter()
        .append("rect")
          .attr("x", function(d) { return x(d.specie) })
          .attr("y", function(d) { return y(d.city) })
          .attr("rx", 4)
          .attr("ry", 4)
          .attr("width", x.bandwidth() )
          .attr("height", y.bandwidth() )
          .style("stroke-width", 4)
          .style("stroke", "none")
          .style("fill", function(d) { return colorScale(d.count)} )
          .style("opacity", 0)
          .transition()
          .duration(800)
          .style("opacity", 1)
          .delay((d, i) => (Math.random() * 1000))

      //tooltip
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

          //add border to the rect
          d3.select(this)
            .style("stroke-width", 4)
            .style("stroke", "black")

          tooltip.transition()
            .duration(200)
            .style("opacity", .9);

          tooltip
            .html(`
              City: ${d.city} <br>
              Species: ${d.specie} <br>
              Count: ${d.count}
            `)
            .style("left", (event.pageX + 30) + "px")
            .style("top", (event.pageY - 30) + "px")
        })
        .on("mouseout", function(d) {

          //remove border from the rect
          d3.select(this)
            .style("stroke-width", 0)

          tooltip.transition()
            .duration(500)
            .style("opacity", 0);
        });
          

        
  
      
    }

    onMount(async () => {
        button_v_barchart();
    });


</script>

<div class="assignment1">

  <div class="backhome">
    <a href="/"> &#x2190 Home </a>
  </div>

  <div class="container">
    <nav class="chart_nav"> 
      <ul>
        <li> <button on:click={button_v_barchart}> <div class="icon"> <FaRegChartBar /> </div> </button> </li>
        <li> <button on:click={button_heatmap}> <div class="icon"> <FaBuromobelexperte/> </div> </button> </li>
        <li> <button on:click={button_o_barchart}> <div class="icon rotate"> <FaRegChartBar/> </div> </button> </li>
      </ul>
    </nav>
    
    <svg id="chart"></svg>
    
    <div class="stuff">
      <select id="dropdown" class="dropdown" on:change={select_change}> </select>

      <select id="dropdown_o" class="dropdown drop_o" on:change={o_barchart_onselect}>
        <option value="Percentage"> Percentage </option>
        <option value="Count"> Count </option>
        <option value="Multiple"> Multiple </option>
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

    .backhome {
      position: absolute;
      top: 2rem;
      left: 2rem;
    }

    .backhome a {
      font-size: 1.5em;
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

    .drop_o {
      display: none;
    }

    @media screen and (max-width: 1320px) {
      .container {
        flex-direction: row;
      }

      svg {
        width: 100%;
      }

      .stuff {
        flex-direction: column;
        margin-left: -4rem;
      }

      .explanation {
        width: 25vw;
        margin-left: 0;
        margin-top: 0rem;
      }

      .dropdown {
        width: 20vw;
        margin-left: 0;
        margin-bottom: 2rem;
      }

      .chart_nav ul {
        flex-direction: column;
        margin-bottom: 5rem;
      }


    }

</style>
  
