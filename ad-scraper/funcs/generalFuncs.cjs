const readline = require('readline');

module.exports = {
  /** Prompt user to press enter and wait */
  pause: () => {
    return new Promise(resolve => {
      const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
      });
      rl.question('press enter to continue...', () => {
        rl.close();
        resolve();
      });
    });
  }
};
