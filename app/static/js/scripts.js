// Función para obtener usuarios
async function fetchUsers() {
    const response = await fetch('/users');
    const users = await response.json();

    const tbody = document.querySelector('#user-table tbody');
    tbody.innerHTML = ''; // Limpiar tabla

    users.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
            <td>
                <button onclick="editUser(${user.id}, '${user.name}', '${user.email}')">Editar</button>
                <button onclick="deleteUser(${user.id})">Eliminar</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Función para crear o actualizar un usuario
async function saveUser(event) {
    event.preventDefault();

    const id = document.getElementById('user-id').value;
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;

    const method = id ? 'PUT' : 'POST';
    const url = id ? `/users/${id}` : '/users';

    const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email })
    });

    if (response.ok) {
        alert(id ? 'Usuario actualizado' : 'Usuario creado');
        document.getElementById('user-form').reset();
        fetchUsers();
    } else {
        alert('Error al guardar el usuario');
    }
}

// Función para eliminar un usuario
async function deleteUser(id) {
    if (!confirm('¿Seguro que quieres eliminar este usuario?')) return;

    const response = await fetch(`/users/${id}`, { method: 'DELETE' });

    if (response.ok) {
        alert('Usuario eliminado');
        fetchUsers();
    } else {
        alert('Error al eliminar el usuario');
    }
}

// Función para cargar datos en el formulario para editar
function editUser(id, name, email) {
    document.getElementById('user-id').value = id;
    document.getElementById('name').value = name;
    document.getElementById('email').value = email;
}

// Inicializar
document.getElementById('user-form').addEventListener('submit', saveUser);
fetchUsers();
