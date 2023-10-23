<!-- BarChart.svelte -->
<script >
    import { onMount } from 'svelte';
    import data_file from '$lib/data/assignment1.json';
    import * as d3 from 'd3';

    const createBarChart = async () => {
        console.log(data_file);
    }   

    let data
    onMount(async () => {
        await createBarChart();
    });

</script>

<div id="chart-container" class="bar"></div>

<style>
    .bar {
        fill: steelblue;
    }
</style>