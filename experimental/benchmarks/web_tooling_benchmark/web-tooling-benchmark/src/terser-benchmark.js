// Copyright 2018 the V8 project authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

const Terser = require("../build/terser-bundled");
const fs = require("fs");

const payloads = [
  {
    name: "speedometer-es2015-test-2.0.js",
    options: { compress: { passes: 1, sequences: false } }
  }
].map(({ name, options }) => ({
  payload: fs.readFileSync(`third_party/${name}`, "utf8"),
  options
}));

module.exports = {
  name: "terser",
  fn() {
    return payloads.map(({ payload, options }) =>
      Terser.minify(payload, options)
    );
  }
};
