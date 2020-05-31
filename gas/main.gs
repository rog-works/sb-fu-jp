function doGet(e) {
  const params = e.parameter;
  const texts = {}
  for (const key in Object.keys(params)) {
    const trans = LanguageApp.translate(params[key], 'en', 'ja');
    if (trans) {
      texts[key] = trans;
    }
  }
  const body = { code: 200, results: texts }
  const res = ContentService.createTextOutput();
  res.setMimeType(ContentService.MimeType.JSON);
  res.setContent(JSON.stringify(body));
  return res;
}
