// 公開用の3冊の表紙を作る。使い方: node covers.js <slides dir>
const fs = require('fs');
const path = require('path');
const dir = process.argv[2];

const covers = [
  { id: 'cover-arch', no: '01', title: 'アーキテクチャ', sub: '全体像から、実際の構成まで', who: 'エンジニア向け', accent: '#7FB0FF',
    toc: ['全体のしくみ', '売買エンジンとAIのつながり', 'Webアプリ(AWS)のしくみ'] },
  { id: 'cover-flow', no: '02', title: '処理フロー', sub: '誰が・いつ・何をするのか', who: 'エンジニア・ビジネス', accent: '#6FD3C5',
    toc: ['5人のAIと、1台の機械', 'AIは考えるだけ。お金を動かすのは機械', '24時間の動き', '情報が集まってから、振り返るまで', '方針ができて、使われるまで', '3秒ごとの売買の判断'] },
  { id: 'cover-biz', no: '03', title: 'AIエージェントの<br>狙いと解説', sub: '何ができて、なぜ安心で、どう測るのか', who: 'ビジネス向け', accent: '#F2B27A',
    toc: ['ひとことで言うと', 'このAIエージェントの狙い', '性格のちがう3つの財布', 'まちがえても、止まっても大丈夫', 'Slack と Webアプリで見られること', 'AIは「AIなし」に勝てるか?', 'いまの段階とこれから'] },
];

for (const c of covers) {
  const items = c.toc.map((t, i) => `<div style="display:flex;flex-direction:row;align-items:center;gap:20px;border-bottom:1px solid #2E3D63;padding:12px 0px"><p style="width:56px;font-size:26px;font-weight:700;color:${c.accent}">${String(i + 1).padStart(2, '0')}</p><p style="font-size:30px;color:#E6EBF5">${t}</p></div>`).join('\n');
  const html = `<section id="${c.id}" data-transition="fade" style="background:#16213A;color:#F6F4EE;font-family:'Noto Sans JP', Arial, sans-serif;padding:120px 128px;display:flex;flex-direction:row;align-items:center;gap:96px">
<div style="width:820px;display:flex;flex-direction:column;gap:28px">
<p style="font-size:28px;font-weight:700;letter-spacing:2px;color:${c.accent}">AIトレードデスク ・ Version 1.0</p>
<div style="display:flex;flex-direction:row;align-items:center;gap:24px"><p style="font-family:'Zen Maru Gothic', 'Noto Sans JP', sans-serif;font-size:120px;font-weight:700;line-height:1;color:#3A4A6B">${c.no}</p></div>
<h1 style="font-family:'Zen Maru Gothic', 'Noto Sans JP', sans-serif;font-size:84px;font-weight:700;line-height:1.2;color:#F6F4EE">${c.title}</h1>
<p style="font-size:36px;line-height:1.5;color:#C9D3E6">${c.sub}</p>
<div style="display:flex;flex-direction:row"><p style="font-size:26px;font-weight:700;color:#16213A;background:${c.accent};padding:8px 28px;border-radius:999px">${c.who}</p></div>
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:4px">
<p style="font-size:24px;font-weight:700;letter-spacing:4px;color:#8A96AD;padding:0px 0px 12px 0px">CONTENTS</p>
${items}
</div>
</section>
`;
  fs.writeFileSync(path.join(dir, c.id + '.html'), html);
}
console.log('ok');
