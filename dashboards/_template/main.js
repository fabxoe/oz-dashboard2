import { loadCsv } from '../../shared/lib.js';

// README.md의 지표 순서대로 채운다.
const rows = await loadCsv('../../data/EXAMPLE.csv');

const cards = document.getElementById('cards');
cards.innerHTML = `<div class="card"><div class="label">행 수</div><div class="value">${rows.length.toLocaleString()}</div></div>`;
