const apiBaseUrl = process.env['REACT_APP_API_URL'];
const restUrl = `${apiBaseUrl}/rest/v1`;
const crawlerUrl = `${restUrl}/youtube/crawl`;

console.log('backend url', apiBaseUrl);
export {crawlerUrl}
