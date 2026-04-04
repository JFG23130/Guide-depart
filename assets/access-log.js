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
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                Accept: 'application/json',
                apikey: cfg.anonKey,
                Authorization: 'Bearer ' + cfg.anonKey,
                Prefer: 'return=minimal'
            },
            body: JSON.stringify([row]),
            keepalive: true
        })
            .then(function (res) {
                if (res.ok) {
                    return;
                }
                return res.text().then(function (txt) {
                    if (typeof console !== 'undefined' && console.warn) {
                        console.warn('[Guide access-log] HTTP ' + res.status, txt || '');
                    }
                });
            })
            .catch(function (err) {
                if (typeof console !== 'undefined' && console.warn) {
                    console.warn('[Guide access-log]', err);
                }
            });
    }

    window.logGuideAccessAttempt = logAccessAttempt;
})();
