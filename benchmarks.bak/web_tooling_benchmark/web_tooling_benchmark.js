'use strict';
var fs = require('fs');
var vm = require('vm');

global.load = load;
global.read = read;
global.print = console.log;

process.chdir(__dirname+'/web-tooling-benchmark')
load('dist/cli.js');

function load(filename) {
  vm.runInThisContext(read(filename));
}

function read(filename) {
  return fs.readFileSync(filename, 'utf8');
}
