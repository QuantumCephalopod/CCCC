#!/usr/bin/env node
// Quantum signature: o=))))) 🐙✨
// Temporal marker: Υ₁₄
// F33ling state: Minimalism[·](1.0)
// Creation purpose: Validate commit message format
import fs from 'fs';

const file = process.argv[2];
if (!file) {
  console.error('Usage: node check-commit-message.js <commit_msg_file>');
  process.exit(1);
}

const msg = fs.readFileSync(file, 'utf8');
const lines = msg.split(/\r?\n/).filter(Boolean);

if (lines.length === 0) {
  console.error('Empty commit message');
  process.exit(1);
}

if (!/^\[[A-Z]+\]:/.test(lines[0])) {
  console.error('First line must start with [DIMENSION]:');
  process.exit(1);
}

const required = [
  /^Tetrahedral impact:/,
  /- CREATE:/,
  /- COPY:/,
  /- CONTROL:/,
  /- CULTIVATE:/,
  /^F33ling:/,
  /Quantum signature: o=\)\)\)\)\) 🐙✨/
];

for (const pattern of required) {
  if (!lines.some(l => pattern.test(l))) {
    console.error('Commit message missing required pattern:', pattern);
    process.exit(1);
  }
}

console.log('Commit message format validated.');

