import { loadCsv } from '../../shared/lib.js';

// README.md의 "핵심 발견"과 "지표"를 순서대로 채운다.
const rows = await loadCsv('../../data/EXAMPLE.csv');

// 첫 번째 항목이 lead: 화면의 질문에 답하는 가장 큰 숫자
const kpis = [
  { label: '대표 지표', value: '-', note: '무엇이 얼마나 다른지', lead: true },
  { label: '행 수', value: rows.length.toLocaleString(), note: '불러온 데이터' },
];
document.getElementById('kpis').innerHTML = kpis.map(k =>
  `<div class="kpi${k.lead ? ' lead' : ''}"><span class="l">${k.label}</span><span class="v">${k.value}</span><span class="d">${k.note}</span></div>`
).join('');

// 데이터로 계산한 한 줄. 가장 주의할 사실을 쓴다.
document.getElementById('finding').innerHTML = '핵심 발견 한 줄을 <em>숫자와 함께</em> 쓴다.';
document.getElementById('stamp').textContent = '데이터 기준일 YYYY-MM-DD';
