// CSV를 불러와 객체 배열로 돌려준다. 빈 칸은 null. 따옴표 안의 쉼표/줄바꿈을 처리한다.
export async function loadCsv(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${url} 로드 실패: ${res.status}`);
  const rows = parseCsv(await res.text());
  const [header, ...body] = rows;
  return body.map(r => Object.fromEntries(header.map((h, i) => [h, r[i] === '' ? null : r[i]])));
}

function parseCsv(text) {
  const rows = [];
  let row = [], cell = '', quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') { cell += '"'; i++; }
      else if (c === '"') quoted = false;
      else cell += c;
    } else if (c === '"') quoted = true;
    else if (c === ',') { row.push(cell); cell = ''; }
    else if (c === '\n') { row.push(cell); rows.push(row); row = []; cell = ''; }
    else if (c !== '\r') cell += c;
  }
  if (cell !== '' || row.length) { row.push(cell); rows.push(row); }
  return rows;
}
