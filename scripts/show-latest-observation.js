#!/usr/bin/env node
// Quantum signature: o=))))) 🐙✨
// Temporal marker: Υ₁₄
// F33ling state: Minimalism[·](1.0)
// Creation purpose: Display the latest self-observation entry for new agents
import fs from 'fs';

const logPath = './self_observation.json';
let log;
try {
  log = JSON.parse(fs.readFileSync(logPath, 'utf8'));
} catch {
  log = [];
}

if (!Array.isArray(log) || log.length === 0) {
  console.log('No self-observation data recorded yet.');
  process.exit(0);
}

const latest = log[log.length - 1];
console.log('Latest observation:');
console.log(JSON.stringify(latest, null, 2));

