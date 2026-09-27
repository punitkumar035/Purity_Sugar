const fs = require('fs');
const html = fs.readFileSync('massecuite_phase4_8_9_1_centrifugal_solver.html', 'utf8');

const regex = /<div class="empty-state" id="emptyState">/i;
const match = regex.exec(html);
console.log('emptyState match:', match ? match.index : 'none');
