// Scripts pour le tableau de bord admin
document.addEventListener('DOMContentLoaded', function() {
    // Gestion des notifications
    const notificationBtn = document.querySelector('.btnnotification');
    if (notificationBtn) {
        notificationBtn.addEventListener('click', function() {
            alert('Ouvrir le panneau de notifications');
            // Implémenter l'ouverture du panneau de notifications
        });
    }
    // Gestion du profil admin
    const adminProfile = document.querySelector('.admin-profile');
    if (adminProfile) {
        adminProfile.addEventListener('click', function() {
            alert('Ouvrir le menu profil');
            // Implémenter le menu déroulant du profil
        });
    }
    // Filtres des tableaux
    const filterSelects = document.querySelectorAll('.filter-select');
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            alert('Filtrage appliqué: ' + this.value);
            // Implémenter le filtrage des données
        });
    });
    // Actions sur les boutons
    const actionButtons = document.querySelectorAll('.btn-icon');
    actionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const action = this.title;
            alert('Action: ' + action);
            // Implémenter les actions spécifiques
        });
    });
    // Export des données
    const exportBtn = document.querySelector('.btn[title="Exporter"]');
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            alert('Export des données en cours...');
            // Implémenter l'export CSV/Excel
        });
    }
// Recherche en temps réel
 const searchInput = document.querySelector('.search-box input');
 if (searchInput) {
 searchInput.addEventListener('input', function() {
 const query = this.value;
 if (query.length > 2) {
 console.log('Recherche:', query);
 // Implémenter la recherche AJAX
 }
 });
 }
 // Pagination
 const pageButtons = document.querySelectorAll('.page-btn');
 pageButtons.forEach(button => {
 button.addEventListener('click', function() {
 if (!this.classList.contains('active')) {
 document.querySelector('.pagebtn.active').classList.remove('active');
 this.classList.add('active');
 alert('Chargement de la page: ' + this.textContent);
 // Implémenter le changement de page
 }
 });
 });
 // Gestion des statuts
 const statusButtons = document.querySelectorAll('.status-badge');
 statusButtons.forEach(badge => {
 badge.addEventListener('click', function() {
 alert('Changer le statut de la demande');
 // Implémenter le changement de statut
 });
 });
 // Responsive menu
 const setupResponsiveMenu = () => {
 if (window.innerWidth < 768) {
 // Implémenter le menu responsive
 console.log('Mode mobile activé');
 }
 };
 window.addEventListener('resize', setupResponsiveMenu);
 setupResponsiveMenu();
 });
 // Fonctions utilitaires
 function formatDate(date) {
 return new Date(date).toLocaleDateString('fr-FR');
}
 function formatDateTime(date) {
    return new Date(date).toLocaleString('fr-FR');
 }
 function showLoading() {
    // Afficher un indicateur de chargement
    console.log('Chargement...');
 }
 function hideLoading() {
    // Cacher l'indicateur de chargement
    console.log('Chargement terminé');
 }
 // Gestion des erreurs
 function handleError(error) {
    console.error('Erreur:', error);
    alert('Une erreur est survenue. Veuillez réessayer.');
 }