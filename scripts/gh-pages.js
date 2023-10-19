var ghpages = require('gh-pages');
import dotenv from 'dotenv';
dotenv.config();

ghpages.publish(
    'public',
    {
        branch: 'gh-pages',
        silent: true,
        repo: 'https://' + dotenv.GITHUB_TOKEN + '@github.com/josecelano/svelte-deploy-with-github-actions.git',
        user: {
            name: 'leonardogonfiantini',
            email: 'lp.gonfiantini@gmail.com'
        }
    },
    () => {
        console.log('Deploy Complete!')
    }
)