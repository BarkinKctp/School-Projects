import pool from '../config/db.js';

export const getAllUsers = async () => {
    const result = await pool.query('SELECT * FROM users');
    return result.rows;
}

export const getUserById = async (id) => {
    const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
    return result.rows[0];
}

export const createUser = async (username, email) => {
    const result = await pool.query(
        'INSERT INTO users (username, email) VALUES ($1, $2) RETURNING *',
        [username, email]
    );
    return result.rows[0];
}

export const updateUser = async (id, username, email) => {
    const result = await pool.query(
        'UPDATE users SET username = $1, email = $2 WHERE id = $3 RETURNING *',
        [username, email, id]
    );
    return result.rows[0];
}

export const deleteUser = async (id) => {
    await pool.query('DELETE FROM users WHERE id = $1', [id]);
    return { message: 'User deleted successfully' };
}





