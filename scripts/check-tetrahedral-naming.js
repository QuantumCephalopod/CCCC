#!/usr/bin/env node
// Quantum signature: o=))))) 🐙✨
// Temporal marker: Υ₁₄
// F33ling state: Minimalism[·](1.0)
// Creation purpose: Ensure file names follow tetrahedral prefixes
import fs from 'fs';

const prefixPattern = /^[oxyz](?:\.|$)/;
const files = fs.readdirSync('.');
const violations = files.filter(f => f.endsWith('.js') && !prefixPattern.test(f));
if (violations.length) {
  console.error('Naming violations:', violations.join(', '));
  process.exit(1);
}
console.log('Naming convention check passed.');
