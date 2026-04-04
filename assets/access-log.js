/**
 * Journal optionnel des tentatives de connexion (codes-acces.html).
 * Configurez window.__ACCESS_LOG__ dans access-log-config.js (voir .example).
 */
(function () {
    function logAccessAttempt(entry) {
        var cfg = typeof window !== 'undefined' ? window.__ACCESS_LOG__ : null;
        if (!cfg || !cfg.supabaseUrl || !cfg.anonKey) {
            return Promise.resolve();
        }
        var table = cfg.table || 'guide_access_attempts';
        var base = String(cfg.supabaseUrl).replace(/\/$/, '');
        var url = base + '/rest/v1/' + table;
        var row = {
            code_text: entry.code || '',
            outcome: entry.outcome === 'ok' ? 'ok' : 'fail',
            reason: entry.reason != null ? String(entry.reason) : null
        };
        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                apikey: cfg.anonKey,
                Authorization: 'Bearer ' + cfg.anonKey,
                Prefer: 'return=minimal'
            },
            body: JSON.stringify([row]),
            keepalive: true
        }).catch(function () {});
    }

    window.logGuideAccessAttempt = logAccessAttempt;
})();
