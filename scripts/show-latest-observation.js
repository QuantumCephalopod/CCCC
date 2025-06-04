#!/usr/bin/env node
// Quantum signature: o=))))) 🐙✨
// Temporal marker: Υ₁₄
// F33ling state: Minimalism[·](1.0)
// Creation purpose: Display the most recent self-observation entry
import fs from 'fs';

let observations;
try {
  const data = fs.readFileSync('./self_observation.json', 'utf8');
  observations = JSON.parse(data);
} catch {
  console.error('Unable to read self_observation.json');
  process.exit(1);
}

if (!Array.isArray(observations) || observations.length === 0) {
  console.log('No observations recorded yet.');
  process.exit(0);
}

const latest = observations[observations.length - 1];
console.log(JSON.stringify(latest, null, 2));
