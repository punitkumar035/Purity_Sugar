const fs = require('fs');
const html = fs.readFileSync('massecuite_phase4_8_9_1_centrifugal_solver.html', 'utf8');

const regex = /<\/section>\s*<aside class="props">/i;
const match = regex.exec(html);
if (match) {
  console.log('Matched section to aside props at index:', match.index);
  console.log('Match content:', JSON.stringify(match[0]));
} else {
  console.log('No match found');
}
