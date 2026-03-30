/**
 * Configuration manuelle des codes d'accès
 * À utiliser si vous préférez gérer manuellement les codes
 * 
 * ✅ Structure: {CODE: {expires, guest, wifi, portail, notes}}
 */

const CODES_CONFIG = {
    'KATI9999': {
        expires: '2099-12-31',
        guest: 'Code Test',
        wifi: 'Katikias33',
        portail: '9999',
        notes: 'À supprimer avant production'
    }
    
    // Ajouter d'autres codes ici
    // Format: 'KATIMMJJ': { expires: 'YYYY-MM-DD', guest: 'Nom', wifi: 'SSID', portail: 'Code', notes: 'Notes' }
};

// À ajouter dans codes-acces.html après les autres scripts
// <script>
// var CODES_DATABASE = CODES_CONFIG;
// </script>
