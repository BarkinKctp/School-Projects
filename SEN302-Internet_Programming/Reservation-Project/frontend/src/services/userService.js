
export async function fetchUsers() {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/user`);
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to fetch users');
    }
    const result = await response.json();
    return result.data;
}

export async function editUser(id, userData) {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/user/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to edit user');
    }
    const result = await response.json();
    return result.data;
}

export async function deleteUser(id) {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/user/${id}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to delete user');
    }
    const result = await response.json();
    return result.data;
}

export async function createUser(userData) {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/user`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to create user');
    }
    const result = await response.json();
    return result.data;
}

