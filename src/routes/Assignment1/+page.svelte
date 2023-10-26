<script>
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

  
    onMount(async () => {

      let data = data_file

      // Take only the data with city == Los Angeles
      data = data.filter(d => d.city == "Los Angeles")
      //Take only top 10 count
      data = data.filter((d) => d.count > 4000)
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

    /*
      Grafico 1: Una citta con top 10 tipi di alberi, menu dropdown per selezionale la citta
      Grafico 2: Piu citta insieme, dello stesso stato per esempio, con top 5 alberi
      Grafico 3: Heatmap su alcune cittaf
    */

</script>

<div class="assignment1">
  <nav class="chart_nav"> 
    <ul>
      <li> <img src={v_bar} alt="v_bar" /> </li>
      <li> <img src={o_bar} alt="o_bar" /> </li>
      <li> <img src={heatmap} alt="heatmap" /> </li>
    </ul>
  </nav>
  
  <svg id="chart"></svg>

  <p class="explanation">
    Lorem ipsum dolor sit amet consectetur adipisicing elit. 
    Repellat sunt dolorum ducimus est libero, doloremque neque,
    vitae optio expedita illum id suscipit magni hic laboriosam. 
    Error odit pariatur corrupti laudantium?
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Sit, 
    veniam cupiditate aut porro libero illum dolores magnam minus, 
    accusantium iste facere cum perspiciatis numquam quo eaque quos 
    delectus, pariatur atque!
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Sit, 
    veniam cupiditate aut porro libero illum dolores magnam minus, 
    accusantium iste facere cum perspiciatis numquam quo eaque quos 
    delectus, pariatur atque!
  </p>
</div>

<style>
    .assignment1 {
      position: absolute;
      top: 0;
      height: 100vh;
      width: 100vw;
      background-color: #333;
    }

    svg {
      width: auto;
      height: 1000px;
      
      display: flex;
      justify-content: center;
      align-items: center;
      margin-left: 10rem;
      margin-top: 10rem;
      color: wheat;
    }

    .chart_nav {
      position: absolute;
      display: block;
      top: 28vh;
      left: 5%;
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

    .chart_nav img {
      width: 48px;
      height: 48px;
    }

    .explanation {
      position: absolute;
      top: 28vh;
      right: 5%;
      width: 20rem;
      color: wheat;

    }

  </style>
  
