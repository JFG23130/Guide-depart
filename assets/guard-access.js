(function () {
    const STORAGE_STATE_KEY = 'katikias_access_granted';
    const STORAGE_CODE_KEY = 'katikias_current_code';

    function getCodeFromUrl() {
        const params = new URLSearchParams(window.location.search);
        return params.get('code');
    }

    function parseDateFr(dmy) {
        if (!dmy || typeof dmy !== 'string') return null;
        const parts = dmy.split('/');
        if (parts.length !== 3) return null;
        const [dd, mm, yyyy] = parts.map(Number);
        if (!dd || !mm || !yyyy) return null;
        const d = new Date(yyyy, mm - 1, dd);
        d.setHours(0, 0, 0, 0);
        return d;
    }

    function isWithinStay(data) {
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        if (!data || !data.arrival || !data.departure) {
            return false;
        }

        const arrival = parseDateFr(data.arrival);
        const departure = parseDateFr(data.departure);
        if (!arrival || !departure) {
            return false;
        }

        return today >= arrival && today <= departure;
    }

    function blockAccess(message) {
        document.body.innerHTML = `
            <div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:20px;">
                <div style="background:#fff;border-radius:16px;padding:30px;max-width:520px;width:100%;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,0.2);">
                    <h2 style="margin-bottom:12px;">Accès restreint</h2>
                    <p style="color:#555;line-height:1.6;">${message}</p>
                    <a href="codes-acces.html" style="display:inline-block;margin-top:16px;padding:12px 18px;background:#667eea;color:#fff;text-decoration:none;border-radius:8px;">Accéder aux codes</a>
                </div>
            </div>
        `;
    }

    const codeFromUrl = getCodeFromUrl();
    if (codeFromUrl) {
        sessionStorage.setItem(STORAGE_CODE_KEY, codeFromUrl);
    }

    const granted = sessionStorage.getItem(STORAGE_STATE_KEY) === '1';
    const code = sessionStorage.getItem(STORAGE_CODE_KEY) || codeFromUrl;

    if (!granted || !code || typeof CODES_DATABASE === 'undefined') {
        const target = code ? `codes-acces.html?code=${encodeURIComponent(code)}` : 'codes-acces.html';
        window.location.replace(target);
        return;
    }

    const data = CODES_DATABASE[code.toUpperCase()];
    if (!data) {
        window.location.replace('codes-acces.html');
        return;
    }

    if (!isWithinStay(data)) {
        sessionStorage.removeItem(STORAGE_STATE_KEY);
        sessionStorage.removeItem(STORAGE_CODE_KEY);
        blockAccess('Le guide est accessible uniquement pendant votre période de séjour.');
    }
})();
