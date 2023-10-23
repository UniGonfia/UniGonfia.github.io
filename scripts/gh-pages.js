import ghpages from 'gh-pages';

ghpages.publish(
  'build', // path to public directory
  {
    branch: 'gh-pages',
    repo: 'https://github.com/UniGonfia/UniGonfia.github.io/', // Update to point to your repository
    user: {
      name: 'leonardogonfiantini', // update to use your name
      email: 'lp.gonfiantini@gmail.com' // Update to use your email
    },
    dotfiles: true
  },
  () => {
    console.log('Deploy Complete!');
  }
);