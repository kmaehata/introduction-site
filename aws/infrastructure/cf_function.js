/**
 * CloudFront Function — URL リライト
 * Next.js static export の /path → /path/index.html を解決する
 * CloudFront → Functions → Viewer Request に設定する
 */
function handler(event) {
  var uri = event.request.uri;

  // ルートはそのまま
  if (uri === '/') {
    event.request.uri = '/index.html';
    return event.request;
  }

  // すでに拡張子がある場合はそのまま (.html, .js, .css, .png, .ico など)
  if (/\.[a-zA-Z0-9]+$/.test(uri)) {
    return event.request;
  }

  // /path → /path/index.html
  // /path/ → /path/index.html
  event.request.uri = uri.replace(/\/?$/, '/index.html');

  return event.request;
}
