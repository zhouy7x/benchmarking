# Contributing

Contributions are always welcome, no matter how large or small. Before
contributing, please read the
[code of conduct](https://github.com/v8/web-tooling-benchmark/blob/master/CODE_OF_CONDUCT.md).

## Setup locally

> The Web Tooling Benchmark doesn't officially support any version of [Node](https://www.nodejs.org/) prior to Node 8, it currently works with Node 6 and Node 7, but that might change at any point in time.

To start developing on the Web Tooling Benchmark you only need to install its dependencies:

```bash
git clone https://github.com/v8/web-tooling-benchmark
cd web-tooling-benchmark
npm install
```

## Tests

There's no formal test suite yet. For now the process is roughly:

- [ ] Check that `npm install` passes.
- [ ] Check that `npm test` passes.
- [ ] Check that the suite runs in `node`, via `node src/cli.js`.
- [ ] Check that the suite runs in `d8` via `/path/to/d8 dist/cli.js`.
- [ ] Check that the browser bundle works by pointing your browser to `dist/index.html`.

## Creating a new benchmark

- Create a new issue that describes the motivation for including the benchmark. Include any relevant information.
- The pull request should include:
  - [ ] An update to the [in-depth.md](https://github.com/v8/web-tooling-benchmark/blob/master/docs/in-depth.md) document. Add a new entry to that list for the new benchmark, which describes the tool and the concrete benchmark case.
  - [ ] Add a new file `src/foo-benchmark.js`, which includes the actual driver code for the benchmark (see the [`src/babylon-benchmark.js`](https://github.com/v8/web-tooling-benchmark/blob/master/src/babylon-benchmark.js) for example).
  - [ ] Add a new file `src/foo-benchmark.test.js`, which checks that the benchmark in `src/foo-benchmark.js` at least runs to completion.
  - [ ] `npm install --save-exact` any necessary dependencies, and be sure to include the `package.json` changes in your pull request.
  - [ ] Put any assets used by the benchmark into the `third_party` folder and hook them up with the virtual file system in `src/vfs.js`.

Many of the steps above can be automated with the `npm run new-benchmark` script. It uses [`wtb-generate`](https://github.com/alopezsanchez/web-tooling-benchmark-generator), which is a CLI tool that automates some repetitive task when creating new benchmarks.

## Sign the CLA

Before we can use your code you have to sign the [Google Individual Contributor License Agreement](https://cla.developers.google.com/about/google-individual), which you can do online. This is mainly because you own the copyright to your changes, even after your contribution becomes part of our codebase, so we need your permission to use and distribute your code. We also need to be sure of various other things, for instance that you’ll tell us if you know that your code infringes on other people’s patents. You don’t have to do this until after you’ve submitted your code for review and a member has approved it, but you will have to do it before we can put your code into our codebase.

Contributions made by corporations are covered by a different agreement than the one above, the [Software Grant and Corporate Contributor License Agreement](https://cla.developers.google.com/about/google-corporate).

Sign them online [here](https://cla.developers.google.com/).
