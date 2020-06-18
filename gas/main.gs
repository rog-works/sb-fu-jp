function doGet(e) {
  const params = e.parameter;
  const texts = {}
  for (const key of Object.keys(params)) {
    try {
      texts[key] = LanguageApp.translate(params[key], 'en', 'ja');
      Utilities.sleep(100);
    } catch (e) {
      break;
    }
  }
  const total = Object.keys(params).length;
  const translates = Object.keys(texts).length;
  const status = total == translates ? 200 : 405;
  const body = { code: status, results: texts }
  const res = ContentService.createTextOutput();
  res.setMimeType(ContentService.MimeType.JSON);
  res.setContent(JSON.stringify(body));
  return res;
}
