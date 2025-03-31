// menu.js

// Referencias a los elementos del menú y botones
const menuToggle = document.getElementById('menu-toggle');
const sidebar = document.getElementById('sidebar');
const reactivateBtn = document.getElementById('reactivate-btn');

// Función para ocultar el menú
function hideMenu() {
    sidebar.classList.add('hidden'); // Oculta el menú
    reactivateBtn.style.display = 'block'; // Muestra el botón para reactivar el menú
}

// Función para mostrar el menú
function showMenu() {
    sidebar.classList.remove('hidden'); // Muestra el menú
    reactivateBtn.style.display = 'none'; // Oculta el botón
}

// Añadir el evento para el botón de menú hamburguesa
menuToggle.addEventListener('click', hideMenu);

// Añadir el evento para el botón para reactivar el menú
reactivateBtn.addEventListener('click', showMenu);
