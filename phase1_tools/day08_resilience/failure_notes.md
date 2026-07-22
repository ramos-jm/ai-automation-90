## 400 error:

Automation Failed !!

Status Code: 400

message: 'messages.0' : discriminator property 'role' has invalid value

type: invalid request error

code: 400

### stack:
AxiosError: Request failed with status code 400
    at settle (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\@n8n\backend-network\node_modules\axios\dist\node\axios.cjs:2199:12)
    at RedirectableRequest.handleResponse (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\@n8n\backend-network\node_modules\axios\dist\node\axios.cjs:3965:9)
    at RedirectableRequest.emit (node:events:520:35)
    at RedirectableRequest._processResponse (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\follow-redirects\index.js:424:10)
    at ClientRequest.RedirectableRequest._onNativeResponse (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\follow-redirects\index.js:109:12)
    at Object.onceWrapper (node:events:623:26)
    at ClientRequest.emit (node:events:508:28)
    at HTTPParser.parserOnIncomingClient (node:_http_client:780:27)
    at HTTPParser.parserOnHeadersComplete (node:_http_common:123:17)
    at TLSSocket.socketOnData (node:_http_client:615:22)
    at Axios.request (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\@n8n\backend-network\node_modules\axios\dist\node\axios.cjs:5427:41)
    at processTicksAndRejections (node:internal/process/task_queues:103:5)
    at invokeAxios (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\@n8n\backend-network\src\http\axios\invoke.ts:15:10)
    at executeLegacyRequest (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\@n8n\backend-network\src\http\legacy-request.ts:77:6)
    at Object.requestLegacy (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\@n8n\backend-network\src\http\outbound-http.ts:199:13)
    at proxyRequestToAxios (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\n8n-core\src\execution-engine\node-execution-context\utils\request-helpers\legacy-request-adapter.ts:31:9)
    at Object.request (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\n8n-core\src\execution-engine\node-execution-context\utils\request-helpers\factory.ts:166:11)

## 401 error:

Automation Failed !!

Status Code: 401

message: Invalid API Key

type: invalid request error

code: invalid_api_key

### stack:
"AxiosError: Request failed with status code 401
    at settle (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\@n8n\backend-network\node_modules\axios\dist\node\axios.cjs:2199:12)
    at RedirectableRequest.handleResponse (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\@n8n\backend-network\node_modules\axios\dist\node\axios.cjs:3965:9)
    at RedirectableRequest.emit (node:events:520:35)
    at RedirectableRequest._processResponse (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\follow-redirects\index.js:424:10)
    at ClientRequest.RedirectableRequest._onNativeResponse (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\follow-redirects\index.js:109:12)
    at Object.onceWrapper (node:events:623:26)
    at ClientRequest.emit (node:events:508:28)
    at HTTPParser.parserOnIncomingClient (node:_http_client:780:27)
    at HTTPParser.parserOnHeadersComplete (node:_http_common:123:17)
    at TLSSocket.socketOnData (node:_http_client:615:22)
    at Axios.request (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\@n8n\backend-network\node_modules\axios\dist\node\axios.cjs:5427:41)
    at processTicksAndRejections (node:internal/process/task_queues:103:5)
    at invokeAxios (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\@n8n\backend-network\src\http\axios\invoke.ts:15:10)
    at executeLegacyRequest (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\@n8n\backend-network\src\http\legacy-request.ts:77:6)
    at Object.requestLegacy (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\@n8n\backend-network\src\http\outbound-http.ts:199:13)
    at proxyRequestToAxios (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\n8n-core\src\execution-engine\node-execution-context\utils\request-helpers\legacy-request-adapter.ts:31:9)
    at Object.request (C:\Users\ramos\AppData\Roaming\npm\node_modules\n8n\node_modules\n8n-core\src\execution-engine\node-execution-context\utils\request-helpers\factory.ts:166:11)"