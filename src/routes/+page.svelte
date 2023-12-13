<script>
    import { base } from '$app/paths';
</script>


<div class="home">

    <div class="presentation"> 
        <h1> Team Visa</h1>
        <p> Members: <a href="https://leonardogonfiantini.github.io"> Leonardo Gonfiantini </a> (S4844709) </p>
    </div>

    <div class="description">
        <p>
            This site is divided into sections, can be accessed from the <strong> menu </strong> at the bottom, <br>
            each section is an assignment and inside is a page dedicated to the exercise to be done.    <br>
            The <strong> svelte </strong> and <strong> sveltekit </strong> framework was used to create this site, the styling is handled     <br>
            in <strong> CSS </strong> and the deployment of the application to the github pages is done using the <strong> gh-pages </strong> library
            and the script found within the repository, as package manager <strong> npm </strong> was used. <br> 
            Subsequently everything will be deployed with a github-action. <br>
            The <strong>scripts</strong> folder in the repository also contains the various python scripts used to generate the datasets or the visualisations.
        </p>
    </div>

    <nav class="assignments">
        <ul>
            <li> <a href="{base}/Assignment1"> Assignment 1 - Comparing Categories </a> </li>
            <li> <a href="{base}/Assignment2"> Assignment 2 - Alluvial </a> </li>
            <li> <a href="{base}/Assignment3"> Assignment 3 - Timelines and distributions </a> </li>
            <li> <a href="{base}/Assignment4"> Assignment 4 - Maps </a> </li>
        </ul>
    </nav>

</div>

<style>

    .home {  
        background-color: #364e51;
        color: #fff;
        height: 100vh;
    }

    .presentation, .description, .assignments {
        display: block;
        margin-inline: auto;
        width: 40vw;
        padding: 20px;
    }

    @media screen and (max-width: 1300px) {
        .presentation, .description, .assignments {
            width: 60%;
        }
    }

    @media screen and (max-width: 800px) {
        .presentation, .description, .assignments {
            width: 80%;
        }
    }

    .presentation h1 {
        font-size: xx-large;
        color: wheat;
    }

    .presentation a {
        text-decoration: underline;
    }

    .description strong {
        color: wheat;
    }

    .assignments li {
        margin-bottom: 1rem;
    }

</style>